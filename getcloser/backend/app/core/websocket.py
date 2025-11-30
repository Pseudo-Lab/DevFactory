from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from core.dependencies import get_current_user
from core.security import verify_access_token

router = APIRouter()
active_sockets: dict[int, WebSocket] = {}

@router.websocket("/invitations")
async def websocket_endpoint(websocket: WebSocket):
    try:
      user_id = verify_access_token(websocket.headers.get("Sec-Websocket-Protocol"))["sub"]
    except HTTPException:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    active_sockets[user_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_sockets[user_id]

async def notify_invitation(member_ids, team):
    for uid in member_ids:
        if uid in active_sockets:
            await active_sockets[uid].send_json({
                "event": "team_invitation",
                "team_id": team.id,
                "members": member_ids,
                "expires_at": str(team.expires_at)
            })
