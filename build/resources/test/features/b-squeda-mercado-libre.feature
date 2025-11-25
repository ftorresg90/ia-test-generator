Feature: Búsqueda Mercado Libre
  Feature generado para Búsqueda Mercado Libre

  Scenario: Búsqueda Mercado Libre
    Given Navegar a Mercado Libre
    When Buscar "camiseta de futbol"
    Then Validar resultados en Mercado Libre
