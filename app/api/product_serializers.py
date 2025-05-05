from rest_framework import serializers
from .product_models import Products, CartItem, Payment

class ProductSerializer(serializers.ModelSerializer):
    p_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'p_image', 'price', 'stock', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.p_image:
            # Manually construct the URL with the port
            base_url = "http://172.17.100.14:3329"
            relative_url = instance.p_image.url
            representation['p_image'] = f"{base_url}{relative_url}"
        else:
            representation['p_image'] = None
        return representation

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'name', 'description', 'p_image', 'price', 'stock', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        product_id = self.context.get('request').data.get('product_id')
        if not product_id:
            raise serializers.ValidationError("Product ID is required")
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            raise serializers.ValidationError(f"Product with ID {product_id} does not exist")

        if data['name'] != product.name:
            raise serializers.ValidationError("Name does not match the product")
        if data['description'] != product.description:
            raise serializers.ValidationError("Description does not match the product")
        if data['price'] != product.price:
            raise serializers.ValidationError("Price does not match the product")
        if data['stock'] != product.stock:
            raise serializers.ValidationError("Stock does not match the product")

        if product.stock < 1:
            raise serializers.ValidationError(f"Product {product.name} is out of stock")

        return data

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer")
        return value

class PaymentSerializer(serializers.ModelSerializer):
    avatar_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Payment
        fields = ['id', 'name', 'email', 'address', 'payment_method', 'total_amount', 'products', 'avatar_image', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.avatar_image:
            # Manually construct the full URL with desired host and port
            image_url = f"http://172.17.100.14:3329{instance.avatar_image.url}"
            representation['avatar_image'] = image_url
        else:
            representation['avatar_image'] = None
        return representation

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
