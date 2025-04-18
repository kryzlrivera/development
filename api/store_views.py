from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .store_models import Products, Payment
from .store_serializers import ProductSerializer, PaymentSerializer
from django.shortcuts import render

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        print("Incoming POST data:", request.data)
        print("Incoming POST files:", request.FILES)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            print("Saved product:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print("Serialized products for list:", serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print("Serialized products for list:", serializer.data)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        print("Payment POST data:", request.data)
        print("Payment POST files:", request.FILES)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            print("Saved payment:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Payment serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def product_list_view(request):
    return render(request, 'product_list.html')
