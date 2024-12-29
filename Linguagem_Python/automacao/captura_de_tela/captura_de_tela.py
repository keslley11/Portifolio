import pyautogui

# Captura tela inteira

def prtSc_1(): # Opção 1) salva em C:\Users\Keslley\Pictures\Screenshots
    pyautogui.hotkey('win','prtsc') 
def prtSc_2(): # Opção 2)salva na área de transferencia
    pyautogui.hotkey('prtsc') 
def prtSc_3():  # Opção 3) salva na pasta que está executando
    pyautogui.screenshot('screen.png')
def prtSc_4():
    screenshot = pyautogui.screenshot() # Opção 4) salva na pasta indicada
    screenshot.save('c:/Users/Keslley/gitHub/Portifolio/Linguagem_Python/automacao/captura_de_tela/captura.png')

# Adicionar anotações usando bibliotecas como PIL ou OpenCV (opcional)

if __name__ == "__main__":
    #prtSc_1()
    #prtSc_2()
    #prtSc_3()
    prtSc_4()