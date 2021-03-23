from rest_framework import serializers

from .models import Wine, WineSearchWord


class WineSerializer(serializers.ModelSerializer):
    variety = serializers.SerializerMethodField()
    winery = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_variety(self, obj):
        if hasattr(obj, 'variety_headline'):
            return getattr(obj, 'variety_headline')
        return getattr(obj, 'variety')

    def get_winery(self, obj):
        if hasattr(obj, 'winery_headline'):
            return getattr(obj, 'winery_headline')
        return getattr(obj, 'winery')

    def get_description(self, obj):
        if hasattr(obj, 'description_headline'):
            return getattr(obj, 'description_headline')
        return getattr(obj, 'description')

    class Meta:
        model = Wine
        fields = ('id', 'country', 'description', 'points', 'price', 'variety', 'winery',)


class WineSearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineSearchWord
        fields = ('word',)
