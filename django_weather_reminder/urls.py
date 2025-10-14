from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/index/', permanent=True), name='root_redirect'),
    path('', include('user_management.urls')),
    path('admin/', admin.site.urls),
]
