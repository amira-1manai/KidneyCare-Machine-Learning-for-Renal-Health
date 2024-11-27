from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static 
from django.conf import settings 

urlpatterns = [
    path('', include('renal_app.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
