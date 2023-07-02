from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from company.models import Company
from .models import User
from accounts import serializers
from .permissions import IsOwner


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


class AddEmployeeAPIView(generics.GenericAPIView):
    serializer_class = serializers.AddEmployeeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        if request.user.type != 'admin':
            return Response({'message': 'for creating an employee you must be admin for some company'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Pagination10To100(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetAllCompanyEmployeesAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.GetAllCompanyEmployeesSerializer
    pagination_class = Pagination10To100
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get('pk')
        user = request.user
        company = Company.objects.get(id=company_id)

        if user == company.owner or user in company.employee.filter(type='admin'):
            self.queryset = company.employee.all()
            return super().get(self, request, *args, **kwargs)
        else:
            return Response({'message': 'for getting a list of employees you must be owner or admin for this company'},
                            status=status.HTTP_400_BAD_REQUEST)


class DeleteEmployeesAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DeleteEmployeesSerializer

    def post(self, request):
        company_id = request.data.get('company_id')
        company = Company.objects.get(id=company_id)
        # print(request.data)
        if company.owner == request.user:
            user_ids = request.data.get('ids')  # [1,2,3] List of ID's
            # print(user_ids)
            users = User.objects.filter(id__in=user_ids)
            users = users.filter(type='employee')
            for user in users:
                user.delete()

            return Response({'message': 'Your company employees deleted successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'You are not owner of this company'}, status=status.HTTP_400_BAD_REQUEST)
