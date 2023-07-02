from rest_framework import serializers
from django.core.validators import validate_email


def valid_name(name):
    if not name.isalpha():
        raise serializers.ValidationError('Your first_name or last_name has not alphabetic symbols')
    return True


def valid_phone_number(phone):
    if not phone.isnumeric() or len(phone) > 12:
        raise serializers.ValidationError('phone number is too length or has not numeric symbols')
    return True


def valid_username(username):
    if not username.isalnum():
        raise serializers.ValidationError('enter valid username')
    return True


def valid_email(email):
    try:
        validate_email(email)
        return True
    except:
        raise serializers.ValidationError('enter valid email')


def password_equality(password, password2):
    if password != password2:
        raise serializers.ValidationError('password != password2')
    return True
