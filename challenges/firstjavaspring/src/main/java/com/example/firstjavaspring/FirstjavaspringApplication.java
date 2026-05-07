package com.example.firstjavaspring;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class FirstjavaspringApplication {

	public static void main(String[] args) {
		SpringApplication.run(FirstjavaspringApplication.class, args);
	}

	@GetMapping("/hello")
	public String sayHello() {
		return "Hello, World! from java 21";
	}

}
