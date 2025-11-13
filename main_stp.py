import webbrowser
import os
import time
import sys
import threading
import shutil
import tempfile
from pathlib import Path 

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from Entities.sender import send_email_with_attachment 
from Entities.sender import FLAG_FILEPATH 
from Entities.sender import MONITOR_DIR 


HTML_FILE = 'STP.html'

PROCESS_LOCK = threading.Lock() 

def resource_path(relative_path):
   
    if getattr(sys, 'frozen', False):
      
        base_path = sys._MEIPASS
    else:
        
        base_path = Path('.')
        
    return os.path.join(base_path, relative_path)

def copy_to_temp_and_get_path(filename):
    
    source_path = resource_path(filename)
    temp_dir = tempfile.gettempdir()
    destination_path = os.path.join(temp_dir, filename)
    
    try:
        shutil.copy2(source_path, destination_path)
        print(f"[PREVIEW] Arquivo HTML copiado temporariamente para: {destination_path}")
        return destination_path
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao copiar o arquivo HTML para a pasta Temp: {e}")
        return None

class PDFHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        self.handle_file_event(event)

    def on_modified(self, event):
        self.handle_file_event(event)

    def handle_file_event(self, event):
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



def check_exit_flag_and_stop(observer):
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

    print("\n" + "="*80)
    print(f"| ** ATENÇÃO: SALVE O PDF NA SEGUINTE PASTA PARA PROCESSAMENTO AUTOMÁTICO ** |")
    print(f"| PASTA DE ENTRADA: {MONITOR_DIR.ljust(58)} |")
    print(f"| Esta janela do console deve permanecer aberta até o envio ser concluído.          |")
    print("="*80 + "\n")
    input("Precione Enter")
    
    os.makedirs(MONITOR_DIR, exist_ok=True)
    if os.path.exists(FLAG_FILEPATH):
        os.remove(FLAG_FILEPATH) 
    
    print(f"Abrindo formulário: {HTML_FILE}")

    html_filepath_stable = copy_to_temp_and_get_path(HTML_FILE)
    
    if html_filepath_stable:
        html_url = 'file:///' + html_filepath_stable.replace('\\', '/')
        webbrowser.open(html_url) 
    else:
        print("Não foi possível iniciar o formulário no navegador devido a um erro de cópia.")
        sys.exit(1)
    
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=False)
    observer.start()
  
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