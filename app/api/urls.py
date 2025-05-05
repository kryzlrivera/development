from django.urls import path
from .views import HelloWorld, Students, ContactListView
from .exam_views import ChatView
from .product_views import ProductViewSet, PaymentViewSet

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('Students/', Students.as_view(), name='list_student'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('chat/', ChatView.as_view(), name='chat_view'),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product_list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product_detail'),
    path('payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment_list'),
    path('payments/<int:pk>/', PaymentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='payment_detail'),

]
