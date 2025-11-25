package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.BSquedaMercadoLibreSeleccionarRegistrosPage;
import com.autogen.pages.BusquedaMercadoLibreFiltroCamisetasPage;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

public class BusquedaMercadoLibreFiltroCamisetasSteps {
    private final WebDriver driver;
    private final BusquedaMercadoLibreFiltroCamisetasPage busquedamercadolibrefiltrocamisetaspage;
    private final BSquedaMercadoLibreSeleccionarRegistrosPage bsquedamercadolibreseleccionarregistrospage;

    public BusquedaMercadoLibreFiltroCamisetasSteps() {
        this.driver = Hooks.getDriver();
        this.busquedamercadolibrefiltrocamisetaspage = new BusquedaMercadoLibreFiltroCamisetasPage(this.driver);
        this.bsquedamercadolibreseleccionarregistrospage = new BSquedaMercadoLibreSeleccionarRegistrosPage(this.driver);
    }

    @Given("Navegar a Mercado Libre {string}")
    public void navegarAMercadoLibre(String url) {
        driver.get(url);
    }

    @When("Buscar el producto {string}")
    public void buscarElProducto(String producto) {
        busquedamercadolibrefiltrocamisetaspage.buscarelproductocamisetadefutbolSendKeys(producto);
    }

    @Then("Validar resultados en Mercado Libre")
    public void validarResultadosEnMercadoLibre() {
        Assert.assertTrue(busquedamercadolibrefiltrocamisetaspage.validarresultadosenmercadolibreIsVisible());
    }

    @Given("Navegar a Mercado Libre {string}")
    public void navegarAMercadoLibreHttpsWwwMercadolibreCl(String url) {
        driver.get(url);
    }

    @When("Buscar el producto {string}")
    public void buscarElProductoCamisetaDeFutbol(String producto) {
        bsquedamercadolibreseleccionarregistrospage.buscarelproductozapatosdefutbolSendKeys(producto);
    }
}