from passlib import CryptoContext

pwd_context = CryptoContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)
