import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
class Config:
    MONGO_URI = os.getenv("MONGO_URI")
