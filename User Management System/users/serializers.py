from rest_framework import serializers
from .models import User, UserLog
from PIL import Image
import os
#User serializerı
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # required for create via admin
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'role': {'required': True},
            'department': {'required': True, 'allow_blank': False},
            'status': {'required': True},
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if raw_password:
            instance.set_password(raw_password)
            instance.save()
        # thumbnail
        self.make_thumbnail(instance)
        return instance

    def update(self, instance, validated_data):
        raw_password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if raw_password:
            instance.set_password(raw_password)
            instance.save()
        # thumbnail
        self.make_thumbnail(instance)
        return instance

    def make_thumbnail(self, instance):
        if instance.profile_picture:
            from io import BytesIO
            from django.core.files.base import ContentFile
            from PIL import Image

            try:
                img = Image.open(instance.profile_picture)
                img.thumbnail((200, 200))
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')
                thumb_name = os.path.basename(instance.profile_picture.name)
                thumb_name = f"thumb_{thumb_name}"
                instance.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=True)
            except Exception:
                # silently ignore thumbnail failures (optional: log)
                pass


class UserLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = UserLog
        fields = ['id', 'user_name', 'user_email', 'action', 'performed_by', 'timestamp', 'changes']
