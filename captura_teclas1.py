#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install keyboard
import keyboard
import time

# Nome do arquivo onde os movimentos serão registrados
log_file = 'movimentos.txt'

# Função para registrar um evento de tecla
def registrar_movimento(event):
    # Abrir o arquivo no modo de append (para adicionar novos registros)
    with open(log_file, 'a') as f:
        # Gravar a tecla pressionada e o timestamp
        f.write(f'{event.name},{time.time()}\n')
    print(f'Tecla pressionada: {event.name}')

# Lista das teclas que queremos detectar
teclas = ['up', 'down', 'left', 'right', 'page up', 'page down']

# Adicionar ganchos para as teclas específicas
for tecla in teclas:
    keyboard.on_press_key(tecla, registrar_movimento)

# Informar o usuário sobre o início da captura
print("Captura de teclas iniciada. Pressione ESC para sair.")

# Loop principal que mantém o script rodando
try:
    keyboard.wait('esc')  # Espera até que a tecla 'esc' seja pressionada para sair
except KeyboardInterrupt:
    print("Captura interrompida pelo usuário.")

# Informar o usuário sobre o fim da captura
print("Captura de teclas finalizada.")
