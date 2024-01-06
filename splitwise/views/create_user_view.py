from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from splitwise.serializers import UserCreateSerializer


class CreateUserView(GenericAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user = serializer.save()
        return Response(serializer.validated_data)
