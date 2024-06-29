from kart.models import Cake

from rest_framework import serializers

class CakeSerializer(serializers.ModelSerializer):

    size_object=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Cake

        fields="__all__"

        read_only_fields=["id","category_object","size_object","flavour_object","occasion_object","tag_object","created_date","updated_date","is_active"]