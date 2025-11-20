Feature: Login positivo
  Feature generado para Login positivo

  @smoke @login
  Scenario: Login positivo
    Given Ingresar usuario "qa_user"
    When Ingresar password "1234"
    When Presionar Ingresar
    Then Validar dashboard principal
