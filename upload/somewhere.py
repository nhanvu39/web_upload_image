import os

def handle_uploaded_file(f):
    print (type(f))
    with open('image/test.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return 1
        else:
            return 0
    except OSError:
        print('Error create')


