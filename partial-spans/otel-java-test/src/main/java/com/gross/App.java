package com.gross;

/**
 * Hello world!
 */
public class App {
  public static void main(String[] args) {
    System.out.println("Hello World!");

    OtelProvider otelProvider = new OtelProvider();
    otelProvider.run(false);
  }
}
