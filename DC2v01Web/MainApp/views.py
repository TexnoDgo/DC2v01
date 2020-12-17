from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status


# TODO: Функция правки имени заказа +
class MainAppClass(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            pass

            return Response(True)
        except Exception:
            return Response(False)