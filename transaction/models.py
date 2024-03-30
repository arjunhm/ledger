from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    account = models.ForeignKey("account.Account", on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(
        "category.Category", on_delete=models.SET_NULL, null=True, blank=True
    )

    date = models.DateField()
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.type}"
