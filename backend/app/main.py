from fastapi import FastAPI

app = FastAPI(title="API TecnoRepuestos S.A.")

@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido al sistema de TecnoRepuestos S.A."}