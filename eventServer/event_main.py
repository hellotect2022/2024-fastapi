from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketClose
import asyncio

import uvicorn
#import redis
import redis.asyncio as aioredis
import json


app = FastAPI()

async def handle_messages(websocket: WebSocket, user_id: str, pubsubChannel):
    try:
        async for message in pubsubChannel.listen():
            if message['type'] != 'subscribe':
                try:# 메시지 유효성 검사
                    await websocket.send_text(message['data'].decode('UTF-8'))
                except json.JSONDecodeError:
                    # 메시지 형식이 올바르지 않을 경우 처리
                    print(f"Invalid message format received: {message['data']}")
                except WebSocketClose:
                    # WebSocket 연결이 닫힌 경우 처리
                    print(f"WebSocket connection closed for user {user_id}")
                    break
    except Exception as e:
        print(f"Error handling message for user {user_id}: {e}")
    finally:
        print(f"Cleaning up resources for user {user_id}")
        await pubsubChannel.unsubscribe(user_id)
        await pubsubChannel.aclose()
    # while True:
    #     message = pubsub.get_message()
    #     if message is not None and message['type'] != 'subscribe':
    #         try:
    #             data = json.loads(message['data'].decode('UTF-8'))  # 메시지 유효성 검사
    #             await websocket.send_text(json.dumps(data))
    #         except json.JSONDecodeError:
    #             # 메시지 형식이 올바르지 않을 경우 처리
    #             print(f"Invalid message format received: {message['data']}")
    #         except WebSocketClose:
    #             # WebSocket 연결이 닫힌 경우 처리
    #             print(f"WebSocket connection closed for user {user_id}")
    #             break
    #     await asyncio.sleep(0.1)  # 작업에 대한 CPU 점유를 막기 위해 짧은 대기시간을 추가

@app.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        obj = json.loads(data)
        print(f"웹소켓 : {obj}")
        await websocket.send_text(data)

        #redisClient = redis.StrictRedis(host="10.10.27.119", port=6379, db=0)
        redisClient = aioredis.StrictRedis(host="10.10.27.119", port=6379, db=0)
        pubsub = redisClient.pubsub()
        #pubsub.subscribe(obj["userId"])
        await pubsub.subscribe(obj["userId"])
        task = asyncio.create_task(handle_messages(websocket, obj["userId"], pubsub))
        try:
            await task
        except asyncio.CancelledError:
            print(f"{obj['userId']} 연결이 끊김")
        finally:
            task.cancel()
            await redisClient.aclose()
    except WebSocketDisconnect:
        print("WebSocket connection closed by client")
    except json.JSONDecodeError:
        print("Received invalid JSON data")
    finally:
        await websocket.close()




if __name__ == "__main__":
    #test()
    uvicorn.run(app,host="0.0.0.0",port=7777)