from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"],
                responses={404:{"Message": "No encontrado"}})

products_list = ["producto 1",
                 "producto 2",
                 "producto 3"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def product(id: int):
    return products_list[id]