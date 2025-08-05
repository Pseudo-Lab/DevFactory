import datetime
import json
import logging
import os

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Notion API 설정
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE_URL = "https://api.notion.com/v1"

# Discord Webhook 설정
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def get_property_value(prop: dict) -> str:
    """Extracts the value from a Notion property object as a string."""
    prop_type = prop.get("type")

    if prop_type == "title":
        # Title is handled separately in the embed title
        return ""
    elif prop_type == "rich_text":
        return "".join(item.get("plain_text", "") for item in prop.get("rich_text", []))
    elif prop_type == "number":
        return str(prop.get("number"))
    elif prop_type == "select":
        select_info = prop.get("select")
        return select_info.get("name", "") if select_info else ""
    elif prop_type == "multi_select":
        return ", ".join(option.get("name", "") for option in prop.get("multi_select", []))
    elif prop_type == "date":
        date_info = prop.get("date")
        if not date_info:
            return ""
        start_date_str = date_info.get("start")
        if not start_date_str:
            return ""

        try:
            if "T" in start_date_str:
                dt_obj = datetime.datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
                if dt_obj.tzinfo:
                    kst = datetime.timezone(datetime.timedelta(hours=9))
                    dt_obj = dt_obj.astimezone(kst)
                return dt_obj.strftime("%Y-%m-%d %H:%M")
            else:
                return start_date_str
        except (ValueError, TypeError):
            return start_date_str
    elif prop_type == "email":
        return prop.get("email", "")
    elif prop_type == "phone_number":
        return prop.get("phone_number", "")
    elif prop_type == "url":
        return prop.get("url", "")
    elif prop_type == "checkbox":
        return "✅" if prop.get("checkbox") else "⬜️"
    elif prop_type == "created_time":
        dt_str = prop.get("created_time", "")
        if not dt_str:
            return ""
        try:
            # UTC 시간을 파싱하여 timezone-aware 객체로 만듭니다.
            dt_obj = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            # KST (UTC+9)로 변환합니다.
            kst = datetime.timezone(datetime.timedelta(hours=9))
            kst_dt = dt_obj.astimezone(kst)
            # YYYY-MM-DD HH:MM (24시간) 형식으로 포맷합니다.
            return kst_dt.strftime("%Y-%m-%d %H:%M")
        except (ValueError, TypeError):
            return dt_str
    return ""


def format_properties_for_discord(properties: dict) -> list:
    """Formats Notion page properties into a list of Discord embed fields."""
    fields = []
    # Properties to display
    props_to_show = {name: prop for name, prop in properties.items() if prop.get("type") != "title"}

    for name, prop in props_to_show.items():
        value = get_property_value(prop)
        if value:
            # Add field. `inline: True` allows multiple fields to sit on the same line.
            fields.append({"name": name, "value": str(value), "inline": True})

    # To avoid having an odd number of inline fields which can look weird,
    # add a blank inline field if the number of fields is odd.
    if len(fields) > 0 and len(fields) % 2 == 1:
        fields.append({"name": "\u200b", "value": "\u200b", "inline": True})

    return fields


def send_discord_notification(page_title: str, database_title: str, page_url: str, database_url: str, fields: list = None):
    """Discord로 알림을 보냅니다."""
    if not DISCORD_WEBHOOK_URL:
        logger.error("Discord Webhook URL이 설정되지 않았습니다.")
        return

    embed = {
        "title": f"📝 {database_title}에 새로운 폼이 작성되었습니다",
        "color": 5814783,  # 파란색
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }

    all_fields = [
        {"name": "페이지 제목", "value": f"[{page_title}]({page_url})", "inline": False}
    ]

    if fields:
        all_fields.extend(fields)

    all_fields.append(
        {
            "name": "\u200b",
            "value": f"[**↗️ 페이지 바로가기**]({page_url})\n[**↗️ {database_title} DB 바로가기**]({database_url})",
            "inline": False,
        }
    )

    embed["fields"] = all_fields

    payload = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            logger.error(f"Discord 알림 전송 실패: {response.text}")
    except Exception as e:
        logger.error(f"Discord 알림 전송 중 오류 발생: {e}")


def get_notion_page_info(page_id: str) -> dict:
    """Notion 페이지 정보를 가져옵니다."""
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": NOTION_API_VERSION, "Content-Type": "application/json"}

    response = requests.get(f"{NOTION_API_BASE_URL}/pages/{page_id}", headers=headers)

    if response.status_code != 200:
        logger.error(f"페이지 정보 조회 실패: {response.text}")
        return None

    return response.json()


def get_database_title(data: dict) -> str:
    database_title = data.get("title", [{}])[0].get("plain_text")
    return database_title


