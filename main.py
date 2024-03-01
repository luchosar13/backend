### Library´s imports

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()

### Routers

app.include_router(products.router)

app.include_router(users.router)

app.include_router(users_db.router)

app.include_router(basic_auth_users.router)

app.include_router(jwt_auth_users.router)
### Router method for import static content

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
## async is an function of the asynchronism. the server is run while executing other functions
async def root():
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}
