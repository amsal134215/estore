"""estore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from django.contrib import admin
from django.urls import path

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter, Route, escape_curly_brackets

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.views import CustomerSubscriptionViewset, CustomerSubscriptionCustomViewSet


class HyphenatedRouter(DefaultRouter):
    """Same as Default Router only switches _ with -"""

    def _get_dynamic_route(self, route, action):
        init_kwargs = route.initkwargs.copy()
        init_kwargs.update(action.kwargs)

        url_path = escape_curly_brackets(action.url_path)

        return Route(
            url=route.url.replace("{url_path}", url_path.replace("_", "-")),
            mapping=action.mapping,
            name=route.name.replace("{url_name}", action.url_name),
            detail=route.detail,
            initkwargs=init_kwargs,
        )


router = HyphenatedRouter()
router.register("subscription", CustomerSubscriptionViewset, basename="subscription")
router.register("subscription-edit", CustomerSubscriptionCustomViewSet, basename="subscription-edit")

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

] + router.urls

schema_view = get_schema_view(
    openapi.Info(
        title="estore API",
        default_version='v1',
        description="estore PANEL",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amsal@we-over-i.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns.extend(
    [
        re_path(
            r"swagger(?P<format>\.json|\.yaml)",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
)
