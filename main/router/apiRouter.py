import json

from fastapi import APIRouter, HTTPException, status
from ..model.modelVO import User
from database.nosql import db
from bson import ObjectId
from utils.redisUtil import RedisHelper

router = APIRouter(prefix="/api")

@router.post("/register")
async def register(user: User) -> dict:
    print(user)
    #user_exist = await db.users.find_one({'username': user.username})
    user_exist = RedisHelper.getHashMap(f"user:{user.username}")
    print('result',user_exist)

    if user_exist:
        d = {'error_code':104,'message':'User is existed'}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)
    # 패스워드 인크립트
    RedisHelper.setHashMap(f"user:{user.username}", user.to_dict_with_empty_string())
    #doc = await db.users.insert_one({ 'username' : user.username, 'password' : user.password })

    return { 'message' : 'User is created' }


# @router.post("/register")
# async def register(user: User) -> dict:
#     print (user)
#     user_exist = await db.users.find_one({'email' : user.username})
#
#     if user_exist:
#       d = json.dumps({ 'error_code' : 104, 'message' : 'User is existed'})
#       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=d)
#
#     password = create_hash(user.password)
#     print(password)
#     c = { 'email' : user.username, 'password' : password }
#     doc = await db.users.insert_one(c)
#
#     ret = { 'message' : 'User is created' }
#     return ret