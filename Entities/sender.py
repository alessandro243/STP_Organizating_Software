import os
import smtplib 
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


SMTP_SERVER = 'smtp.gmail.com' 
SMTP_PORT = 587
SENDER_EMAIL = 'alex.alessandro6666@gmail.com' 
SENDER_PASSWORD = 'wtwz pmkb prxs emqv' 
RECEIVER_EMAIL = 'alex.alessandro342@gmail.com'


MONITOR_DIR = r'C:\STP_INPUT'
FLAG_FILENAME = 'SAIR.txt'
FLAG_FILEPATH = os.path.join(MONITOR_DIR, FLAG_FILENAME)

def create_exit_flag():
    
    try:
       
        os.makedirs(MONITOR_DIR, exist_ok=True) 
        with open(FLAG_FILEPATH, 'w') as f:
            f.write(f"Monitoramento encerrado em {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[FLAG] Arquivo de encerramento '{FLAG_FILENAME}' criado em {MONITOR_DIR}.")
    except Exception as e:
        print(f"[ERRO] Falha ao criar o arquivo de flag: {e}")

def send_email_with_attachment(filepath, subject_prefix="STP - Chamado Concluído"):

    filename = os.path.basename(filepath)
    print(f"[SMTP] Preparando email para envio do arquivo: {filename}")

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    
    cleaned_filename = filename.rsplit('.', 1)[0]
    msg['Subject'] = f"{subject_prefix}: {cleaned_filename}"
    body = f"O checklist '{filename}' foi preenchido e está anexo.\n\nPor favor, arquivar e iniciar o próximo passo do processo."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(filepath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado em {filepath}. Não será enviado.")
        return False
    except Exception as e:
        print(f"[ERRO] Falha ao anexar o arquivo: {e}")
        return False

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"[SMTP] ✅ Email enviado com sucesso para {RECEIVER_EMAIL}!")
        
        try:
            os.remove(filepath)
            print(f"[CLEANUP] ✅ Arquivo '{filename}' EXCLUÍDO com sucesso!")
        except Exception as e:
            print(f"[ERRO] ❌ Falha ao excluir o arquivo: {e}. O arquivo permaneceu na pasta INPUT.")
        
        create_exit_flag()
        
        return True
    
    except Exception as e:
        print(f"[ERRO] ❌ Falha crítica no envio SMTP. Verifique as credenciais ou a Senha de App: {e}")
        return False

if __name__ == '__main__':
    print("Módulo de envio SMTP carregado.")