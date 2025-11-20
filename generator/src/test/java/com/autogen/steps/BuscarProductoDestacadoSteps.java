package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.BuscarProductoDestacadoPage;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

public class BuscarProductoDestacadoSteps {
    private final WebDriver driver;
    private final BuscarProductoDestacadoPage buscarproductodestacadopage;

    public BuscarProductoDestacadoSteps() {
        this.driver = Hooks.getDriver();
        this.buscarproductodestacadopage = new BuscarProductoDestacadoPage(this.driver);
    }

    @Given("Navegar a la home")
    public void navegarALaHome() {
        buscarproductodestacadopage.navegaralahomeClick();
    }

    @When("Buscar \"(.*)\"")
    public void buscar(String param1) {
        buscarproductodestacadopage.buscarcamisetaSendKeys(param1);
    }

    @Then("Validar resultados")
    public void validarResultados() {
        Assert.assertTrue(buscarproductodestacadopage.validarresultadosIsVisible());
    }
}