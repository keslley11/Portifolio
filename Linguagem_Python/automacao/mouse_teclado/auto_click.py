import pyautogui
import time

time.sleep(3)  # tempo para posicionar o cursor

# Número de cliques
for _ in range(10):
    pyautogui.click()
    time.sleep(0.1)  # Intervalo entre cliques
