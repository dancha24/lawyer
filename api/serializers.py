from rest_framework import serializers


class PromoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    sale = serializers.CharField(max_length=200)
    aktive = serializers.BooleanField()
    linkpay = serializers.CharField(max_length=200)
