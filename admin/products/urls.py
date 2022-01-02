from django.urls import path
from .views import  ProductViewSet, UserViewSet


urlpatterns = [
    
    path( 'products', ProductViewSet.as_view({
        'get': 'get_list',
        'post': 'create_product'
    })),

    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'get_product',
        'put': 'update_product',
        'delete': 'delete_product'
    })),

    path('user',UserViewSet.as_view({
        'post': 'create_user'
    })),
    path('user/<str:uid>',UserViewSet.as_view({
        'get': 'get_user',
    }))
]
