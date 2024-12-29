import zipfile, os, pyautogui

def backup(folder): #
    folder = os.path.abspath(folder)
    offset=1
    
    zip_name=os.path.basename(folder)+'_'+str(offset)+'.zip'
    if os.path.exists(zip_name):
        zip_name=os.path.basename(folder)+'_'+str(offset+1)+'.zip'
        
    print("Successfully created file %s" %(zip_name))
    backupzip=zipfile.ZipFile(zip_name,'w')
    for foldername,subfolders,filenames in os.walk(folder):
        backupzip.write(foldername)
    backupzip.close()
    print("done!")
    
def clean(folder):
    confirm = pyautogui.confirm(text=f'Apagar todos os backups de {folder}?', title='Atenção!', buttons=['OK', 'Cancelar'])
    if(confirm=='OK'):
        folder = os.path.abspath(folder)
        offset=1
        while 1:
            zip_name=os.path.basename(folder)+'_'+str(offset)+'.zip'
            if os.path.exists(zip_name):
                os.remove(zip_name) #apaga
                print("Successfully removed file %s" %(zip_name))
                offset+=1
                continue
            break
        print("done")

if __name__ == "__main__":
    
    #execultar na página que deseja fazer/apagar backup

    backup(os.getcwd())
    clean(os.getcwd())