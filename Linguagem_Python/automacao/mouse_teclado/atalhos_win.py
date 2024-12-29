import pyautogui
import pyperclip
#>>pip install pyperclip



'''
https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
'''
#selecionar tudo
#pyautogui.hotkey('ctrl','a')

#copiar
#pyperclip.copy('The text to be copied to the clipboard.')#pyautogui.hotkey('ctrl','c')

#colar
#pyperclip.paste()#pyautogui.hotkey('ctrl','v')

#recortar
#pyautogui.hotkey('ctrl','x')

#desfazer
#pyautogui.hotkey('ctrl','z')

#refazer
#pyautogui.hotkey('ctrl','y')

#histórico da área de transferência
#pyautogui.hotkey('win','v')

#maximizar janela
#pyautogui.press('f11')#pyautogui.hotkey('win','up')

#area de trabalho
#pyautogui.hotkey('win','d')

#trocar janela
#pyautogui.hotkey('alt','\t')

#fecha janela
#pyautogui.hotkey('alt','f4')

#deletar item
#pyautogui.hotkey('ctrl','d')#pyautogui.hotkey('delete')

#renomear item
#pyautogui.hotkey('f2')

#bloquear computador
#pyautogui.hotkey('win','l')

# Captura tela
#pyautogui.hotkey('win','prtsc')#pyautogui.hotkey('prtsc')#pyautogui.screenshot() # ver em 'captura_de_tela'

#ferramenta de captura
#pyautogui.hotkey('win','shift','s')

#zoom
#pyautogui.hotkey('ctrl','+')#pyautogui.hotkey('ctrl','-')

#explorador de arquivos
def open_explorer():
    pyautogui.hotkey('win','e')

# ...
