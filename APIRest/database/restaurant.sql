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


CREATE TABLE usuarios(
	usuario VARCHAR(100) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    perfil VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    fechaUltimoAcceso DATE,
    fechaBloqueo DATE,
    numeroAccesosErroneo INTEGER,
    debeCambiarClave BOOLEAN
);
INSERT INTO `usuarios` (`usuario`, `clave`, `perfil`,`estado`, `correo`,`numeroAccesosErroneo`,`fechaUltimoAcceso`) VALUES ('root','$2b$10$hJtLt4u0SqSf.h3S5Uuev.nu98ARhn.6SpvFCYbc1eeynJmy81cmK', 'admin', 'activo','root@pp.es', 0, '2022-03-01 00:00');


-- Insertar datos de prueba en la tabla de CAMAREROS (waiters)
INSERT INTO waiters (username, email, profile, password, state , login_errors) VALUES
    ('admin', 'admin@admin.test', 'admin', '$2b$10$bmRewuyQ57fOW3v9YHQuZe8TpqUA5BBC7D864QpY/DJLXSKbP.W7i', 'active', 0);

-- Insertar datos de prueba en la tabla de PRODUCTOS (products)
INSERT INTO products (name, description, number, price, tax) VALUES
    ('Pizza Margarita', 'Pizza con tomate, queso mozzarella y albahaca', 8, 8.99, 21),
    ('Hamburguesa Clásica', 'Hamburguesa con carne de res, lechuga, tomate y cebolla', 6, 6.50, 21),
    ('Ensalada César', 'Ensalada con lechuga, pollo, croutons y salsa César', 6, 5.99, 21);
