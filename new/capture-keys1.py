import pyautogui
import cv2
import numpy as np
import time
import os

def localizar_elemento(imagem_referencia, precisao=0.8):
    # Verificar se a imagem de referência existe
    if not os.path.isfile(imagem_referencia):
        print(f"Imagem de referência não encontrada: {imagem_referencia}")
        return None

    # Fazer captura de tela
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Ler a imagem de referência
    referencia = cv2.imread(imagem_referencia, cv2.IMREAD_UNCHANGED)

    # Verificar se a imagem de referência foi carregada corretamente
    if referencia is None:
        print(f"Falha ao carregar a imagem de referência: {imagem_referencia}")
        return None

    # Fazer a correspondência de modelo
    resultado = cv2.matchTemplate(screenshot, referencia, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
    
    if max_val >= precisao:
        return max_loc, referencia.shape[:2]  # Retorna a localização e o tamanho da referência
    else:
        return None

def clicar_elemento(imagem_referencia, precisao=0.8):
    localizacao = localizar_elemento(imagem_referencia, precisao)
    if localizacao:
        (max_loc, (h, w)) = localizacao
        centro_x = max_loc[0] + w // 2
        centro_y = max_loc[1] + h // 2
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
