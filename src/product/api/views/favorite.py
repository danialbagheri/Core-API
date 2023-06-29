from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product


class FavoriteProductUpdateAPIView(UpdateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.filter(is_public=True)
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        action = self.request.data.get('action', 'add')
        if action == 'add':
            user.favorite_products.add(product)
        elif action == 'remove':
            user.favorite_products.remove(product)
        else:
            return Response(
                data='Invalid action.',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data='Action done successfully',
            status=status.HTTP_200_OK,
        )
