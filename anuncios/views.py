from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.conf.urls.static import static
from PIL import Image
import json
import string
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.http import JsonResponse
from django.core import serializers

global GLOBAL_VAR_X

path = "/code/anuncios-controle/usados/"

class TodoListApiView(APIView):
    def get(self, request, *args, **kwargs):
        json_dir = json.dumps( path_to_json(path) )
        json_object = json.loads(json_dir)
        return Response(json_object, status=status.HTTP_200_OK)


def index(request):
    json_dir = json.dumps( path_to_json(path) )
    return HttpResponse(json_dir, content_type="application/json")

def path_to_json(path):
    if os.path.basename(path)!=".DS_Store":
        nivel = path.count('/')-3
        filename = os.path.basename(path)
        product_name = filename.split("R$")[0].strip()
        d = {'name': product_name}
        #if os.path.basename(path).find("R$"):
        if nivel==1:
            price = 0
            tem_preco_definido = len(filename.split("R$"))
            if tem_preco_definido>1:
                price = filename.split("R$")[1].split("|")[0].strip()
                #price = price[1]

            local="local indefindo"
            tem_local_definido = len(filename.split("Local="))
            if tem_local_definido>1:
                local=filename.split("Local=")[1].split("|")[0].strip()
            
            category="categoria indefindo"
            tem_category_definido = len(filename.split("Cat="))
            if tem_local_definido>1:
                category=filename.split("Cat=")[1].strip()
            
            d['price'] = price
            d['local'] = local
            d['cat'] = category
        d['path'] = path
        d['x'] = nivel
        if os.path.isdir(path):
            d['type'] = "directory"
            #usar o reverso só nas fotos do produto, não na listagem
            d['pictures'] = [path_to_json(os.path.join(path,x)) for x in  sorted(os.listdir(path), key=str.casefold ) if not x.startswith('.') ]
        else:
            d['type'] = "file"
    else:
        d = {'name': 'nps'}
    return d

def renderHTML(refer):
    global GLOBAL_VAR_X
    GLOBAL_VAR_X="["

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


    return HttpResponse(json_object)
#print json.dumps(path_to_dict('.'))
