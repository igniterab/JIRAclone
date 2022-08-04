from rest_framework import serializers
from .models import MyUser


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password does not match")
        return super().validate(attrs)

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        model = MyUser
        fields = ["email", "password"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields= ["name","email"]