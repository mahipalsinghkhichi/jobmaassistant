from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('apis/', include("myapp.urls")),
    path('admin/', admin.site.urls)
    # path('api/items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]

# myproject/myapp/urls.py

# from django.urls import path
# from .views import ItemList, ItemDetail, api_root  # Import the new view

# urlpatterns = [
#     path('', api_root, name='api-root'),  # Map the view to the root path
#     path('api/items/', ItemList.as_view(), name='item-list'),
#     path('api/items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
# ]
