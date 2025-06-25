import win32com.client as win32
import pandas as pd
import pyautogui


#integração com o outlook
outlook = win32.Dispatch('outlook.application')

def send_email(contato):
    #novo email
    email = outlook.CreateItem(0)

    #informações do email
    email.To =   contato["Email"]   # "destinatário"
    email.Subject =  "Subject - Email from excel"   # "Assunto"
    email.HTMLBody = f"""
    
    <p>Good morning {contato["Nome"] },</p>
    <br>
    <br>

    <p>text line 1  <br>
    text line 2 </p>

    <p>Sincerely,
    <br>Python Code Test</p>
    """     #formatação HTML
    email.Attachments.Add("C:/Users/Keslley/gitHub/Portifolio/Linguagem_Python/automacao/enviar_email/outlook.jpg")
    #enviar email
    email.Send()
    print('Email enviado!')


def listar_emails():
    # Caminho do arquivo Excel
    caminho_arquivo = 'contatos.xlsx'

    # Lê o arquivo Excel (é necessário que ele tenha as colunas 'Nome' e 'Email')
    df = pd.read_excel(caminho_arquivo)

    # Converte o DataFrame em uma lista de dicionários
    global lista_contatos
    lista_contatos = df.to_dict(orient='records')

    # Exibe a lista
    for contato in lista_contatos:
        print(contato)
        
def main():
    listar_emails()
    
    for contato in lista_contatos:
        send_email(contato)

    print("Done!")
    
confirm = pyautogui.confirm(text='Check the contact spreadsheet, email text and updated post path!', title='Do you wanna cotinue?', buttons=['OK', 'Cancel'])
if confirm=="OK":
    print(confirm)
    main()
    
else:
    print("exit!")

