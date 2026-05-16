from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def listar():
    return {"mensaje": "Ruta configurada correctamente"}