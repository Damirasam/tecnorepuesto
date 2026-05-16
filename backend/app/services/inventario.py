
def calcular_stock_disponible(stock_actual: int, cantidad_solicitada: int) -> bool:
    if stock_actual < 0 or cantidad_solicitada < 0:
        raise ValueError("Los valores no pueden ser negativos")
    return stock_actual >= cantidad_solicitada

def calcular_total_compra(detalles_compra: list) -> float:
    total = 0.0
    for item in detalles_compra:
        if item.get("cantidad", 0) <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if item.get("costo_unitario", 0.0) < 0:
            raise ValueError("El costo no puede ser negativo")
        total += item["cantidad"] * item["costo_unitario"]
    return round(total, 2)

def calcular_total_venta(detalles_venta: list) -> float:
    total = 0.0
    for item in detalles_venta:
        if item.get("precio_unitario", 0.0) <= 0:
            raise ValueError("El precio debe ser mayor a cero")
        total += item.get("cantidad", 1) * item["precio_unitario"]
    return round(total, 2)

def verificar_alerta_stock(stock_actual: int, stock_minimo: int) -> bool:
    return stock_actual <= stock_minimo