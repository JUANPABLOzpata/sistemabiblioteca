-- Script de creación de Base de Datos para el Sistema de Biblioteca
CREATE DATABASE IF NOT EXISTS biblioteca_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE biblioteca_db;

CREATE TABLE IF NOT EXISTS materiales (
    id INT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    autor VARCHAR(150) NULL,
    editorial VARCHAR(150) NULL,
    año_publicacion INT NULL,
    numero_paginas INT NULL,
    isbn VARCHAR(50) NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    identificacion VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    extra VARCHAR(150) NULL
);

CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_material INT NOT NULL,
    id_usuario VARCHAR(10) NOT NULL,
    fecha DATE NOT NULL,
    CONSTRAINT fk_prestamo_material
        FOREIGN KEY (id_material) REFERENCES materiales(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_prestamo_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(identificacion)
        ON DELETE CASCADE ON UPDATE CASCADE
);