from datetime import date
import pytest
from app.validador import ValidadorDeAvistamiento


class RelojFijoStub:
    """Doble de prueba (Stub) que devuelve siempre la fecha fija 2026-10-21."""
    def __init__(self, fecha_fija: date):
        self.fecha_fija = fecha_fija

    def hoy(self) -> date:
        return self.fecha_fija


# Caso 1: Límite inferior inválido de especie (2 caracteres)
def test_validar_especie_con_2_caracteres_en_limite_inferior_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act & Assert
    with pytest.raises(ValueError, match="especie"):
        validador.validar(especie="Co", lugar="Bogotá", fecha="2026-10-21", observador="Ana")


# Caso 2: Límite inferior válido de especie (3 caracteres)
def test_validar_especie_con_3_caracteres_en_limite_inferior_es_valido():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act
    resultado = validador.validar(especie="Ave", lugar="Bogotá", fecha="2026-10-21", observador="Ana")

    # Assert
    assert resultado is None


# Caso 3: Valor representativo válido de especie (7 caracteres)
def test_validar_especie_con_longitud_representativa_valida_pasa():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act
    resultado = validador.validar(especie="Colibrí", lugar="Bogotá", fecha="2026-10-21", observador="Ana")

    # Assert
    assert resultado is None


# Caso 4: Límite superior válido de especie (50 caracteres)
def test_validar_especie_con_50_caracteres_en_limite_superior_es_valido():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))
    especie_50 = "A" * 50

    # Act
    resultado = validador.validar(especie=especie_50, lugar="Bogotá", fecha="2026-10-21", observador="Ana")

    # Assert
    assert resultado is None


# Caso 5: Límite superior inválido de especie (51 caracteres)
def test_validar_especie_con_51_caracteres_en_limite_superior_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))
    especie_51 = "A" * 51

    # Act & Assert
    with pytest.raises(ValueError, match="especie"):
        validador.validar(especie=especie_51, lugar="Bogotá", fecha="2026-10-21", observador="Ana")


# Caso 6: Límite válido de fecha (Hoy)
def test_validar_fecha_igual_a_hoy_en_limite_temporal_es_valido():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act
    resultado = validador.validar(especie="Colibrí", lugar="Bogotá", fecha="2026-10-21", observador="Ana")

    # Assert
    assert resultado is None


# Caso 7: Límite inválido de fecha (Mañana)
def test_validar_fecha_de_manana_posterior_a_hoy_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act & Assert
    with pytest.raises(ValueError, match="fecha"):
        validador.validar(especie="Colibrí", lugar="Bogotá", fecha="2026-10-22", observador="Ana")


# Caso 8: Partición inválida de formato de fecha
def test_validar_fecha_con_formato_distinto_a_aaaa_mm_dd_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act & Assert
    with pytest.raises(ValueError, match="fecha"):
        validador.validar(especie="Colibrí", lugar="Bogotá", fecha="21-10-2026", observador="Ana")


# Caso 9: Partición inválida de lugar vacío
def test_validar_lugar_con_solo_espacios_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act & Assert
    with pytest.raises(ValueError, match="lugar"):
        validador.validar(especie="Colibrí", lugar="   ", fecha="2026-10-21", observador="Ana")


# Caso 10: Partición inválida de observador vacío
def test_validar_observador_vacio_lanza_error():
    # Arrange
    validador = ValidadorDeAvistamiento(reloj=RelojFijoStub(date(2026, 10, 21)))

    # Act & Assert
    with pytest.raises(ValueError, match="observador"):
        validador.validar(especie="Colibrí", lugar="Bogotá", fecha="2026-10-21", observador="")