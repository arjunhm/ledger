from django.db import models

class Category(models.Model):
    CATEGORY_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    icon = models.CharField(max_length=50, null=True, blank=True)  # For UI purposes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['type', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.type})"

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return f"{self.category.name} - {self.name}"

