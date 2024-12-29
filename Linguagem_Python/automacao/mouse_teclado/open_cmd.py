import pyautogui

pyautogui.PAUSE=0.2 # pausa antes de cada comando

def open_cmd(name_app=''):
    pyautogui.press('win')
    pyautogui.typewrite('cmd') 
    pyautogui.press('enter')
    pyautogui.write(name_app)
    pyautogui.press('enter')

if __name__ == "__main__":
    open_cmd('python')