# python.exe -m pip install --upgrade pip
# pip install pyautogui opencv-python numpy
# pyautogui.screenshot('caminho/para/imagem.png')

import pyautogui
import cv2
import numpy as np
import time

def localizar_elemento(imagem_referencia, precisao=0.8):
    # Fazer captura de tela
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Ler a imagem de referência
    referencia = cv2.imread(imagem_referencia, cv2.IMREAD_UNCHANGED)
    
    # Fazer a correspondência de modelo
    resultado = cv2.matchTemplate(screenshot, referencia, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
    
    if max_val >= precisao:
        return max_loc
    else:
        return None

def clicar_elemento(imagem_referencia, precisao=0.8):
    localizacao = localizar_elemento(imagem_referencia, precisao)
    if localizacao:
        centro_x = localizacao[0] + referencia.shape[1] // 2
        centro_y = localizacao[1] + referencia.shape[0] // 2
        pyautogui.click(centro_x, centro_y)
        return True
    else:
        print(f"Elemento {imagem_referencia} não encontrado.")
        return False

def escrever_texto(texto):
    pyautogui.typewrite(texto)

def exemplo_uso():
    # Esperar um pouco antes de começar
    time.sleep(3)
    
    # Clicar em um ícone ou botão usando uma imagem de referência
    clicar_elemento("imagens/botao_exemplo.png")
    
    # Escrever texto em um campo de texto
    escrever_texto("Texto de exemplo")

if __name__ == "__main__":
    exemplo_uso()
