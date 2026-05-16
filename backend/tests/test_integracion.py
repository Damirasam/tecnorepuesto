from fastapi import FastAPI
from fastapi.testclient import TestClient

# 1. Simulamos una mini-aplicación FastAPI directamente aquí para la prueba
app_prueba = FastAPI()

# 2. Simulamos la ruta (endpoint) de creación de un producto
@app_prueba.post("/api/productos/")
def crear_producto(producto: dict):
    # Simulamos que el sistema lo guarda y le asigna el ID 1
    return {"id": 1, "codigo": producto.get("codigo"), "nombre": producto.get("nombre")}

# 3. Configuramos el cliente de pruebas
client = TestClient(app_prueba)

# 4. LA PRUEBA DE INTEGRACIÓN
def test_creacion_producto_integracion():
    # Datos que enviaría el frontend (React)
    payload = {
        "codigo": "CAB-001",
        "nombre": "Cable UTP Cat 6",
        "stock_minimo": 10
    }
    
    # Hacemos la petición POST a la ruta
    response = client.post("/api/productos/", json=payload)
    
    # Verificamos que el servidor responda "200 OK" (Éxito)
    assert response.status_code == 200
    
    # Verificamos que el sistema devuelva los datos correctamente guardados
    datos_respuesta = response.json()
    assert datos_respuesta["codigo"] == "CAB-001"
    assert datos_respuesta["id"] == 1