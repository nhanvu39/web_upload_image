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
from upload.wrapper import Wrapper
# import filetype
import base64
import PIL
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
            f1 = request.FILES['file1']
            kind = f.name.split('.')
            print (type(f))
            ck =['jpg', 'jpx', 'png', 'gif', 'webp', 'cr2', 'tif', 'bmp', 'jxr', 'psd', 'ico', 'heic', 'jfif'] 
            dot =kind[len(kind)-1]
            if dot in ck:
                if (f and f1):
                    print("haha")
                img1 = PIL.Image.open(f)
                img2 = PIL.Image.open(f1)
                wr = Wrapper()
                data = wr.calculate_similarity(img1, img2)
                print(data)
                # # check = createFolder(url_img'/')
                with open(url_img  + f.name, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                # # image 
                img_base64 = ""
                with open(url_img  + f.name, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read())
                    img_base64 = 'data:image/png;base64,%s' % (my_string.decode('utf-8'))
                # print (type(f))
                with open(url_img  + f1.name, 'wb+') as destination:
                    for chunk in f1.chunks():
                        destination.write(chunk)
                # # image 
                img_base641 = ""
                with open(url_img  + f1.name, "rb") as img_file:
                    my_string = base64.b64encode(img_file.read())
                    img_base641 = 'data:image/png;base64,%s' % (my_string.decode('utf-8'))
                
                return render(request, 'upload.html', {'dt': img_base64, 'dt1': img_base641 , 'num': data})
            else:
                # not image
                messages.info(request, 'Plese input file is image!')
                return render(request, 'name.html')
    else:
        form = UploadFileForm()
    return render(request, 'name.html', {'form': form})


