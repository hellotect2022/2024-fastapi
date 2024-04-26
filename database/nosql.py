from motor import motor_asyncio

MONGO_URL = "mongodb://10.10.27.119:27017"

client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = client.test2