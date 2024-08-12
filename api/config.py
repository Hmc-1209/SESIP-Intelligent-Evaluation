import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')

# JWT token configuration
access_token_secret_key = os.getenv("ACCESS_TOKEN_SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_days = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")

# Other configuration
base_path = os.getenv("BASE_PATH")
api_key = os.getenv("API_KEY")
