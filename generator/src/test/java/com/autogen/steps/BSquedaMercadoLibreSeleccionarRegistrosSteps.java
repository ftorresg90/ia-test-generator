package com.autogen.steps;

import com.autogen.hooks.Hooks;
import com.autogen.pages.BSquedaMercadoLibreSeleccionarRegistrosPage;
import io.cucumber.java.en.*;
import org.openqa.selenium.WebDriver;

public class BSquedaMercadoLibreSeleccionarRegistrosSteps {
    private final WebDriver driver;
    private final BSquedaMercadoLibreSeleccionarRegistrosPage bsquedamercadolibreseleccionarregistrospage;

    public BSquedaMercadoLibreSeleccionarRegistrosSteps() {
        this.driver = Hooks.getDriver();
        this.bsquedamercadolibreseleccionarregistrospage = new BSquedaMercadoLibreSeleccionarRegistrosPage(this.driver);
    }

    @Then("selecciono el primer registro del listado")
    public void seleccionoElPrimerRegistroDelListado() {
        bsquedamercadolibreseleccionarregistrospage.seleccionoelprimerregistrodellistadoClick();
    }
}