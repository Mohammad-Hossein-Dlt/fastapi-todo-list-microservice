from src.infra.broker_config.app import app
from src.worker.consumer.rabbitmq import broker, exchange
from src.models.schemas.user.login_user_input import LoginUserInput
from src.models.schemas.user.login_user_output import LoginUserOutput
from src.domain.schemas.user.user_model import UserModel
from pydantic import BaseModel
import json
import time

app.set_broker(broker)

@app.after_startup
async def startup():
    
    token = '''

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMjE3NjY2fQ.K0Wop6jGVqHqssUwwjFA_DcoycOUINfMG9XWP1HhUGE

'''
    token = token.strip()
    
    while True:
        response = await broker.request(
            message={
                # "user_id": "3",
                "username": "mh",
            }, 
            
            # message=LoginUserInput(username="mh", password="1234"),
                        
            headers={
                "token": token,
            },

            # routing_key="auth_service.auth.login",
            # routing_key="auth_service.auth.refresh_token",
            # routing_key="auth_service.user.get.self",
            routing_key="auth_service.admin.user.get",
            
            exchange=exchange,
            timeout=10,
        )

        data: dict = json.loads(response.body.decode())
        try:
            if not data.get("status_code", None):
                response = LoginUserOutput.model_validate(data)
            else:
                response = data
                
        except:
            
            if hasattr(response, "body"):         
                response = data
                
        if isinstance(response, BaseModel):                
            print(response.model_dump())
        else:
            print(response)
            
        print(type(response))
        
        time.sleep(2)
