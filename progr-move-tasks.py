#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from Adafruit_Motor.PWM import Adafruit_DCMotor

# Definir pinos de entrada
pinos_entrada = [17, 18, 27, 22]

# Definir pinos dos motores
pino_motor1_a = 23
pino_motor1_b = 24
pino_motor2_a = 10
pino_motor2_b = 9

# Definir velocidade inicial dos motores (em porcentagem)
velocidade_motor1 = 50
velocidade_motor2 = 50

# Definir pinos de saída para a nota de movimento
pinos_saida_nota_movimento = [4, 14, 21, 20, 16, 5]

def configura_pinos():
    """
    Configurar os pinos GPIO como entrada ou saída.
    """
    # Configurar os pinos de entrada como entrada
    for pino in pinos_entrada:
        GPIO.setup(pino, GPIO.IN)

    # Configurar os pinos de saída como saída
    for pino in pinos_saida_nota_movimento:
        GPIO.setup(pino, GPIO.OUT)

def le_estado_entrada():
    """
    Ler o estado dos pinos de entrada e retornar uma lista com os valores.

    :return: Lista com os valores dos pinos de entrada (0 ou 1).
    """
    estado_entrada = []
    for pino in pinos_entrada:
        estado_entrada.append(GPIO.input(pino))
    return estado_entrada

def converte_estado_para_nota_movimento(estado_entrada):
    """
    Converter o estado de entrada em uma nota de movimento.

    :param estado_entrada: Lista com os valores dos pinos de entrada (0 ou 1).
    :return: Nota de movimento (inteiro).
    """
    nota_movimento = 0
    for i, bit in enumerate(estado_entrada):
        if bit:
            nota_movimento |= (1 << i)
    return nota_movimento

def cria_motores():
    """
    Criar objetos Adafruit_DCMotor para os motores de corrente contínua.

    :return: Objetos Adafruit_DCMotor para os motores 1 e 2.
    """
    motor1 = Adafruit_DCMotor(pin1=pino_motor1_a, pin2=pino_motor1_b, freq=2000)
    motor2 = Adafruit_DCMotor(pin1=pino_motor2_a, pin2=pino_motor2_b, freq=2000)
    return motor1, motor2

def controla_motores(motor1, motor2, nota_movimento, velocidade_motor1, velocidade_motor2):
    """
    Controlar os motores de corrente contínua com base na nota de movimento e na velocidade.

    :param motor1: Objeto Adafruit_DCMotor para o motor 1.
    :param motor2: Objeto Adafruit_DCMotor para o motor 2.
    :param nota_movimento: Nota de movimento (inteiro).
    :param velocidade_motor1: Velocidade do motor 1 (em porcentagem).
    :param velocidade_motor2: Velocidade do motor 2 (em porcentagem).
    """
    # Extrair as direções dos motores
    direcao_motor1 = (nota_movimento >> 2) & 1
    direcao_motor2 = (nota_movimento >> 3) & 1

    # Extrair a velocidade dos motores
    velocidade_motor1 = velocidade_motor1 / 100
    velocidade_motor2 = velocidade_motor2 / 100

    # Controlar o motor 1
    motor1.set_speed(velocidade_motor1)
    if direcao_motor1:
        motor1.reverse()
    else:
        motor1.forward()

    # Controlar o motor 2
    motor2.set_speed(velocidade_motor2)
    if direcao_motor2:
        motor2.reverse()
    else:
        motor2.forward()

def ajusta_velocidade_motores(velocidade_motor1
