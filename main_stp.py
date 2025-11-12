import webbrowser
import os
import time
import sys
import threading
import shutil # NOVO: Para copiar arquivos
import tempfile # NOVO: Para obter o caminho temporário do sistema
from pathlib import Path 
# Bibliotecas do monitoramento:
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# Importamos as funções e variáveis do sender (caminho fixo e flag)
from sender import send_email_with_attachment 
from sender import FLAG_FILEPATH 
from sender import MONITOR_DIR 

# --- CONFIGURAÇÕES FIXAS ---
HTML_FILE = 'STP.html'

# Variável de trava para evitar que múltiplos eventos de arquivo processem o mesmo PDF
PROCESS_LOCK = threading.Lock() 

# FUNÇÃO DE SUPORTE 1: CRÍTICA PARA ARQUIVOS EMPACOTADOS PELO PYINSTALLER
def resource_path(relative_path):
    """
    Obtém o caminho absoluto para o recurso, compatível com o PyInstaller (onefile).
    Acessa arquivos dentro do diretório temporário _MEIPASS.
    """
    if getattr(sys, 'frozen', False):
        # Caminho dentro do executável temporário
        base_path = sys._MEIPASS
    else:
        # Caminho no ambiente de desenvolvimento Python
        base_path = Path('.')
        
    return os.path.join(base_path, relative_path)

# FUNÇÃO DE SUPORTE 2: COPIA O ARQUIVO PARA UM LOCAL ESTÁVEL QUE O NAVEGADOR ACEITA
def copy_to_temp_and_get_path(filename):
    """
    Copia o arquivo do local interno do EXE (_MEIPASS) para a pasta Temp 
    padrão do Windows, garantindo que o navegador não bloqueie o acesso.
    """
    # 1. Obtém o caminho do arquivo dentro do executável
    source_path = resource_path(filename)
    
    # 2. Obtém o diretório temporário do sistema (confiável)
    temp_dir = tempfile.gettempdir()
    
    # 3. Define o caminho final do arquivo na pasta Temp
    destination_path = os.path.join(temp_dir, filename)
    
    try:
        # 4. Copia o arquivo (usamos shutil.copy2 para preservar metadados)
        shutil.copy2(source_path, destination_path)
        print(f"[PREVIEW] Arquivo HTML copiado temporariamente para: {destination_path}")
        return destination_path
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao copiar o arquivo HTML para a pasta Temp: {e}")
        return None


# 1. FUNÇÃO DE MONITORAMENTO (Apenas detecta PDFs e chama o sender)
class PDFHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        self.handle_file_event(event)

    def on_modified(self, event):
        self.handle_file_event(event)

    def handle_file_event(self, event):
        # Ignora diretórios e a flag de saída
        if event.is_directory or os.path.basename(event.src_path) == os.path.basename(FLAG_FILEPATH):
             return

        filepath = event.src_path
        filename = os.path.basename(filepath)

        if filepath.lower().endswith('.pdf'):
            
            with PROCESS_LOCK:
                
                if not os.path.exists(filepath):
                    print(f"[PROCESSAMENTO] Arquivo {filename} já foi processado e removido. Ignorando evento duplicado.")
                    return
                
                print(f"Novo PDF detectado: {filename}. Aguardando liberação do arquivo (2s)...")
                time.sleep(2) 
                
                success = send_email_with_attachment(filepath)
                
                if not success:
                    print(f"[PROCESSAMENTO] Falha no envio do arquivo {filename}. Ele permanece na pasta {MONITOR_DIR} para revisão.")


# Função que verifica a existência da flag a cada loop
def check_exit_flag_and_stop(observer):
    """Verifica se o arquivo SAIR.txt existe e interrompe o observer se for o caso."""
    if os.path.exists(FLAG_FILEPATH):
        print("\n[ENCERRAMENTO] Arquivo SAIR.txt detectado. Parando monitoramento...")
        observer.stop()
        try:
            os.remove(FLAG_FILEPATH) 
        except Exception as e:
            print(f"[ERRO] Falha ao remover a flag de saída: {e}")
        return True
    return False


if __name__ == '__main__':

    # 3. MENSAGEM PROEMINENTE PARA O USUÁRIO
    print("\n" + "="*80)
    print(f"| ** ATENÇÃO: SALVE O PDF NA SEGUINTE PASTA PARA PROCESSAMENTO AUTOMÁTICO ** |")
    print(f"| PASTA DE ENTRADA: {MONITOR_DIR.ljust(58)} |")
    print(f"| Esta janela do console deve permanecer aberta até o envio ser concluído.          |")
    print("="*80 + "\n")
    input("Precione Enter")
    
    # 0. Limpeza e Criação Inicial
    os.makedirs(MONITOR_DIR, exist_ok=True)
    if os.path.exists(FLAG_FILEPATH):
        os.remove(FLAG_FILEPATH) 
    
    # 1. ABRE O FORMULÁRIO NO NAVEGADOR
    print(f"Abrindo formulário: {HTML_FILE}")
    
    # 1. COPIA O HTML PARA A PASTA TEMP DO SISTEMA E OBTÉM O CAMINHO ESTÁVEL
    html_filepath_stable = copy_to_temp_and_get_path(HTML_FILE)
    
    if html_filepath_stable:
        # 2. Converte o caminho estável para uma URL que o navegador confia
        html_url = 'file:///' + html_filepath_stable.replace('\\', '/')
        webbrowser.open(html_url) 
    else:
        print("Não foi possível iniciar o formulário no navegador devido a um erro de cópia.")
        sys.exit(1)
    
    # 2. INICIA A VIGILÂNCIA
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=False)
    observer.start()
        
    # 4. LOOP PRINCIPAL QUE VERIFICA A FLAG A CADA SEGUNDO
    try:
        while observer.is_alive():
            time.sleep(1)
            if check_exit_flag_and_stop(observer):
                break
    
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    print("\nMonitoramento encerrado e programa finalizado.")
    sys.exit(0)