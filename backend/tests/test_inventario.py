import pytest
from app.services.inventario import (
    calcular_stock_disponible,
    calcular_total_compra,
    calcular_total_venta,
    verificar_alerta_stock
)

class TestCalcularStockDisponible:
    def test_stock_suficiente(self):
        assert calcular_stock_disponible(50, 10) is True

    def test_stock_exacto(self):
        assert calcular_stock_disponible(15, 15) is True

    def test_stock_insuficiente(self):
        assert calcular_stock_disponible(5, 10) is False

    def test_stock_cero(self):
        assert calcular_stock_disponible(0, 5) is False

    def test_cantidad_cero_siempre_disponible(self):
        assert calcular_stock_disponible(10, 0) is True

    def test_valor_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_stock_disponible(-5, 10)

    def test_cantidad_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_stock_disponible(10, -2)

class TestCalcularTotalCompra:
    def test_un_producto(self):
        detalles = [{"cantidad": 10, "costo_unitario": 2.50}]
        assert calcular_total_compra(detalles) == 25.0

    def test_multiples_productos(self):
        detalles = [
            {"cantidad": 2, "costo_unitario": 5.0},
            {"cantidad": 3, "costo_unitario": 10.0}
        ]
        assert calcular_total_compra(detalles) == 40.0

    def test_total_cero_en_lista_vacia(self):
        assert calcular_total_compra([]) == 0.0

    def test_cantidad_cero_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_total_compra([{"cantidad": 0, "costo_unitario": 5.0}])

    def test_costo_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_total_compra([{"cantidad": 5, "costo_unitario": -2.0}])

    def test_precision_decimal(self):
        detalles = [{"cantidad": 3, "costo_unitario": 2.333}]
        assert calcular_total_compra(detalles) == 7.0

class TestCalcularTotalVenta:
    def test_venta_simple(self):
        assert calcular_total_venta([{"cantidad": 1, "precio_unitario": 15.0}]) == 15.0

    def test_venta_multiples_items(self):
        detalles = [
            {"cantidad": 2, "precio_unitario": 10.0},
            {"cantidad": 1, "precio_unitario": 5.50}
        ]
        assert calcular_total_venta(detalles) == 25.50

    def test_precio_cero_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_total_venta([{"cantidad": 1, "precio_unitario": 0.0}])

class TestVerificarAlertaStock:
    def test_alerta_activa_por_debajo(self):
        assert verificar_alerta_stock(stock_actual=4, stock_minimo=5) is True

    def test_alerta_activa_igual_al_minimo(self):
        assert verificar_alerta_stock(stock_actual=10, stock_minimo=10) is True

    def test_sin_alerta(self):
        assert verificar_alerta_stock(stock_actual=20, stock_minimo=5) is False

    def test_stock_cero_genera_alerta(self):
        assert verificar_alerta_stock(stock_actual=0, stock_minimo=10) is True