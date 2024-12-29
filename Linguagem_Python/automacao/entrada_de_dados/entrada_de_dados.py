import pyautogui
import time

time.sleep(3)  # Espera o aplicativo abrir

# Simula cliques e interações
pyautogui.click(100, 200)  # Coordenadas de um campo de texto ou botão
pyautogui.typewrite("Teste de GUI")
pyautogui.press('enter')
time.sleep(1)
pyautogui.click(200, 300)  # Outro botão
