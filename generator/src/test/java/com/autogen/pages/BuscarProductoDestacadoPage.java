package com.autogen.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class BuscarProductoDestacadoPage extends WebBasePage {
    private static WebDriver driver;

    @FindBy(css = "[data-test='step-1']")
    private WebElement navegaralahome;

    @FindBy(css = "input[type='search']")
    private WebElement buscarcamiseta;

    @FindBy(css = "div[data-test='resultado-3']")
    private WebElement validarresultados;

    public BuscarProductoDestacadoPage(WebDriver driver) {
        super(driver);
        BuscarProductoDestacadoPage.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void navegaralahomeClick() {
        clickElement(navegaralahome);
    }

    public void navegaralahomeSendKeys(String text) {
        typeText(navegaralahome, text);
    }

    public boolean navegaralahomeIsVisible() {
        return isVisible(navegaralahome);
    }

    public String navegaralahomeGetText() {
        return getText(navegaralahome);
    }

    public void buscarcamisetaClick() {
        clickElement(buscarcamiseta);
    }

    public void buscarcamisetaSendKeys(String text) {
        typeText(buscarcamiseta, text);
    }

    public boolean buscarcamisetaIsVisible() {
        return isVisible(buscarcamiseta);
    }

    public String buscarcamisetaGetText() {
        return getText(buscarcamiseta);
    }

    public void validarresultadosClick() {
        clickElement(validarresultados);
    }

    public void validarresultadosSendKeys(String text) {
        typeText(validarresultados, text);
    }

    public boolean validarresultadosIsVisible() {
        return isVisible(validarresultados);
    }

    public String validarresultadosGetText() {
        return getText(validarresultados);
    }

}