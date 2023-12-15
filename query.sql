-- Active: 1702580722383@@127.0.0.1@3306

create database cadastro_bd;

use cad astro_bd;

CREATE TABLE idosos (
    id CHAR(36) NOT NULL DEFAULT (uuid()),
    name VARCHAR(50),
    birth DATE,
	cpf VARCHAR(14) unique,
    PRIMARY KEY (id)
)

CREATE TABLE remedios (
    id CHAR(36) NOT NULL DEFAULT (uuid()),
    name VARCHAR(30),
    isControled CHAR(3) NOT NULL DEFAULT ('nao'),
    PRIMARY KEY (id)
);

CREATE TABLE remedio_idoso (
	id CHAR(36) NOT NULL DEFAULT (uuid()),
    remedy_id CHAR(36) NOT NULL,
    elderly_id CHAR(36) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_rel_elderly FOREIGN KEY (elderly_id) REFERENCES idosos(id)
    ON DELETE CASCADE,
    CONSTRAINT fk_rel_remedy FOREIGN KEY (remedy_id) REFERENCES remedios(id)
    ON DELETE CASCADE
);
