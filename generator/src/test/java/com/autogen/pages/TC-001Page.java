package com.autogen.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class TC-001Page extends WebBasePage {
    private static WebDriver driver;

    @FindBy(id = "username")
    private WebElement ingresarusuarioqauser;

    @FindBy(id = "password")
    private WebElement ingresarpassword1234;

    @FindBy(css = "[data-test='step-3']")
    private WebElement presionaringresar;

    @FindBy(css = "div[data-test='resultado-4']")
    private WebElement validardashboardprincipal;

    public TC-001Page(WebDriver driver) {
        super(driver);
        TC-001Page.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void ingresarusuarioqauserClick() {
        clickElement(ingresarusuarioqauser);
    }

    public void ingresarusuarioqauserSendKeys(String text) {
        typeText(ingresarusuarioqauser, text);
    }

    public boolean ingresarusuarioqauserIsVisible() {
        return isVisible(ingresarusuarioqauser);
    }

    public String ingresarusuarioqauserGetText() {
        return getText(ingresarusuarioqauser);
    }

    public void ingresarpassword1234Click() {
        clickElement(ingresarpassword1234);
    }

    public void ingresarpassword1234SendKeys(String text) {
        typeText(ingresarpassword1234, text);
    }

    public boolean ingresarpassword1234IsVisible() {
        return isVisible(ingresarpassword1234);
    }

    public String ingresarpassword1234GetText() {
        return getText(ingresarpassword1234);
    }

    public void presionaringresarClick() {
        clickElement(presionaringresar);
    }

    public void presionaringresarSendKeys(String text) {
        typeText(presionaringresar, text);
    }

    public boolean presionaringresarIsVisible() {
        return isVisible(presionaringresar);
    }

    public String presionaringresarGetText() {
        return getText(presionaringresar);
    }

    public void validardashboardprincipalClick() {
        clickElement(validardashboardprincipal);
    }

    public void validardashboardprincipalSendKeys(String text) {
        typeText(validardashboardprincipal, text);
    }

    public boolean validardashboardprincipalIsVisible() {
        return isVisible(validardashboardprincipal);
    }

    public String validardashboardprincipalGetText() {
        return getText(validardashboardprincipal);
    }

}
