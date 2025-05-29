-- Crear base de datos
DROP DATABASE IF EXISTS restaurant;
CREATE DATABASE restaurant;
USE restaurant;

-- Tabla PRODUCTOS
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    number INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    tax INT NOT NULL
);


CREATE TABLE users(
	user VARCHAR(100) NOT NULL PRIMARY KEY,
    passwd VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    activity VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    last_login DATE,
    block_date DATE,
    login_errors INTEGER,
    change_passwd BOOLEAN
);
INSERT INTO `users` (`user`, `passwd`, `role`,`activity`, `email`,`login_errors`,`last_login`) VALUES ('root','$2b$10$hJtLt4u0SqSf.h3S5Uuev.nu98ARhn.6SpvFCYbc1eeynJmy81cmK', 'admin', 'activo','root@pp.es', 0, '2022-03-01 00:00');


-- Insertar datos de prueba en la tabla de PRODUCTOS (products)
INSERT INTO products (name, description, number, price, tax) VALUES
    ('Pizza Margarita', 'Pizza con tomate, queso mozzarella y albahaca', 8, 8.99, 21),
    ('Hamburguesa Clásica', 'Hamburguesa con carne de res, lechuga, tomate y cebolla', 6, 6.50, 21),
    ('Ensalada César', 'Ensalada con lechuga, pollo, croutons y salsa César', 6, 5.99, 21);
