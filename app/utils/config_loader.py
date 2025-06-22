import os
from dotenv import load_dotenv

class ConfigLoader:
    """
    Tải biến môi trường và cấu hình hệ thống từ file .env
    """

    def __init__(self, env_path=".env"):
        load_dotenv(env_path)

    def get(self, key: str, default=None):
        return os.getenv(key, default)
