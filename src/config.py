import os


def get_version():
    try:
        with open("VERSION", "r") as f:
            version = f.read().strip()
        return version
    except FileNotFoundError:
        return "0.0.0"  # Valor por defecto en caso de que no exista el archivo VERSION


class Config:
    PORT: int = int(os.getenv("PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecretkey")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    VERSION: str = get_version()
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
