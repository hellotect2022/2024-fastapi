from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from main.router import testRouter, registRouter, messageRouter, userRouter
from setting.Settings import Settings
from utils.redisUtil import RedisHelper
from utils.logUtil import LogHelper
import sys
import uvicorn


app = FastAPI()

app.include_router(testRouter.router,tags=["test"])
app.include_router(registRouter.router, tags=["api"])
app.include_router(messageRouter.router, tags=["api"])
app.include_router(userRouter.router, tags=["api"])

origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(app,host=settings.server_host,port=int(settings.server_port),log_level="info")