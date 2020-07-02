from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.routers import DefaultRouter
from product_ventory.users.views import (
    UserCreateViewSet,
)

router = DefaultRouter()
# User management
router.register(r'accounts/register', UserCreateViewSet,base_name='register_view')

urlpatterns = [
    #APIs
    path('api/v1/', include(router.urls)),
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # User stuff: User urls includes go here
    path("accounts/", include("product_ventory.users.urls", namespace="users")),
  path("", include("product_ventory.products.urls", namespace="products")),
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
