from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_grapesjs.views import GetTemplate


urlpatterns = [
    path('', include('web.urls', namespace='web')),
    path('_nested_admin/', include('nested_admin.urls')),
    path('api/products/', include('product.api.urls', namespace='products_api')),
    path('api/reviews/', include('review.api.urls', namespace='review_api')),
    path('api/surveys/', include('surveys.api.urls', namespace='surveys_api')),
    path('api/web/', include('web.api.urls', namespace='web_api')),
    path('api/page/', include('page.urls', namespace='page')),
    path('api/faq/', include('faq.urls', namespace='faq')),
    path('api/blogs/', include('blog.urls', namespace='blogs_api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
    path('summernote/', include('django_summernote.urls')),
    path('api/users/', include('user.api.urls', namespace='user')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
