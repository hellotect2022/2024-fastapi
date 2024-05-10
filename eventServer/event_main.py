from fastapi import FastAPI, WebSocket

import uvicorn
import redis


app = FastAPI()


@app.websocket("/test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    redisClient = redis.StrictRedis(host="10.10.27.119", port=6379, db=0)
    # 현재 사용 가능한 채널 조회
    channels = redisClient.pubsub_channels()
    # 조회된 채널 출력
    print("Available channels:")
    for channel in channels:
        print(channel)

    i: int = 1
    while True:
        data = await websocket.receive_text()
        print(f"웹소켓 : {data}")
        await websocket.send_text(f"Message text was: {data}")

def test():
    redisClient = redis.StrictRedis(host="10.10.27.119", port=6379, db=0)
    channels = ["test", "test", "test2", "test3"]
    pubsubs = [redisClient.pubsub() for _ in range(len(channels))]

    for pubsub, channel in zip(pubsubs,channels):
        pubsub.subscribe(channel)

    while True:
        for pubsub in pubsubs:
            message = pubsub.get_message()
            if message is not None : print("message : ",message)


if __name__ == "__main__":
    #test()
    uvicorn.run(app,host="0.0.0.0",port=7777)