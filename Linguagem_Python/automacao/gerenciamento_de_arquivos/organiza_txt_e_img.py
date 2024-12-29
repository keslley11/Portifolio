import os
import shutil

# Organiza arquivos por extensão
'''
source_dir = 'C:\\Users\\Keslley\\Downloads'
dest_dir = 'C:\\Users\\Keslley\\Downloads\\Organizados'
'''

'''
'C:\\Users\\Keslley\\Desktop'
'''

source_dir = os.path.join(os.path.expanduser("~"), "Desktop") 
dest_dir = os.path.join(source_dir, "Organizados")

os.makedirs(os.path.join(dest_dir, 'Textos'), exist_ok=True) #cria as pastas
os.makedirs(os.path.join(dest_dir, 'Imagens'), exist_ok=True) #cria as pastas



for file_name in os.listdir(source_dir):

    try:
        if file_name.endswith('.txt'):
            file_name_= file_name.replace(" ", "_")
            os.rename(os.path.join(source_dir, file_name), os.path.join(source_dir, file_name_)) # renomeia removendo espaços
            shutil.move(os.path.join(source_dir, file_name_), os.path.join(dest_dir, 'Textos'))
        
        elif file_name.endswith(('.jpg', '.jpeg', '.png')):
            file_name_= file_name.replace(" ", "_")
            os.rename(os.path.join(source_dir, file_name), os.path.join(source_dir, file_name_)) # renomeia removendo espaços
            shutil.move(os.path.join(source_dir, file_name_), os.path.join(dest_dir, 'Imagens'))
            
    except Exception as e:
        # Exibe o erro e continua com o próximo arquivo
        print(f"Erro ao processar o arquivo '{file_name}': {e}")
        
print("Done!")
