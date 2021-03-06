from passlib import CryptoContext

pwd_context = CryptoContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_passwod: str):
    return pwd_context.verify(plain_password, hashed_passwod)
