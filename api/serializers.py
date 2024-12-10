from rest_framework import serializers, validators

from api.models import ApiUser, Warehouse, Product

"""сериализатор модели пользователя"""
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApiUser
        fields = ['id', 'username', 'email', 'password', "user_type"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = ApiUser.objects.create(
            user_type=validated_data['user_type'],
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])
        return user


"""сериализатор склада"""
class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


"""сериализатор продукта"""
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}}


