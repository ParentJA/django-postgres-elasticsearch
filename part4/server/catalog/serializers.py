from rest_framework import serializers

from .models import Wine


class WineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ('id', 'country', 'description', 'points', 'price', 'variety', 'winery',)
