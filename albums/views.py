from rest_framework.views import status, Response
from rest_framework.generics import GenericAPIView
from .models import Album
from .serializers import AlbumSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AlbumView(GenericAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get(self, request):
        """
        Obtenção de albums
        """
        albums = Album.objects.all()

        result_page = self.paginate_queryset(albums)
        serializer = AlbumSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Criação de album
        """
        serializer = AlbumSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)
