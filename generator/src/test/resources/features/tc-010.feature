Feature: Buscar producto destacado
  Feature generado para Buscar producto destacado

  Scenario: Buscar producto destacado
    Given Navegar a la home
    When Buscar "camiseta"
    Then Validar resultados
