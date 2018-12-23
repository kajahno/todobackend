from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from todo import views

router = DefaultRouter(trailing_slash=False)
router.register(r'todos', views.TodoItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