def get_page_title(page_info: dict) -> str:
    """Notion 페이지 정보에서 제목을 추출합니다."""
    properties = page_info.get("properties", {})
    for prop in properties.values():
        if prop.get("type") == "title":
            title_list = prop.get("title", [])
            if title_list:
                return title_list[0].get("plain_text", "제목 없음")
    return "제목 없음"


def get_notion_database_info(database_id: str) -> dict:
    """Notion 데이터베이스 정보를 가져옵니다."""
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": NOTION_API_VERSION, "Content-Type": "application/json"}

    response = requests.get(f"{NOTION_API_BASE_URL}/databases/{database_id}", headers=headers)

    if response.status_code != 200:
        logger.error(f"데이터베이스 정보 조회 실패: {response.text}")
        return None

    return response.json()


def process_data(data: dict):
    """웹훅 데이터를 처리하고 페이지/데이터베이스 정보를 가져옵니다."""
    try:
        if data.get("type") == "page.created":
            page_id = data.get("entity", {}).get("id")
            parent_info = data.get("data", {}).get("parent", {})
            database_id = None
            if parent_info.get("type") == "database":
                database_id = parent_info.get("id")

            if not page_id or not database_id:
                logger.error(f"페이로드에서 page_id 또는 database_id를 찾을 수 없습니다. page_id: {page_id}, database_id: {database_id}")
                return

            # 페이지 정보 가져오기
            page_info = get_notion_page_info(page_id)
            logger.info(f"page_info: {page_info}")
            database_info = get_notion_database_info(database_id)

            if page_info and database_info:
                page_title = get_page_title(page_info)
                database_title = get_database_title(database_info)
                page_url = page_info.get("url")
                database_url = database_info.get("url")
                form_content_fields = format_properties_for_discord(page_info.get("properties", {}))

                logger.info(f"생성된 페이지 제목: {page_title}")
                logger.info(f"데이터베이스 제목: {database_title}")
                logger.info(f"페이지 URL: {page_url}")
                logger.info(f"데이터베이스 URL: {database_url}")

                # Discord로 알림 전송
                if page_url and database_url:
                    send_discord_notification(page_title, database_title, page_url, database_url, form_content_fields)
                else:
                    logger.error("페이지 또는 데이터베이스 URL을 가져올 수 없습니다.")

    except Exception as e:
        logger.error(f"데이터 처리 중 오류 발생: {e}", exc_info=True)


@app.get("/")
async def read_root():
    return {"message": "Server is running"}


# @app.get("/test")
# async def test():
#     # NOTE: 테스트를 위해서는 유효한 page_id와 database_id를 사용해야 합니다.
#     page_id = ""
#     database_id = ""
#     page_info = get_notion_page_info(page_id)
#     database_info = get_notion_database_info(database_id)
#     if page_info and database_info:
#         page_title = get_page_title(page_info)
#         database_title = get_database_title(database_info)
#         page_url = page_info.get("url")
#         database_url = database_info.get("url")
#         form_content_fields = format_properties_for_discord(page_info.get("properties", {}))
#         send_discord_notification(page_title, database_title, page_url, database_url, form_content_fields)
#         return {"page_info": page_info, "database_info": database_info, "database_title": database_title}
#     else:
#         return {"error": "Could not retrieve page or database info. Check your test IDs."}


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    웹훅 이벤트를 수신하고 처리합니다.
    """
    logger.info(f"수신된 헤더: {request.headers}")

    try:
        payload = await request.json()

        # 웹훅 인증 토큰 확인
        if "verification_token" in payload:
            logger.info("\n==================================================")
            logger.info(">>> 웹훅 공급자로부터 인증 요청을 수신했습니다. <<<")
            logger.info(f"인증 페이로드: {payload}")
            logger.info("==================================================\n")
            return {"status": "success", "message": "인증 요청이 성공적으로 수신되었습니다."}
        else:
            logger.info(f"수신된 웹훅 페이로드: {payload}")

        # 웹훅 데이터 처리
        process_data(payload)

        return {"status": "success", "message": "웹훅이 성공적으로 수신되었습니다."}

    except json.JSONDecodeError:
        logger.error("잘못된 JSON 페이로드 수신")
        raise HTTPException(status_code=400, detail="잘못된 JSON 페이로드입니다.")
    except Exception as e:
        logger.error(f"웹훅 처리 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="내부 서버 오류가 발생했습니다.")


if __name__ == "__main__":
    # Uvicorn을 사용하여 FastAPI 앱 실행
    # reload 옵션을 사용할 때는 import string 형태로 전달해야 합니다
    uvicorn.run("test:app", host="0.0.0.0", port=8000, reload=True)
