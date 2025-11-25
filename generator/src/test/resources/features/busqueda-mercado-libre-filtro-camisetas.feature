Feature: Busqueda Mercado Libre filtro camisetas
  Feature generado para Busqueda Mercado Libre filtro camisetas

  Scenario: Busqueda Mercado Libre filtro camisetas
    Given Navegar a Mercado Libre "https://www.mercadolibre.cl"
    When Buscar el producto "camiseta de futbol"
    Then Validar resultados en Mercado Libre
