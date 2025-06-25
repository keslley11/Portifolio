import pyautogui
import time

pyautogui.PAUSE=1 # pausa antes de cada comando

time.sleep(3)  # Abrir e-mail Outlook e maximizar janela 


pyautogui.click(130, 130)  # Clique no botão "Compor"
pyautogui.typewrite('destinatario@example.com')
pyautogui.press('tab')
pyautogui.press('tab') #pula cópia oculta (Cco)
pyautogui.press('tab') #pula cópia (Cc)
pyautogui.typewrite('Assunto do E-mail')
pyautogui.press('tab')
pyautogui.typewrite('Corpo do e-mail.')
#pyautogui.hotkey('ctrl', 'enter')  # Envia o e-mail
