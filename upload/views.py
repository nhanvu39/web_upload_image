from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from upload.forms import NameForm, UploadFileForm
from django.contrib import messages
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.template import loader
import threading
import gzip
import gzip as gzip_module
# import cv2
import os
import pathlib
import imghdr
# import filetype
import base64
##
# Create your views here.


url_img ='upload/images/'
def upload_img(request):
    if request.method == 'POST':
        print('haha')
       
        form = UploadFileForm(request.POST, request.FILES)
        
       
        if form.is_valid():
            data = form.cleaned_data
            print (data)
            f = request.FILES['file']
            
            kind = f.name.split('.')
           
            ck =['jpg', 'jpx', 'png', 'gif', 'webp', 'cr2', 'tif', 'bmp', 'jxr', 'psd', 'ico', 'heic', 'jfif'] 
            dot =kind[len(kind)-1]
            if dot in ck:
                # check = createFolder(url_img'/')
                with open(url_img  + f.name, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                # image 
                img_base64 = ""
                with open(url_img  + f.name, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read())
                    img_base64 = 'data:image/png;base64,%s' % (my_string.decode('utf-8'))
                print (type(f))
                
                return render(request, 'upload.html', {'dt': img_base64})
            else:
                # not image
                messages.info(request, 'Plese input file is image!')
                return render(request, 'name.html')
    else:
        form = UploadFileForm()
    return render(request, 'name.html', {'form': form})


