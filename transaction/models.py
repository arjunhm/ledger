from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    account = models.ForeignKey(
        "account.Account", on_delete=models.CASCADE, related_name="transactions"
    )
    to_account = models.ForeignKey(
        "account.Account",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transfer_transactions",
    )

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


@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, created, **kwargs):
    if created:
        if instance.type in ["expense", "transfer"]:
            # if instance.amount >= instance.account.balance:
            #     raise ValueError()
            instance.account.balance -= instance.amount
            if instance.type == "transfer" and instance.to_account is not None:
                instance.to_account.balance += instance.amount
                instance.to_account.save()
        else:
            instance.account.balance -= instance.amount
        instance.account.save()
