import os


class Config:
    PORT: int = int(os.getenv("PORT", 8002))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecretkey")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
