## Start the server with uvicorn users_db:router --reload

from operator import index
from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/userdb",
                tags=["userdb"],
                responses={status.HTTP_404_NOT_FOUND:{"Message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


# Search users using a path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# This function search an user on users_list with the id

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"Error!":" No se ha encontrado el usuario"}
    

## Add user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    #if type(search_user("email",user.email)) == User:
    #    ### Changed the http status in case of error
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    #else:
    #    users_list.append(user)

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


## Modify user

@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.update_one({"_id": ObjectId(user.id)}, {"$set": user_dict})
    except:
        return {"Error": "El usuario ingresado no existe en la base de datos"}

    return search_user("_id", ObjectId(user.id))

## Eliminate user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    print(id)

    found = db_client.users.delete_one({"_id": ObjectId(id)})

    if not found:
        return {"Error": "No se ha eliminado el usuario"}