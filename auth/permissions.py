import jwt
from fastapi import  HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
import hashlib
import secrets
import string



class AuthHandler():
    security =HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret='SECRET'

    def get_password_hash(self,password):
        """This Function returns hashed password. It takes in a clean password and returns the hash"""
        try:
            return self.pwd_context.hash(password)
        except Exception as e:
            print(e)

    def verify_password(self, plain_password, hashed_password):
        """This Function checks if the passwords match. It  returns boolean value. """
        return self.pwd_context.verify(plain_password, hashed_password)



    def encode_token(self, user_id):
        """This Function creates a JWT token. It takes in the user ID which will be used as the subject of the token"""
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=25),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )



    def decode_token(self, token):
        """This Function creates a JWT token. It takes in the user ID which will be used as the subject of the token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        """This Function is a dependency injection wrapper for auth."""
        return self.decode_token(auth.credentials)

    def generate_and_hash_token(self,token: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(token.encode("utf-8"))
        hashed_token = sha256.hexdigest()
        return hashed_token

    def create_secret_string(self,length: int = 16) -> tuple:
        alphabet = string.ascii_letters + string.digits
        secret = ''.join(secrets.choice(alphabet) for _ in range(length))
        hashed_secret = self.generate_and_hash_token(secret)
        return secret, hashed_secret



