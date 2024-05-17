from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio

import uvicorn
import redis
import json


app = FastAPI()

async def handle_messages(websocket: WebSocket, user_id: str, pubsub):
    while True:
        message = pubsub.get_message()
        if message is not None and message['type'] != 'subscribe':
            await websocket.send_text(message['data'].decode('UTF-8'))
        await asyncio.sleep(0.1)  # 작업에 대한 CPU 점유를 막기 위해 짧은 대기시간을 추가

@app.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    data = await websocket.receive_text()
    obj = json.loads(data)
    print(f"웹소켓 : {obj}")
    await websocket.send_text(data)
    redisClient = redis.StrictRedis(host="10.10.27.119", port=6379, db=0)

    pubsub = redisClient.pubsub()
    pubsub.subscribe(obj["userId"])

    task = asyncio.create_task(handle_messages(websocket, obj["userId"], pubsub))
    try:
        await task
    except asyncio.CancelledError:
        print(f"{obj['userId']} 연결이 끊김")
    finally:
        task.cancel()




if __name__ == "__main__":
    #test()
    uvicorn.run(app,host="0.0.0.0",port=7777)