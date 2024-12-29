import pyautogui
import pandas as pd
import time
import pandas as pd
import os
import sys
sys.path.append('C:\\Users\\Keslley\\gitHub\\Portifolio\\Linguagem_Python')
from automacao.mouse_teclado.atalhos_win import open_explorer as explorer # cd c:/Users/Keslley/gitHub/Portifolio/Linguagem_Python

pyautogui.FAILSAFE=True
pyautogui.PAUSE=0.2 # pausa antes de cada comando

def abrir_excel():
    pyautogui.press('win')
    pyautogui.typewrite('excel') # abre excel 
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('enter') # abre nova planilha
    pyautogui.hotkey('win','up')#pyautogui.press('f11')


def clica_celula_A1():
    pass

def write_row(data):
     for index, row in data.iterrows():
        pyautogui.typewrite(str(row['Coluna1']))
        pyautogui.press('tab')
        pyautogui.typewrite(str(row['Coluna2']))
        pyautogui.press('tab')
        pyautogui.press('enter')


def save_1():
    #pyautogui.hotkey('ctrl','shift', 's')
    pyautogui.hotkey('ctrl','b')
    pyautogui.typewrite('planilha_automatizada')

    #esta parte pode ser direrente...
    pyautogui.press('\t')
    pyautogui.press('\t')
    pyautogui.press('enter') #salvar no pc
    pyautogui.press('down')
    pyautogui.press('enter') #seleciona pasta 'documentos'
    pyautogui.press('\t')
    pyautogui.press('\t')
    pyautogui.press('\t')
    pyautogui.press('\t')
    pyautogui.press('enter') #salvar

def close():
    #fecha janela
    pyautogui.hotkey('alt','f4')


def save_2(data):
    # Criação de um DataFrame e salvamento como arquivo Excel
    df = pd.DataFrame(data)

    # Diretório atual
    current_folder = os.getcwd()
    excel_file = os.path.join(current_folder, "dados_salvos.xlsx")
    df.to_excel(excel_file, index=False)

    print(f"Arquivo Excel salvo em: {excel_file}")


if __name__ == "__main__":

    # Carrega dados do CSV (arqivo exemplo de duas colunas)
    data = pd.read_csv('c:/Users/Keslley/gitHub/Portifolio/Linguagem_Python/automacao/entrada_de_dados_automatizada_em_planilhas/dados.csv')
    
    abrir_excel()
    write_row(data) #duas colunas
    save_1()
    close()
    explorer()
    #conferir arquivo criado

    save_2(data) 

    '''
    Obs:
        - caso haja janelas de excel, feche-as (pode falhar, neste caso use FAILSAFE)
        - caso exista um 'planilha_automatizada.xlsx', não irá salvar
        - rodar apenas save_2() já seria suficiente!
    '''

