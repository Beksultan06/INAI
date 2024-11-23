from rest_framework import serializers
from .models import User, Kura

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'type_user']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)
    confirm_password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'type_user', 'password', 'confirm_password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': "Пароли не совпадают"})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': "Минимум 8 символов"})
        return attrs

class KuraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Kura
        fields = ['fio', 'about_me', 'photo1', 'photo2']

    def validate(self, attrs):
        if not attrs.get('photo1') or not attrs.get('photo2'):
            raise serializers.ValidationError({'files': 'Все файлы должны быть загружены.'})