import base64

# It's deprecated :c
# from passlib.context import CryptContext
#
# pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
#
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return base64.b64encode(plain_password.encode()).decode() == hashed_password


def get_password_hash(password: str) -> str:
    return base64.b64encode(password.encode()).decode()
