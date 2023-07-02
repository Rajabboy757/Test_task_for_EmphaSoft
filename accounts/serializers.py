from company.models import Company
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from accounts.validator_functions import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        password_equality(password, password2)
        attrs.pop('password2')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=1, write_only=True)
    username_or_email = serializers.CharField(max_length=255, min_length=3, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'username_or_email', 'tokens']

    def validate(self, attrs):

        password = attrs.get('password', '')
        username_or_email = attrs.pop('username_or_email')

        if '@' in username_or_email:
            email = username_or_email
            user = User.objects.get(email=email)
            username = user.username
        else:
            username = username_or_email
            user = User.objects.get(username=username)

        if user.email_verified:
            user = auth.authenticate(username=username, password=password)
        else:
            raise AuthenticationFailed('For log in you must verify your email')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerificationCodeCheckSerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()


class NewPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=68, write_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'code', 'password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code', '')
        user = User.objects.get(email=email)
        # print(attrs)
        if user.verification_code != code:
            raise serializers.ValidationError('invalid code for user')
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        password_equality(password, password2)
        attrs.pop('password2')
        attrs.pop('code')
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.get(email=email)
        user.set_password(validated_data['password'])
        print(user.verification_code)
        user.verification_code = ''
        print(user.verification_code)
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')
        # fields = '__all__'

    def validate(self, attrs):
        valid_email(attrs.get('email'))
        valid_username(attrs.get('username'))
        valid_phone_number(attrs.get('phone'))
        valid_name(attrs.get('first_name'))
        valid_name(attrs.get('last_name'))

        return attrs


class AddEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    type = serializers.CharField(max_length=10, default='employee', required=False)
    company_id = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'type', 'company_id']

    def validate(self, attrs):
        company_id = attrs.get('company_id', '')
        company = Company.objects.get(id=company_id)
        owner = company.owner
        user = self.context['request'].user
        # print(user, user.id)
        # print(company, company_id, owner, owner.id)
        if not (user == owner or (user.type == 'admin' and user in company.employee.all())):
            raise serializers.ValidationError(
                f'for creating an employee you must be owner or admin for company: {company}')

        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password2 = attrs.pop('password2', '')

        if password != password2:
            raise serializers.ValidationError('password != password2')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        company_id = validated_data.pop('company_id', '')
        company = Company.objects.get(id=company_id)
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        company.employee.add(instance)
        return instance


class GetAllCompanyEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'type']


class DeleteEmployeesSerializer(serializers.ModelSerializer):
    company_id = serializers.CharField(max_length=4)
    ids = serializers.ListField()

    class Meta:
        model = User
        fields = ['ids', 'company_id']


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
