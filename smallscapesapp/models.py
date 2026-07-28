from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    # New reviews from the public form are held for staff approval before they
    # appear on the public Reviews page. This closes the spam/abuse gap where
    # anyone could previously publish unmoderated content instantly.
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - Rating: {self.rating} ({'approved' if self.is_approved else 'pending'})"
