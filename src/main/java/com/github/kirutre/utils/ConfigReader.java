package com.github.kirutre.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Map;
import java.util.Properties;

public class ConfigReader {
    private static final String CONFIG_FILE = "config.properties";

    public Map<String, String> getProperties() {
        var properties = new Properties();

        try (InputStream fis = getClass().getClassLoader().getResourceAsStream(CONFIG_FILE)) {
            return loadFile(properties, fis);
        } catch (IOException e) {
            e.printStackTrace();

            return Map.of();
        }
    }

    private Map<String, String> loadFile(Properties properties, InputStream fis) throws IOException {
        properties.load(fis);

        var dbUrl = properties.getProperty("db.url");
        var dbUser = properties.getProperty("db.user");
        var dbPassword = properties.getProperty("db.password");

        if (dbUrl != null && dbUser != null && dbPassword != null) {
            return Map.of("url", dbUrl, "user", dbUser, "password", dbPassword);
        }

        System.err.println("One or more properties not found");

        return Map.of();
    }
}
