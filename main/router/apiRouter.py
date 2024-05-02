import json

from fastapi import APIRouter, HTTPException, status
from ..model.modelVO import User
from database.nosql import db
from bson import ObjectId
from utils.combinedUtils import RedisHelper, LogHelper
import jwt
from passlib.context import CryptContext

# Crypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(prefix="/api")
apilogHelper = LogHelper()

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
  token = jwt.encode(payload, config['secret'], algorithm='HS256')
  return token

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
            payload = {'userid': userid, 'email': user_exist['email'], 'until': int(time.time()) + int(config['delta'])}
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