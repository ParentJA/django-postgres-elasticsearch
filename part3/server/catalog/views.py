from rest_framework.generics import ListAPIView

from .models import Wine
from .serializers import WineSerializer
from .filters import WineFilterSet


class WinesView(ListAPIView):
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    filterset_class = WineFilterSet
