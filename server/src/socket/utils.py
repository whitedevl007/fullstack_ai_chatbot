from fastapi import WebSocket, status, Query
from typing import Optional
from ..redis.config import Redis

async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):

    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    redis_instance = Redis()  # Create an instance of Redis
    redis_client = await redis_instance.create_connection()  # Call create_connection() on the instance
    isexists = await redis_client.exists(token)

    if isexists == 1:
        return token
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")
