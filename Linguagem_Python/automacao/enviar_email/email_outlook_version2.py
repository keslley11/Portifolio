import win32com.client as win32

#integração com o outlook
outlook = win32.Dispatch('outlook.application')

#novo email
email = outlook.CreateItem(0)

#informações do email
email.To =   "keslley.ramos@ufu.br"   # "destinatário"
email.Subject =  "Assunto - Email teste"   # "Assunto"
email.HTMLBody = """
<p>Olá,</p>  
<p>Corpo do email teste</p>
<p>Atenciosamente,<br>Código Python</p>
"""     #formatação HTML

#enviar email
email.Send()
print('Email enviado!')
