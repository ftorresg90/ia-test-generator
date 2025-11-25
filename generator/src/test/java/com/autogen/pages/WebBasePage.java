package com.autogen.pages;

import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public abstract class WebBasePage {
    protected final WebDriver driver;
    private final WebDriverWait wait;
    private static final long DEFAULT_TIMEOUT = 30;

    protected WebBasePage(WebDriver driver) {
        this(driver, DEFAULT_TIMEOUT);
    }

    protected WebBasePage(WebDriver driver, long timeoutSeconds) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds));
    }

    protected WebDriver getDriver() {
        return driver;
    }

    protected void waitUntilElementIsVisible(WebElement element) {
        wait.until(ExpectedConditions.visibilityOf(element));
    }

    protected void waitUntilElementIsVisible(By locator) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    protected void waitUntilElementIsVisibleNonThrow(WebElement element, long timeoutSeconds) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .until(ExpectedConditions.visibilityOf(element));
        } catch (Exception ignored) {
        }
    }

    protected void waitUntilElementIsVisibleNonThrow(By locator, long timeoutSeconds) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(timeoutSeconds))
                    .until(ExpectedConditions.visibilityOfElementLocated(locator));
        } catch (Exception ignored) {
        }
    }

    protected void click(WebElement element) {
        element.click();
    }

    protected void doubleClick(WebElement element) {
        new Actions(driver).doubleClick(element).perform();
    }

    protected void hover(WebElement element) {
        new Actions(driver).moveToElement(element).perform();
    }

    protected void scrollIntoView(WebElement element) {
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", element);
    }

    protected void clear(WebElement element) {
        element.clear();
    }

    protected void sendKeys(WebElement element, String text) {
        clear(element);
        element.sendKeys(text);
    }

    protected boolean isVisible(WebElement element) {
        try {
            return element.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    protected boolean isVisible(By locator) {
        try {
            return driver.findElement(locator).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    protected boolean isInvisible(WebElement element) {
        try {
            return !element.isDisplayed();
        } catch (NoSuchElementException | StaleElementReferenceException e) {
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    protected boolean isInvisible(By locator) {
        try {
            return !driver.findElement(locator).isDisplayed();
        } catch (NoSuchElementException | StaleElementReferenceException e) {
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    protected String getText(WebElement element) {
        return element.getText();
    }
}