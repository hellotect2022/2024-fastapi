import os

from dotenv import load_dotenv

# find path
dotenv_path = os.path.join(os.path.dirname(__file__),'.dev-env')

class Settings:
    def __init__(self):
        # Load .env file into environment variables
        #print('aa',dotenv_path)
        load_dotenv(dotenv_path)
        #Get variables from environment
        self.redis_host = os.getenv("redis_host")
        self.redis_port = os.getenv("redis_port")
        self.server_host = os.getenv("server_host")
        self.server_port = os.getenv("server_port")
        self.db_host = os.getenv("db_host")
        self.db_port = os.getenv("db_port")
        self.db_user = os.getenv("db_user")
        self.db_passwd = os.getenv("db_passwd")
        self.db_database = os.getenv("db_database")
        self.token_delta = os.getenv("delta")
        self.token_secret = os.getenv("secret")