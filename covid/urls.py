from django.urls import path
from . import views
app_name="covid"
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("2/",views.homepage,name="template2"),
]
