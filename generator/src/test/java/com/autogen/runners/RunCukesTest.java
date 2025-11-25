package com.autogen.runners;

import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
        features = "generator/src/test/resources/features",
        glue = {"com.autogen.steps", "com.autogen.hooks"},
        plugin = "pretty",
        monochrome = true
)
public class RunCukesTest {
}