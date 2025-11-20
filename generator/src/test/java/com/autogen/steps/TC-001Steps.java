package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.TC-001Page;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

public class TC-001Steps {
    private final WebDriver driver;
    private final TC-001Page tc001page;

    public TC-001Steps() {
        this.driver = Hooks.getDriver();
        this.tc001page = new TC-001Page(this.driver);
    }

    @Given("Ingresar usuario \"(.*)\"")
    public void ingresarUsuario(String param1) {
        tc001page.ingresarusuarioqauserSendKeys(param1);
    }

    @When("Ingresar password \"(.*)\"")
    public void ingresarPassword(String param1) {
        tc001page.ingresarpassword1234SendKeys(param1);
    }

    @When("Presionar Ingresar")
    public void presionarIngresar() {
        tc001page.presionaringresarClick();
    }

    @Then("Validar dashboard principal")
    public void validarDashboardPrincipal() {
        Assert.assertTrue(tc001page.validardashboardprincipalIsVisible());
    }
}