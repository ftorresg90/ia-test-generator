package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.TC-010Page;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

public class TC-010Steps {
    private final WebDriver driver;
    private final TC-010Page tc010page;

    public TC-010Steps() {
        this.driver = Hooks.getDriver();
        this.tc010page = new TC-010Page(this.driver);
    }

    @Given("Navegar a la home")
    public void navegarALaHome() {
        tc010page.navegaralahomeClick();
    }

    @When("Buscar \"(.*)\"")
    public void buscar(String param1) {
        tc010page.buscarcamisetaSendKeys(param1);
    }

    @Then("Validar resultados")
    public void validarResultados() {
        Assert.assertTrue(tc010page.validarresultadosIsVisible());
    }
}