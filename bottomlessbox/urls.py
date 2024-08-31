"""bottomlessbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from django.db import router
from django.urls import include, path

from bottomlessboxapi.views.category import CategoryViewSet
from bottomlessboxapi.views.item import ItemViewSet
from bottomlessboxapi.views.location import LocationViewSet
from bottomlessboxapi.views.lore import LoreViewSet
from bottomlessboxapi.views.review import ReviewViewSet
from bottomlessboxapi.views.status import StatusViewSet
from bottomlessboxapi.views.user import UserView

router = DefaultRouter(trailing_slash=False)
router.register(r'items' , ItemViewSet, basename='item')
router.register(r'users', UserView, basename='user')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'statuses', StatusViewSet, basename='status')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'lores', LoreViewSet, basename='lore')
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    
]
