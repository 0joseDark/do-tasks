# pip install pyautogui opencv-python numpy pillow

import cv2
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import os
from PIL import ImageGrab

# Função para capturar uma nova imagem
def capturar_imagem():
    messagebox.showinfo("Instruções", "Coloque o cursor do mouse na área que deseja capturar e pressione Enter.")
    root.withdraw()  # Esconde a janela principal durante a captura
    captura = pyautogui.screenshot()  # Captura a tela
    root.deiconify()  # Mostra a janela principal novamente

    # Salva a imagem capturada
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        captura.save(file_path)
        messagebox.showinfo("Sucesso", f"Imagem salva em {file_path}")

# Função para automação de GUI
def automatizar_gui():
    try:
        # Carregar a imagem do botão
        img_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if not img_path:
            return

        # Lê a imagem do botão
        template = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            messagebox.showerror("Erro", "Imagem não encontrada ou inválida.")
            return
        
        w, h = template.shape[::-1]

        # Captura a tela atual
        screenshot = ImageGrab.grab()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Faz correspondência da imagem
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Ajuste este valor conforme necessário
        loc = np.where(result >= threshold)

        # Se encontra a imagem, clica nela
        for pt in zip(*loc[::-1]):
            pyautogui.click(pt[0] + w / 2, pt[1] + h / 2)
            messagebox.showinfo("Ação", f"Imagem encontrada e clicada em {pt}")
            break
        else:
            messagebox.showinfo("Resultado", "Imagem não encontrada na tela.")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Configurar a interface gráfica
root = tk.Tk()
root.title("Automatizador de GUI")
root.geometry("300x200")

frame = tk.Frame(root)
frame.pack(pady=20)

btn_automate = tk.Button(frame, text="Automatizar GUI", command=automatizar_gui)
btn_automate.pack(pady=10)

btn_capture = tk.Button(frame, text="Capturar Imagem", command=capturar_imagem)
btn_capture.pack(pady=10)

root.mainloop()
