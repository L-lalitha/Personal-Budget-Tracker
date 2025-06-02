from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ${self.amount}"
