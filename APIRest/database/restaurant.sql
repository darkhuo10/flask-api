-- Crear base de datos
DROP DATABASE IF EXISTS restaurant;
CREATE DATABASE restaurant;
USE restaurant;

-- Tabla CAMAREROS
CREATE TABLE waiters (
    username VARCHAR(30) NOT NULL PRIMARY KEY,
    legal_name VARCHAR(40) NOT NULL,
    email VARCHAR(50) NOT NULL,
    type VARCHAR(20),
    password VARCHAR(100) NOT NULL,
    state VARCHAR(20) NOT NULL,
    access_date DATE,
    blocked_date DATE,
    login_errors INTEGER,
    change_password BOOLEAN
);

-- Tabla PRODUCTOS
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    number INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    tax INT NOT NULL
);
-- Insertar datos de prueba en la tabla de CAMAREROS (waiters)
INSERT INTO waiters (username, legal_name, email type password, state , login_errors) VALUES
    ('admin', 'Nombre Apellidos', 'admin@admin.test', 'admin', '$2b$10$bmRewuyQ57fOW3v9YHQuZe8TpqUA5BBC7D864QpY/DJLXSKbP.W7i', 'active', 0)

-- Insertar datos de prueba en la tabla de PRODUCTOS (products)
INSERT INTO products (name, description, number, price, tax) VALUES
    ('Pizza Margarita', 'Pizza con tomate, queso mozzarella y albahaca', 8, 8.99, 21),
    ('Hamburguesa Clásica', 'Hamburguesa con carne de res, lechuga, tomate y cebolla', 6, 6.50, 21),
    ('Ensalada César', 'Ensalada con lechuga, pollo, croutons y salsa César', 6, 5.99, 21);
