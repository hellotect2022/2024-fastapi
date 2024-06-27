import datetime
import json

from fastapi import APIRouter
from utils import RedisHelper, LogHelper

router = APIRouter(prefix="/test")

@router.get("/hello")
async def test() -> dict:
    return {"status":"success"}

# 사용자 로그인 관련
@router.post("/regist")
async def test(body:dict) -> dict:
    print("/regist, body-> ",body)
    # 1. regist 시에 현재 날짜를 기준으로 redis user:current 에 sortedSet 으로 집어넣는다.
    parameter = {body['userId']: datetime.datetime.now().timestamp()}
    print('log  ',parameter)
    resultdata = RedisHelper.setSortedSet("user:current",parameter)
    param :dict = {'userName':body['userId'], 'profileUrl':""}
    RedisHelper.setHashMap("user:info",{body['userId']:json.dumps(param)})
    print('resultdata->',resultdata)
    return {"status":"success"}


# 사용자 목록 조회 하는방법
@router.post("/getUserAll")
async def getUserList() -> dict:
    resultdata = RedisHelper.getSortedSet("user:current",min_score='-inf',max_score='+inf')
    print('resultdata->',resultdata)
    list = [] ;
    for data in resultdata:
        #user:info dhhan:{}
        tmp = RedisHelper.getHashMap("user:info",data[0].decode('utf-8'))
        value = {'userId': data[0], 'loginTime': int(data[1]), 'userName':tmp['userName'], 'profileUrl':tmp['profileUrl']}
        list.append(value)
    return {"status":"success"
            ,"userList" : list
            }
