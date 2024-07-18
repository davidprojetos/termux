package org.example;

public class App {
    public String getGreeting() {
        return "Olá mundo!";
    }

    public static void main(String[] args) {
        System.out.println(new App().getGreeting());
    }
}
