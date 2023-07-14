from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

handler403 = 'store.views.handler403'
handler404 = 'store.views.handler404'
handler500 = 'store.views.handler500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('store.urls', namespace='store')),
    path("users/", include("users.urls", namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path("users/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
