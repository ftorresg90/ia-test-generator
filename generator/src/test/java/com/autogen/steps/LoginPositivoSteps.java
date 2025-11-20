package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.LoginPositivoPage;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

public class LoginPositivoSteps {
    private final WebDriver driver;
    private final LoginPositivoPage loginpositivopage;

    public LoginPositivoSteps() {
        this.driver = Hooks.getDriver();
        this.loginpositivopage = new LoginPositivoPage(this.driver);
    }

    @Given("Ingresar usuario \"(.*)\"")
    public void ingresarUsuario(String param1) {
        loginpositivopage.ingresarusuarioqauserSendKeys(param1);
    }

    @When("Ingresar password \"(.*)\"")
    public void ingresarPassword(String param1) {
        loginpositivopage.ingresarpassword1234SendKeys(param1);
    }

    @And("Presionar Ingresar")
    public void presionarIngresar() {
        loginpositivopage.presionaringresarClick();
    }

    @Then("Validar dashboard principal")
    public void validarDashboardPrincipal() {
        Assert.assertTrue(loginpositivopage.validardashboardprincipalIsVisible());
    }
}