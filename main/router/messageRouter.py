import json

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from ..model.modelVO import User, Message
from database.nosql import db
from bson import ObjectId
from utils import RedisHelper, LogHelper
import jwt
from passlib.context import CryptContext
from setting.Settings import Settings
import time
from datetime import datetime


# Crypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = Settings()

router = APIRouter(prefix="/api")

@router.post("/sendMessage")
#async def sendMessage(message: Message,token:str = Depends(authenticate)) -> dict:
async def sendMessage(message: Message) -> dict:
    userList = RedisHelper.getSmembers("room:"+message.roomId)
    print("userList->",userList)
    print("senMessage -> ",message)
    for user in userList:
        RedisHelper.publish(user,message.json())
    return {"status":"success"}