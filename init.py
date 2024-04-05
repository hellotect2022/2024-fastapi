import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from main.router import testRouter
from setting.Settings import Settings

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
    uvicorn.run(app,host=settings.server_host,port=int(settings.server_port),log_level="info")