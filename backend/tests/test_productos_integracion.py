import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
import sqlite3

# 1. Simulamos la aplicación FastAPI
app_prueba = FastAPI()

# 2. Configuramos una base de datos SQLite "En Memoria" (se borra al terminar la prueba)
conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE productos (id INTEGER PRIMARY KEY, codigo TEXT UNIQUE, nombre TEXT, stock_minimo INTEGER)")
conn.commit()

class Producto(BaseModel):
    codigo: str
    nombre: str
    stock_minimo: int

# 3. Simulamos las rutas (Endpoints)
@app_prueba.get("/api/productos/")
def listar_productos():
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    return [{"id": r[0], "codigo": r[1], "nombre": r[2], "stock_minimo": r[3]} for r in rows]

@app_prueba.post("/api/productos/", status_code=201)
def crear_producto(producto: Producto):
    try:
        cursor.execute("INSERT INTO productos (codigo, nombre, stock_minimo) VALUES (?, ?, ?)",
                       (producto.codigo, producto.nombre, producto.stock_minimo))
        conn.commit()
        return {"id": cursor.lastrowid, "codigo": producto.codigo, "nombre": producto.nombre}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Duplicado")

@app_prueba.delete("/api/productos/{id_prod}")
def borrar_producto(id_prod: int):
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
    conn.commit()
    return {"mensaje": "Borrado lógico exitoso"}

# Configuramos el cliente de pruebas
client = TestClient(app_prueba)

# ==========================================
# LOS 5 ESCENARIOS DE PRUEBA (Para tu PDF)
# ==========================================

def test_listar_vacio():
    response = client.get("/api/productos/")
    assert response.status_code == 200
    assert response.json() == []

def test_crear_exitoso():
    payload = {"codigo": "CAB-001", "nombre": "Cable HDMI", "stock_minimo": 5}
    response = client.post("/api/productos/", json=payload)
    assert response.status_code == 201
    assert response.json()["codigo"] == "CAB-001"

def test_detectar_duplicado():
    # Intentamos crear el mismo cable HDMI otra vez
    payload = {"codigo": "CAB-001", "nombre": "Cable HDMI", "stock_minimo": 5}
    response = client.post("/api/productos/", json=payload)
    assert response.status_code == 409  # 409 significa Conflicto/Duplicado

def test_listar_despues_de_crear():
    # Creamos un producto nuevo (Mouse)
    payload = {"codigo": "CAB-002", "nombre": "Mouse", "stock_minimo": 2}
    client.post("/api/productos/", json=payload)
    response = client.get("/api/productos/")
    assert len(response.json()) > 0 # Verificamos que la lista ya no esté vacía

def test_borrado_logico():
    # Creamos un teclado
    payload = {"codigo": "CAB-003", "nombre": "Teclado", "stock_minimo": 3}
    creado = client.post("/api/productos/", json=payload)
    id_prod = creado.json()["id"]
    
    # Lo borramos
    response_del = client.delete(f"/api/productos/{id_prod}")
    assert response_del.status_code == 200
    
    # Verificamos que ya no aparezca en la lista
    response_get = client.get("/api/productos/")
    ids = [p["id"] for p in response_get.json()]
    assert id_prod not in ids