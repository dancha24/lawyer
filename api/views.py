from rest_framework.response import Response
from rest_framework.views import APIView
from bot.models import Promocodes
from .serializers import PromoSerializer


class PromoSearchByNameView(APIView):

    def get(self, request, search):
        promo = Promocodes.objects.filter(name__iexact=str(search))
        serializer = PromoSerializer(promo, many=True)
        return Response({"promo": serializer.data})
