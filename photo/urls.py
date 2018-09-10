from django.urls import path
from .views import *

app_name = 'photo'
urlpatterns = [
    path('', list, name='list'),
    path('list/<tag>/', TagListView.as_view(), name='list_tag'),
    path('upload/', UploadView.as_view(), name='upload_1'),
    path('upload/', upload, name='upload_2'),
    path('<int:pk>/detail/', DetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='delete'),
]
