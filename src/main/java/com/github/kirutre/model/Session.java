package com.github.kirutre.model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;
import com.github.kirutre.utils.ConfigReader;

public class Session {
    private static final ConfigReader dbData = new ConfigReader();

    public void test() throws ClassNotFoundException {
        Connection connection = null;
        Statement statement = null;
        ResultSet resultSet = null;

        try {
            Class.forName("org.mariadb.jdbc.Driver");

            connection = connectToDb();
            statement = connection.createStatement();

            String querry = "SELECT id, name FROM student";

            resultSet = statement.executeQuery(querry);

            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String name = resultSet.getString("name");

                System.out.println(id + "," + name);
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            try {
                if (resultSet != null) resultSet.close();
                if (statement != null) statement.close();
                if (connection != null) connection.close();

                System.out.println("Connection closed");
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    private Connection connectToDb() throws SQLException {
        return DriverManager.getConnection(dbData.getProperties().get("url"), dbData.getProperties().get("user"),
                dbData.getProperties().get("password"));
    }

    public static void main(String[] args) throws ClassNotFoundException {
        new Session().test();
    }
}
