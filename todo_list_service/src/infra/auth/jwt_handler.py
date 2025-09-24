import jwt
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import InvalidTokenException
from datetime import datetime, timezone, timedelta


class JWTHandler:

    def __init__(self, secret, algorithm, jwt_expiration_minutes):
        self.JWT_SECRET = secret
        self.JWT_ALGORITHM = algorithm
        self.jwt_expiration_minutes = jwt_expiration_minutes
        
    
    def create_jwt_token(
        self,
        payload: JWTPayload,
    ) -> str:
        
        now = datetime.now(timezone.utc).replace(microsecond=0)
        
        payload.exp = now + timedelta(minutes=self.jwt_expiration_minutes)
        
        return jwt.encode(payload.model_dump(), self.JWT_SECRET, self.JWT_ALGORITHM)

    def decode_jwt_token(
        self,
        token: str,
    ) -> JWTPayload:
        try:
            payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError as ex:
            payload: dict = jwt.decode(token, options={"verify_signature": False})
            token_type = payload.get("type", "access")
            
            raise InvalidTokenException(status_code=401, message=f"Invalid {token_type} token. {ex}")
        
        return JWTPayload.model_validate(payload)
    
    def is_token_valid(
        self,
        token: JWTPayload,
    ) -> bool:
        
        now = datetime.now(timezone.utc).replace(microsecond=0)
        expiration_time: datetime = token.exp
                
        if (not expiration_time) or (expiration_time.astimezone(timezone.utc) < now):
            return False

        return True