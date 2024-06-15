#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install RPi.GPIO

import RPi.GPIO as GPIO
import time

# Configuração de pinos
entrada_pins = [5, 6, 13, 19]  # Pinos GPIO de entrada
saida_pins = [12, 16, 20, 21, 26, 27]  # Pinos GPIO de saída

# Configuração do GPIO
GPIO.setmode(GPIO.BCM)  # Usar a numeração BCM dos pinos

# Configurar os pinos de entrada
for pin in entrada_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configurar os pinos de saída
for pin in saida_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Nome do arquivo onde os movimentos serão lidos
log_file = 'movimentos.txt'

# Função para ler o estado dos pinos de entrada
def ler_entradas():
    estados = [GPIO.input(pin) for pin in entrada_pins]
    print(f'Estados das entradas: {estados}')
    return estados

# Função para executar movimentos com base nos dados lidos
def executar_movimentos(movimentos):
    for movimento in movimentos:
        pino, estado = movimento
        GPIO.output(pino, estado)
        print(f'Pino {pino} definido para {"HIGH" if estado else "LOW"}')

# Função principal que lê o arquivo de movimentos e executa
def processar_movimentos():
    try:
        with open(log_file, 'r') as f:
            for linha in f:
                movimentos = []
                comandos = linha.strip().split(';')
                for comando in comandos:
                    pino, estado = comando.split(',')
                    pino = int(pino)
                    estado = int(estado)
                    if pino in saida_pins:
                        movimentos.append((pino, estado))
                executar_movimentos(movimentos)
                time.sleep(1)  # Espera entre cada movimento para ver as mudanças

    except FileNotFoundError:
        print("Arquivo de movimentos não encontrado.")
    except Exception as e:
        print(f"Erro ao processar movimentos: {e}")

# Executar a função principal
try:
    while True:
        entradas = ler_entradas()
        processar_movimentos()
        time.sleep(1)  # Intervalo de leitura

except KeyboardInterrupt:
    print("Execução interrompida pelo usuário.")
finally:
    GPIO.cleanup()  # Resetar a configuração dos GPIO

print("Script finalizado.")
