from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [
    path('upload', views.upload_img, name = 'upload'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#controlbot