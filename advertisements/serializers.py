from django.contrib.auth.models import User
from .models import AdvertisementStatusChoices
from rest_framework import serializers
from .permissions import IsOwnerOrReadOnly


from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        advertisements = Advertisement.objects.filter(status='OPEN')
        adv_open = []
        counting = []
        for advertisement in advertisements:
            if advertisement.creator == self.context["request"].user:
                adv_open.append(advertisement)
        if len(counting) >= 10:
            raise serializers.ValidationError('У вас не может быть больше 10 открытых объявлений. '
                                              'Закройте или удалите объявление.')

        # TODO: добавьте требуемую валидацию
        return data
