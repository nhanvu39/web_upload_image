from django import forms

class UploadFileForm(forms.Form):
    # Name = forms.CharField(max_length=50)
    file = forms.FileField()

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    age = forms.CharField(label='Your age')


['jpg', 'jpx', 'png', 'gif', 'webp', 'cr2', 'tif', 'bmp', 'jxr', 'psd', 'ico', 'heic'] 