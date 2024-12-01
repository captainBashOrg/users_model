# python -m uvicorn main:app --reload
from pydantic import BaseModel
from fastapi import Body, HTTPException, FastAPI, Path
from typing import Annotated, List

app = FastAPI()


#users = {'1': 'Имя: Example, возраст: 18'}
users = []

class User (BaseModel):
    id:int# - номер пользователя (int)
    username:str# - имя пользователя (str)
    age:int# - возраст пользователя (int)



@app.get('/users')
async def get_users() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def post_user(user: User) -> str:
    if users:
        user.id = max(users, key=lambda usr: usr.id).id + 1
    else:
        user.id = 1
    #user.username = username
    #user.age = age
    users.append(user)
    return f'User with id {user.id} is registered.'

@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(ge=1, le=999, description='Введите user_id (целое число)', examples=10)],
                    username: Annotated[str, Path(min_length=3, max_length=15, description='Введите имя_пользователя', examples='UrbanUser')],
                    age: Annotated[int, Path(ge=18, le=120, description='Введите Ваш возраст', examples='39')]) -> str:
    try:
        users[user_id].username = username
        users[user_id].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    #return f'The user with user_id {user_id} is updated.'
    return users[user_id]

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=999, description='Введите user_id (целое число)', examples=1)]) -> User:
    try:
        return users.pop(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.get('/')
async def main() -> str:
    return 'Перейдите на страницу <a href=\"http://127./0.0.1:8000/docs\">http://127.0.0.1:8000/docs</a>'
