package com.autogen.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class BSquedaMercadoLibreSeleccionarRegistrosPage extends WebBasePage {
    private static WebDriver driver;

    @FindBy(css = "[data-test='step-1']")
    private WebElement navegaramercadolibrehttpswwwmercadolibrecl;

    @FindBy(css = "input[id='cb1-edit'], input[name='as_word'], input[name='q']")
    private WebElement buscarelproductozapatosdefutbol;

    @FindBy(css = "ol.ui-search-layout li.ui-search-layout__item, .shops__result-card")
    private WebElement validarresultadosenmercadolibre;

    @FindBy(css = "[data-test='step-4']")
    private WebElement seleccionoelprimerregistrodellistado;

    public BSquedaMercadoLibreSeleccionarRegistrosPage(WebDriver driver) {
        super(driver);
        BSquedaMercadoLibreSeleccionarRegistrosPage.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void navegaramercadolibrehttpswwwmercadolibreclClick() {
        waitUntilElementIsVisible(navegaramercadolibrehttpswwwmercadolibrecl);
        click(navegaramercadolibrehttpswwwmercadolibrecl);
    }

    public void navegaramercadolibrehttpswwwmercadolibreclSendKeys(String text) {
        waitUntilElementIsVisible(navegaramercadolibrehttpswwwmercadolibrecl);
        sendKeys(navegaramercadolibrehttpswwwmercadolibrecl, text);
    }

    public boolean navegaramercadolibrehttpswwwmercadolibreclIsVisible() {
        waitUntilElementIsVisibleNonThrow(navegaramercadolibrehttpswwwmercadolibrecl, 5);
        return isVisible(navegaramercadolibrehttpswwwmercadolibrecl);
    }

    public String navegaramercadolibrehttpswwwmercadolibreclGetText() {
        waitUntilElementIsVisible(navegaramercadolibrehttpswwwmercadolibrecl);
        return getText(navegaramercadolibrehttpswwwmercadolibrecl);
    }

    public void buscarelproductozapatosdefutbolClick() {
        waitUntilElementIsVisible(buscarelproductozapatosdefutbol);
        click(buscarelproductozapatosdefutbol);
    }

    public void buscarelproductozapatosdefutbolSendKeys(String text) {
        waitUntilElementIsVisible(buscarelproductozapatosdefutbol);
        sendKeys(buscarelproductozapatosdefutbol, text);
    }

    public boolean buscarelproductozapatosdefutbolIsVisible() {
        waitUntilElementIsVisibleNonThrow(buscarelproductozapatosdefutbol, 5);
        return isVisible(buscarelproductozapatosdefutbol);
    }

    public String buscarelproductozapatosdefutbolGetText() {
        waitUntilElementIsVisible(buscarelproductozapatosdefutbol);
        return getText(buscarelproductozapatosdefutbol);
    }

    public void validarresultadosenmercadolibreClick() {
        waitUntilElementIsVisible(validarresultadosenmercadolibre);
        click(validarresultadosenmercadolibre);
    }

    public void validarresultadosenmercadolibreSendKeys(String text) {
        waitUntilElementIsVisible(validarresultadosenmercadolibre);
        sendKeys(validarresultadosenmercadolibre, text);
    }

    public boolean validarresultadosenmercadolibreIsVisible() {
        waitUntilElementIsVisibleNonThrow(validarresultadosenmercadolibre, 5);
        return isVisible(validarresultadosenmercadolibre);
    }

    public String validarresultadosenmercadolibreGetText() {
        waitUntilElementIsVisible(validarresultadosenmercadolibre);
        return getText(validarresultadosenmercadolibre);
    }

    public void seleccionoelprimerregistrodellistadoClick() {
        waitUntilElementIsVisible(seleccionoelprimerregistrodellistado);
        click(seleccionoelprimerregistrodellistado);
    }

    public void seleccionoelprimerregistrodellistadoSendKeys(String text) {
        waitUntilElementIsVisible(seleccionoelprimerregistrodellistado);
        sendKeys(seleccionoelprimerregistrodellistado, text);
    }

    public boolean seleccionoelprimerregistrodellistadoIsVisible() {
        waitUntilElementIsVisibleNonThrow(seleccionoelprimerregistrodellistado, 5);
        return isVisible(seleccionoelprimerregistrodellistado);
    }

    public String seleccionoelprimerregistrodellistadoGetText() {
        waitUntilElementIsVisible(seleccionoelprimerregistrodellistado);
        return getText(seleccionoelprimerregistrodellistado);
    }

}