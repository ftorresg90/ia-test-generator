Feature: Búsqueda Mercado Libre seleccionar registros
  Feature generado para Búsqueda Mercado Libre seleccionar registros

  Scenario: Búsqueda Mercado Libre seleccionar registros
    Given Navegar a Mercado Libre "https://www.mercadolibre.cl"
    When Buscar el producto "zapatos de futbol"
    And Validar resultados en Mercado Libre
    Then selecciono el primer registro del listado
