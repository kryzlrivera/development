from rest_framework import serializers
from .store_models import Products, Payment

class ProductSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'product_image', 'price', 'stock', 'created_at']

    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product_image and hasattr(obj.product_image, 'url'):
            url = request.build_absolute_uri(obj.product_image.url)
            print(f"Returning image URL: {url}")
            return url
        return None


class PaymentSerializer(serializers.ModelSerializer):
    receipt_image = serializers.ImageField(required=False, allow_null=True)  # New field for receipt image

    class Meta:
        model = Payment
        fields = ['id', 'name', 'email', 'address', 'payment_method', 'total_amount', 'products', 'receipt_image', 'created_at']

    def validate_products(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Products must be a list")
        for item in value:
            if not all(key in item for key in ['id', 'name', 'quantity', 'price']):
                raise serializers.ValidationError("Each product must have id, name, quantity, and price")
            if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer")
            if not isinstance(item['price'], (int, float)) or item['price'] <= 0:
                raise serializers.ValidationError("Price must be a positive number")
        return value

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be positive")
        return value
