from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import secrets
import validators

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)

    def clean(self):
        # Validate URL using the validators library
        if not validators.url(self.original_url):
            raise ValidationError("Invalid URL format")

    @classmethod
    def generate_unique_short_code(cls, length=8):
        """Generate a unique short code"""
        while True:
            # Use URL-safe base64 encoding and truncate
            code = secrets.token_urlsafe(length)[:length]
            
            # Ensure code is alphanumeric and unique
            if not cls.objects.filter(short_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        # Validate URL before saving
        self.full_clean()
        
        # Generate short code if not provided
        if not self.short_code:
            self.short_code = self.generate_unique_short_code()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Short URL'
        verbose_name_plural = 'Short URLs'
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['-created_at'])
        ]
