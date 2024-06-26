import datetime

from fastapi import APIRouter
from utils import RedisHelper, LogHelper

router = APIRouter(prefix="/test")

@router.get("/hello")
async def test() -> dict:
    return {"status":"success"}

@router.post("/regist")
async def test(body:dict) -> dict:
    print("/regist, body-> ",body)
    # 1. regist 시에 현재 날짜를 기준으로 redis user:current 에 sortedSet 으로 집어넣는다.
    parameter = {body['userId']: datetime.datetime.now().timestamp()}
    print('log  ',parameter)
    resultdata = RedisHelper.setSortedSet("user:current",parameter)
    print('resultdata->',resultdata)
    return {"status":"success"}
