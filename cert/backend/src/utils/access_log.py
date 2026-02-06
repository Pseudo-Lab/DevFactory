import hashlib
import logging
import os
import time
from dataclasses import dataclass
from typing import Optional, Set

import asyncpg
from fastapi import FastAPI, Request, Response


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AccessLogConfig:
    dsn: str
    exclude_paths: Set[str]
    ip_salt: str
    environment: str


def _build_dsn() -> Optional[str]:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([host, port, name, user, password]):
        logger.warning(
            "Access logging disabled: database env vars missing",
            extra={
                "configured": {
                    "DB_HOST": bool(host),
                    "DB_PORT": bool(port),
                    "DB_NAME": bool(name),
                    "DB_USER": bool(user),
                    "DB_PASSWORD": bool(password),
                }
            },
        )
        return None

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def load_access_log_config() -> Optional[AccessLogConfig]:
    enabled = os.getenv("ACCESS_LOGGING_ENABLED", "true").lower() in {"1", "true", "yes"}
    if not enabled:
        logger.info("Access logging disabled via ACCESS_LOGGING_ENABLED")
        return None

    dsn = _build_dsn()
    if not dsn:
        return None

    exclude_raw = os.getenv("ACCESS_LOGGING_EXCLUDE_PATHS", "/health,/api/certs/all-projects,/api/log/pageview")
    exclude_paths = {path.strip() for path in exclude_raw.split(",") if path.strip()}
    ip_salt = os.getenv("ACCESS_LOGGING_IP_SALT", "")
    environment = os.getenv("ENVIRONMENT", "dev").lower()

    return AccessLogConfig(
        dsn=dsn,
        exclude_paths=exclude_paths,
        ip_salt=ip_salt,
        environment=environment,
    )


def _hash_ip(ip_address: Optional[str], salt: str) -> Optional[str]:
    if not ip_address:
        return None
    digest = hashlib.sha256(f"{salt}{ip_address}".encode("utf-8")).hexdigest()
    return digest


async def init_access_log(app: FastAPI) -> None:
    config = load_access_log_config()
    if not config:
        app.state.access_log_pool = None
        app.state.access_log_config = None
        return

    pool = await asyncpg.create_pool(dsn=config.dsn, min_size=1, max_size=5)
    app.state.access_log_pool = pool
    app.state.access_log_config = config


async def close_access_log(app: FastAPI) -> None:
    pool = getattr(app.state, "access_log_pool", None)
    if pool:
        await pool.close()


def _get_client_ip(request: Request) -> Optional[str]:
    """Extracts the client IP address from request headers or client info."""
    # Check X-Forwarded-For header (common for reverse proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can be a comma-separated list; the first one is the original client
        return forwarded_for.split(",")[0].strip()

    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fallback to request.client.host
    if request.client:
        return request.client.host

    return None


async def log_request(
    request: Request,
    response: Optional[Response],
    latency_ms: int,
    status_code: int,
) -> None:
    config: Optional[AccessLogConfig] = getattr(request.app.state, "access_log_config", None)
    pool: Optional[asyncpg.Pool] = getattr(request.app.state, "access_log_pool", None)

    if not config or not pool:
        return

    if request.url.path in config.exclude_paths:
        return

    client_ip = _get_client_ip(request)
    ip_hash = _hash_ip(client_ip, config.ip_salt)
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer") or request.headers.get("referrer")

    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO logging.access_log
                    (path, method, status, latency_ms, ip_hash, user_agent, referrer)
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7)
                """,
                request.url.path,
                request.method,
                status_code,
                latency_ms,
                ip_hash,
                user_agent,
                referrer,
            )

    except Exception:
        logger.warning("Failed to write access log", exc_info=True)


async def log_page_view(request: Request, page_path: str) -> None:
    config: Optional[AccessLogConfig] = getattr(request.app.state, "access_log_config", None)
    pool: Optional[asyncpg.Pool] = getattr(request.app.state, "access_log_pool", None)

    if not config or not pool:
        return

    client_ip = _get_client_ip(request)
    ip_hash = _hash_ip(client_ip, config.ip_salt)
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer") or request.headers.get("referrer")

    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO logging.access_log
                    (path, method, status, latency_ms, ip_hash, user_agent, referrer)
                VALUES
                    ($1, $2, $3, $4, $5, $6, $7)
                """,
                page_path,
                "PAGEVIEW",
                200,
                None,
                ip_hash,
                user_agent,
                referrer,
            )
    except Exception:
        logger.warning("Failed to write pageview log", exc_info=True)


async def access_log_middleware(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        latency_ms = int((time.perf_counter() - start) * 1000)
        await log_request(request, None, latency_ms, status_code=500)
        raise

    latency_ms = int((time.perf_counter() - start) * 1000)
    await log_request(request, response, latency_ms, status_code=response.status_code)
    return response
