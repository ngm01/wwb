"""
urls.py for SEARCH app of WWB project

"""

from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index),
url(r'^upload$', views.upload),
url(r'^execute_search$', views.execute_search),
url(r'^search_results$', views.search_results),
url(r'^create_file$', views.create_file),
url(r'^export$', views.export),
url(r'^logout$', views.logout)
]