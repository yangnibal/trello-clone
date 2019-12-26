from rest_framework import serializers
from .models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class UserSerializer(serializers.HyperlinkedModelSerializer):
    followers = serializers.CharField(source='followers.username', read_only=True)
    class Meta:
        model = User
        fields = ['profile_img', 'name', 'username', 'email', 'password', 'is_staff', 'short_intro', 'github_link', 'facebook_link', 'homepage_link', 'followers']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['profile_img', 'username', 'password', 'short_intro', 'github_link', 'facebook_link', 'homepage_link']
        

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.profile_img = validated_data.get("profile_img", instance.profile_img)
        instance.set_password(validated_data.get('password', instance.password))
        instance.short_intro = validated_data.get("short_intro", instance.short_intro)
        instance.github_link = validated_data.get("github_link", instance.github_link)
        instance.facebook_link = validated_data.get("facebook_link", instance.facebook_link)
        instance.homepage_link = validated_data.get("homepage_link", instance.homepage_link)
        
        instance.save()
        return instance

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')


        attrs['user'] = user
        return attrs