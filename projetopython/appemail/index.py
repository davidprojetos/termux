import smtplib
from email.message import EmailMessage

# Configurações do e-mail
email_de = "davidk1k3kk@gmail.com"
email_para = input("Digite o endereço de email de destino: ")
senha = "pfqlcemdaotxppiw"  # **Nota:** Evite hardcodar senhas no código.

# Criação do objeto EmailMessage
msg = EmailMessage()
msg.set_content(input("Digite o conteúdo: "))
msg['Subject'] = input("Digite o assunto: ")
msg['From'] = email_de
msg['To'] = email_para

# Envio do e-mail
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_de, senha)
        smtp.send_message(msg)
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")