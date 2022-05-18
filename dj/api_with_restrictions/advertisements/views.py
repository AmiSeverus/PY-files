from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwner
from .filters import AdvertisementFilter
    

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    throttle_classes = [AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['creator',]
    filterset_class = AdvertisementFilter
    read_only_fields = ['creator',]
    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        return super().perform_create(serializer)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        return []