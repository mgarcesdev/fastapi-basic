from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

app = FastAPI(docs_url="/")
PORT = 8000

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
# Clave secreta para firmar el JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedpassword",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# Crear JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verificar usuario
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["hashed_password"] != "fakehashed" + password:
        return False
    return user


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Generar Access Token
    access_token = create_access_token(data={"sub": user["username"]},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # Generar Refresh Token (con mayor tiempo de expiración)
    refresh_token = create_access_token(data={"sub": user["username"]},
                                        expires_delta=timedelta(days=7))  # Refresh token válido por 7 días

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@app.post("/token/refresh")
async def refresh_token(request: RefreshTokenRequest):
    refresh_token = request.refresh_token
    try:
        # Decodificar y validar el Refresh Token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Generar un nuevo Access Token
        access_token = create_access_token(data={"sub": username},
                                           expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}


@app.get("/test")
def read_root():
    return {"message": "¡Hola, mundo!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}


def run_server():
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)


if __name__ == "__main__":
    run_server()
