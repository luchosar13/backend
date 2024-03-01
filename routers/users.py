## Start the server with uvicorn users:router --reload

from operator import index
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


## Create the entity User with Base Model

class User(BaseModel):
    id: int
    name: str
    lastname: str
    age: int
    url: str

users_list = [User(id= 43349590,name="lucho", lastname="sarli", age= 22, url= "linkdn.com/lucianosarli")]

router = APIRouter()

@router.get("/usersjson")
## async is an function of the asynchronism. the server is run while executing other functions
async def usersjson():
    return [{}]

@router.get("/users")
async def users():
    return users_list


# Search users using a path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Search users using a query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)


# This function search an user on users_list with the id

def search_user(id: int):  
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error!":" Usuario no encontrado"}
    

## Add user

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        ### Changed the http status in case of error
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return user

## Modify user

@router.put("/user/")
async def user(user: User):
    
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if found is False:
        return {"Error": "El usuario ingresado no existe en la base de datos"}
    else:
        return user


## Eliminate user

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            user_eliminado = users_list[index]
            del users_list[index]
            found = True
    if found is False:
        return {"Error": "El usuario ingresado no existe en la base de datos"}
    else:
        return user_eliminado