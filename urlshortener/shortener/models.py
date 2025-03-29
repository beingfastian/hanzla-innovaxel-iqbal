from django.db import models
import string
import random

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
            while ShortURL.objects.filter(short_code=self.short_code).exists():
                self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"