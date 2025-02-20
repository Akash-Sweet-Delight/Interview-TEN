from rest_framework.serializers import ModelSerializer
from .models import Member, Inventory, Bookings


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class BookingsSerializer(ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
