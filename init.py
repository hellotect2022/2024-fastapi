from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from main.router import testRouter
from setting.Settings import Settings
from utils.redisUtil import RedisHelper
from utils.logUtil import LogHelper
import sys
# def custom_excepthook(exc_type, exc_value, exc_traceback):
#     logHelper = LogHelper()
#     logHelper.logger.error(exc_value)
#     # logHelper.logger.error("Unexpected exception..",
#     #              exc_info=(exc_type, exc_value, exc_traceback)
#     #              )
#
# sys.excepthook = custom_excepthook

app = FastAPI()

app.include_router(testRouter.router,tags=["test"])

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    settings = Settings()
    RedisHelper.setKey("dhhan","hi")
    print("get key:",RedisHelper.getKey("dhhan"))
    #uvicorn.run(app,host=settings.server_host,port=int(settings.server_port),log_level="info")