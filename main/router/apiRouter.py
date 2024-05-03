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

@router.post("/register")
async def userRegister(user: User) -> dict:
    print("RequestBody(User) :",user)
    #user_exist = await db.users.find_one({'username': user.username})
    user_exist = RedisHelper.getHashMap(f"user:{user.username}")

    print('유저 존재여부 체크 -> result',user_exist)

    if user_exist:
        d = {'error_code':104,'message':'User is existed'}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)
    # 패스워드 인크립트
    user.password = create_hash(user.password)
    print("hashed_password : ",user.password)

    RedisHelper.setHashMap(f"user:{user.username}", user.to_dict_with_empty_string())
    #doc = await db.users.insert_one({ 'username' : user.username, 'password' : user.password })

    return { 'message' : 'User is created' }

def create_hash(password: str):
    return bcrypt_context.hash(password)

def verify_hash(plain_password:str, hashed_password:str):
    return bcrypt_context.verify(plain_password,hashed_password)

def create_access_token(payload: dict):
  token = jwt.encode(payload, settings.token_secret, algorithm='HS256')
  return token

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")

async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        d = json.dumps({ 'error_code' : 103, 'message' : 'Token is not existed'})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)

    decoded_token = verify_access_token(token)
    return decoded_token

def verify_access_token(token: str) -> str:
    try:
        data = jwt.decode(token, settings.token_secret, algorithms=['HS256'])
        print(data)

        until = data.get("until")
        t1 = datetime.utcfromtimestamp(until)
        print(t1)
        t2 = datetime.utcnow()
        print(t2)

        if until is None:
            d = json.dumps({'error_code': 100, 'message': 'No access token'})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)
        if datetime.utcnow() > datetime.utcfromtimestamp(until):
            d = json.dumps({'error_code': 101, 'message': 'Token is expired'})
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)
        return data

    except Exception as e:
        LogHelper().error(e)
       # d = json.dumps({'error_code': 102, 'message': str(e)})
        #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)

@router.post("/login")
async def userLogin(user: User) -> dict:
    print("RequestBody(User) :", user)
    # user_exist = await db.users.find_one({'username': user.username})
    user_exist = RedisHelper.getHashMap(f"user:{user.username}")

    print('유저 존재여부 체크 -> result', user_exist["password"])

    if user_exist:
        result = verify_hash(user.password,user_exist["password"])
        print("result : ",result)

        if result == True :
            payload = {'username': user_exist['username'], 'email': user_exist['email'], 'until': int(time.time()) + int(settings.token_delta)}
            print(payload)
            token = create_access_token(payload)
            ret = {'access_token': token, 'token_type': 'Bearer'}
            return ret
        else:
            d = {'error_code': 105, 'message': 'Password is not correct'}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)


    else:
        d = {'error_code': 104, 'message': 'User is not existed'}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)

    return {'message' : 'login successed!!'}


@router.get("/token")
async def checkUserToken(token:str = Depends(authenticate)) -> dict:
    ret = {'token': token}
    return ret

@router.post("/sendMessage")
async def sendMessage(message: Message,token:str = Depends(authenticate)) -> dict:
    RedisHelper.publish("test",message.context)
    return {"status":"success"}