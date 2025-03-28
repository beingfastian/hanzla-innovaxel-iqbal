from rest_framework import serializers
from .models import ShortURL
import validators

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            'id', 
            'original_url', 
            'short_code', 
            'created_at', 
            'updated_at', 
            'access_count'
        ]
        read_only_fields = [
            'id', 
            'short_code', 
            'created_at', 
            'updated_at', 
            'access_count'
        ]

    def validate_original_url(self, value):
        """
        Additional URL validation
        """
        if not validators.url(value):
            raise serializers.ValidationError("Invalid URL format")
        return value