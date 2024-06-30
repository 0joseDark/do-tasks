import pyautogui
import cv2
import numpy as np
from pynput import keyboard, mouse
from datetime import datetime
import os
import time

# Nome do arquivo de log
log_file = "actions_log.txt"

# Diretório onde as imagens de referência estão armazenadas
reference_images_dir = "reference_images"

# Iniciar o ouvinte de teclado
def start_keyboard_listener():
    def on_press(key):
        try:
            if key == keyboard.Key.up:
                log_action("UP_ARROW")
            elif key == keyboard.Key.down:
                log_action("DOWN_ARROW")
            elif key == keyboard.Key.left:
                log_action("LEFT_ARROW")
            elif key == keyboard.Key.right:
                log_action("RIGHT_ARROW")
        except AttributeError:
            pass

    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    return keyboard_listener

# Iniciar o ouvinte de mouse
def start_mouse_listener():
    def on_click(x, y, button, pressed):
        if pressed:
            log_action(f"MOUSE_CLICK at ({x}, {y})")

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    return mouse_listener

# Captura de tela
def screenshot():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return img

# Procurar componente na tela usando reconhecimento de imagem
def find_component(image_path):
    template = cv2.imread(image_path, 0)
    screenshot_img = screenshot()
    screenshot_gray = cv2.cvtColor(screenshot_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        log_action(f"Component found at {max_loc}")
        return max_loc
    else:
        log_action("Component not found")
        return None

# Gravar ação no arquivo de log
def log_action(action):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}: {action}\n")

# Executar ações do arquivo de log
def execute_actions():
    with open(log_file, "r") as f:
        actions = f.readlines()

    for action in actions:
        action = action.strip()
        if "UP_ARROW" in action:
            pyautogui.press('up')
        elif "DOWN_ARROW" in action:
            pyautogui.press('down')
        elif "LEFT_ARROW" in action:
            pyautogui.press('left')
        elif "RIGHT_ARROW" in action:
            pyautogui.press('right')
        elif "MOUSE_CLICK" in action:
            coords = action.split("at (")[1].split(")")[0]
            x, y = map(int, coords.split(", "))
            pyautogui.click(x, y)
        time.sleep(0.5)

# Função principal
def main():
    # Criar diretório para imagens de referência se não existir
    if not os.path.exists(reference_images_dir):
        os.makedirs(reference_images_dir)

    # Iniciar ouvintes de teclado e mouse
    keyboard_listener = start_keyboard_listener()
    mouse_listener = start_mouse_listener()

    print("Pressione 'Esc' para sair e salvar o log.")

    try:
        while True:
            time.sleep(1)
            # Exemplo de uso: procurar por um botão na tela
            button_image = os.path.join(reference_images_dir, "button.png")
            # Salvar a tela atual como imagem de referência para o botão
            pyautogui.screenshot(button_image, region=(0, 0, 100, 100))  # Exemplo de região para captura
            # Encontrar o botão na tela
            find_component(button_image)

            # Exemplo: aguardar a tecla 'Esc' para sair
            if keyboard.is_pressed('esc'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        # Parar ouvintes de teclado e mouse
        keyboard_listener.stop()
        mouse_listener.stop()

        # Salvar ações em um arquivo de log
        with open(log_file, "a") as f:
            f.write("=== End of session ===\n")

    print("Session ended. Executing recorded actions...")
    # Executar ações gravadas
    execute_actions()

if __name__ == "__main__":
    main()
