from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.conf.urls.static import static
from PIL import Image
import json
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
    # add permission to check if user is authenticated
    #permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        #todos = Todo.objects.filter(user = request.user.id)
        #serializer = TodoSerializer(todos, many=True)
        global GLOBAL_VAR_X
        GLOBAL_VAR_X="["
        json_dir = json.dumps(path_to_json(path))
        path_to_json_without_nested(path)
        json_dir2  = GLOBAL_VAR_X;
        json_dir2 = GLOBAL_VAR_X[0:-1]+"]"
        json_object = json.loads(json_dir2)
        return Response(json_object, status=status.HTTP_200_OK)


def index(request):
    global GLOBAL_VAR_X
    
    #path = static 
    #dir_scan(path)

    #dd()
    json_dir = json.dumps(path_to_json(path))
    GLOBAL_VAR_X="["
    path_to_json_without_nested(path)
    json_dir2  = GLOBAL_VAR_X;
    json_dir2 = GLOBAL_VAR_X[0:-1]+"]"
    
    #return JsonResponse(json_dir2, safe=False)
    return HttpResponse(json_dir, content_type="application/json")

def path_to_json(path):
    d = {'name': os.path.basename(path)}
    d['path'] = path
    d['x'] = path.count('/')-3
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_json(os.path.join(path,x)) for x in os.listdir\
                         (path)]
    else:
        d['type'] = "file"
    return d

def path_to_json_without_nested(path):
    global GLOBAL_VAR_X
    if(os.path.basename(path)!=".DS_Store" and os.path.basename(path)!=".htaccess"):
        GLOBAL_VAR_X+= '{ "name": "'+os.path.basename(path)+'"'
        GLOBAL_VAR_X+=', "path": "' + path + '"'
        #GLOBAL_VAR_X+=', "x": "' + path + '"'
        nivel = str(path.count('/')-3)
        GLOBAL_VAR_X+=', "x": "' + nivel + '"'
        
        if not os.path.isdir(path):
            GLOBAL_VAR_X+=', "type": "file" },'            
        else:
            GLOBAL_VAR_X+=', "type": "directory" },'

            [path_to_json_without_nested(os.path.join(path,x)) for x in os.listdir\
                               (path)]

#print json.dumps(path_to_dict('.'))
