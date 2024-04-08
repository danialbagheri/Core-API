from rest_framework import routers

from . import views

app_name = 'bundles_api'

bundle_routers = routers.DefaultRouter()
bundle_routers.register(
    prefix=r'',
    viewset=views.BundleReadOnlyViewSet,
    basename='bundles',
)

urlpatterns = [] + bundle_routers.urls
