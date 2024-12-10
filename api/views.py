from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.models import ApiUser, Warehouse, Product
from api.my_permissions import IsOwnerOrAdmin, IsSupplierOrConsumerOrAdmin
from api.serializers import UserSerializer, WareHouseSerializer, ProductSerializer


class ApiUserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = ApiUser.objects.all()
    http_method_names = ['get', 'post', 'delete', 'put', "patch"]

    def get_permissions(self):
        if self.action == 'create':  # создать пользователя может кто-угодно
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsOwnerOrAdmin()]  # все изменения данных пользователя доступны владельцу или админу
        elif self.action in ['list']:
            return [IsAdminUser()]  # список пользователей доступен только админу
        return [permissions.AllowAny()]

class WareHouseModelViewSet(viewsets.ModelViewSet):
    serializer_class = WareHouseSerializer
    queryset = Warehouse.objects.all()
    http_method_names = ['get', 'post', 'delete', 'put', "patch"]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            return [IsAdminUser()]  # любые манипуляции с данными склада доступны только админу
        return [permissions.AllowAny()]  # но просматривать склады может кто-угодно

class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get', 'post', 'delete', 'put', "patch"]

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            return [IsSupplierOrConsumerOrAdmin()]  # изменять продукт может админ, потребитель и поставщик
        elif self.action in ['create', 'destroy']:
            return [IsAdminUser()]  # удалять может только админ
        elif self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]  # просмотр товаров доступен кому-угодно
        return [permissions.AllowAny()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_type = request.user.user_type

        if user_type == 'supplier':
            if int(request.data.get('count', 0)) < 0:
                return Response({'error': 'You can write only positive num'}, status=status.HTTP_400_BAD_REQUEST)
            instance.count += int(request.data.get('count', 0))
        elif user_type == 'consumer':
            if int(request.data.get('count', 0)) < 0:
                return Response({'error': 'You can write only positive num'}, status=status.HTTP_400_BAD_REQUEST)
            count = int(request.data.get('count', 0))
            if instance.count >= count:
                instance.count -= count
            else:
                return Response({'error': 'Not enough products in stock'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.is_staff:
            if int(request.data.get('count', 0)) < 0:
                return Response({'error': 'You can write only positive num'}, status=status.HTTP_400_BAD_REQUEST)
            count = int(request.data.get('count', 0))
            instance.count = count
            name = request.data.get('name')
            instance.name = name
            warehouse_id = request.data.get('warehouse')
            warehouse = Warehouse.objects.get(id=warehouse_id)
            instance.warehouse = warehouse
        else:
            return Response({'error': 'User type not allowed to update product count'},
                            status=status.HTTP_403_FORBIDDEN)

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return redirect('/')
