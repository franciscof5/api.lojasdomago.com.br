from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.conf.urls.static import static
from PIL import Image


global GLOBAL_VAR_X
# Create your views here.
def index(request):
    global GLOBAL_VAR_X
    GLOBAL_VAR_X = []    # Global var
    path = "/code/anuncios-controle/usados/"
    #path = static 
    dir_scan(path)

    #dd()
    return HttpResponse(GLOBAL_VAR_X)


def dir_scan(path):
    global GLOBAL_VAR_X
    
    path_trocar = "/code/anuncios-controle/"
    #text="dir_scan"
    for i in os.scandir(path):
        if i.is_file() and i.path.lower().endswith(('.jpg')) and not i.path.lower().endswith(('_lowquality.jpg')):
            #Using UNIX filesystem
            imagem_lowquality = i.path[0:-4] + "_lowquality.jpg"
            if not os.path.isfile(imagem_lowquality) :
                foo = Image.open(i.path) 
                foo = foo.resize((300,300),Image.ANTIALIAS)
                foo.save(imagem_lowquality, optimize=True, quality=75)
            
            #GLOBAL_VAR_X.append('<p>' + trocadonew + '</p>')
            #trocado = i.path
            trocado = imagem_lowquality.replace(path_trocar, "/static/")

            GLOBAL_VAR_X.append('<img src="' + trocado + '" width="200">') 
        elif i.is_dir():
            trocado = i.path.replace(path_trocar + "usados/", "")
            GLOBAL_VAR_X.append('<h3>' + trocado + '</h3>')
            dir_scan(i.path)