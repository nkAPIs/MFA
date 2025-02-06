import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import pyotp
from constants import Constants

# **************************************************************************************
# Secret key and algorithm for JWT
SECRET_KEY = "1i743secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

constants = Constants()

def authenticate_user(username: str, password: str):
    if username == constants.user and password == constants.password:
        return {"username": username}
    return None

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def strip_spaces(s):
    return s.replace(" ", "")

def generate_totp(secret_key, digits=6, period=30, algorithm='SHA1'):
    secret_key = strip_spaces(secret_key)
    totp = pyotp.TOTP(secret_key, digits=digits, interval=period, digest=algorithm.lower())
    return totp.now()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user["username"]}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/getsecret")
async def read_item(secret: str, token: str = Depends(verify_token)):
    return {"token": generate_totp(secret)}


# **************************************************************************************
# **************************************************************************************
if __name__ == "__main__":
    uvicorn.run(app,port=8000, host="0.0.0.0")
# **************************************************************************************
# **************************************************************************************