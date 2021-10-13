"""calypso URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_grapesjs.views import GetTemplate


urlpatterns = [
    path('', include('web.urls', namespace='web')),
    path('api/products/', include('product.api.urls', namespace='products_api')),
    path('api/reviews/', include('review.api.urls', namespace='review_api')),
    path('api/web/', include('web.api.urls', namespace='web_api')),
    path('api/page/', include('page.urls', namespace='page')),
    path('api/faq/', include('faq.urls', namespace='faq')),
    path('api/blogs/', include('blog.urls', namespace='blogs_api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
    path('summernote/', include('django_summernote.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
