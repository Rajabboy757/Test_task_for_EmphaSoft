from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from accounts import serializers


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)  # Elbekdan so'rimiz

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer

    def post(self, request):
        email = request.data.get('email')
        if email in User.objects.values_list('email', flat=True):
            user = User.objects.get(email=email)
            user.set_code()

            # send mail to user.email not implemented yet

            return Response({f'{email}': 'exists',
                             'message': 'Please check your email adress for verification code'},
                            status=status.HTTP_200_OK)
        else:
            return Response({f'{email}': 'does not exist',
                             'message': 'Please make sure that you entered correct email adress'},
                            status=status.HTTP_400_BAD_REQUEST)


class VerificationCodeCheckAPIView(generics.GenericAPIView):
    serializer_class = serializers.VerificationCodeCheckSerializer

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)

        if request.data.get('code') == user.verification_code:
            user.email_verified = True
            user.verification_code = ''
            user.save()
            return Response({'user': 'verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'incorrect code'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request):
        res = VerifyEmailAPIView().post(request)
        return res


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = serializers.NewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserDetailSerializer

    def get(self, request):
        serializer = serializers.UserDetailSerializer(request.user)
        return Response(serializer.data)


class UserUpdateAPIView(generics.GenericAPIView):
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        data = self.serializer_class.validate(serializers.UserUpdateSerializer(), request.data)
        user = User.objects.get(id=request.user.id)
        for attr in data:
            if attr == 'email' and data['email'] != user.email:
                user.email_verified = False
            user.__setattr__(attr, data[attr])

        user.save()

        return Response(data)
