from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
ACCOUNT_CHOICES = (
    ("checking", "Checking"),
    ("savings", "Savings"),
    ("credit_card", "Credit Card"),
)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_CHOICES,
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name}__{self.account_type}__{self.balance}"
