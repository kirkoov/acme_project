from django.conf import settings  # For dev only to share statics, pix, etc.
from django.conf.urls.static import static  # Ditto
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# The plus part is for dev only to share statics, pix, etc. (DEBUG=True!)
