package com.autogen.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class BusquedaMercadoLibreFiltroCamisetasPage extends WebBasePage {
    private static WebDriver driver;

    @FindBy(css = "[data-test='step-1']")
    private WebElement navegaramercadolibrehttpswwwmercadolibrecl;

    @FindBy(css = "input[id='cb1-edit'], input[name='as_word'], input[name='q']")
    private WebElement buscarelproductocamisetadefutbol;

    @FindBy(css = "ol.ui-search-layout li.ui-search-layout__item, .shops__result-card")
    private WebElement validarresultadosenmercadolibre;

    public BusquedaMercadoLibreFiltroCamisetasPage(WebDriver driver) {
        super(driver);
        BusquedaMercadoLibreFiltroCamisetasPage.driver = driver;
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

    public void buscarelproductocamisetadefutbolClick() {
        waitUntilElementIsVisible(buscarelproductocamisetadefutbol);
        click(buscarelproductocamisetadefutbol);
    }

    public void buscarelproductocamisetadefutbolSendKeys(String text) {
        waitUntilElementIsVisible(buscarelproductocamisetadefutbol);
        sendKeys(buscarelproductocamisetadefutbol, text);
    }

    public boolean buscarelproductocamisetadefutbolIsVisible() {
        waitUntilElementIsVisibleNonThrow(buscarelproductocamisetadefutbol, 5);
        return isVisible(buscarelproductocamisetadefutbol);
    }

    public String buscarelproductocamisetadefutbolGetText() {
        waitUntilElementIsVisible(buscarelproductocamisetadefutbol);
        return getText(buscarelproductocamisetadefutbol);
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

}