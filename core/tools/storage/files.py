import os
from os import path
import shutil
from django.conf import settings

print(settings.BASE_DIR)

# folder_path = "/Users/manuel.cruz/Documents/github/backendMedimas/uploads/"
folder_path = settings.BASE_DIR

def delFolderContent():
    print(folder_path)
    # if path.exists(folder_path):
    #     for file_object in os.listdir(folder_path): 
    #         file_object_path = os.path.join(folder_path, file_object) 
    #     if os.path.isfile(file_object_path): 
    #         os.unlink(file_object_path) 
    #     else: 
    #         shutil.rmtree(file_object_path)
