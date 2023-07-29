from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    detail = models.TextField(max_length=350, blank=True, null=True)
    percentage = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    last_funds = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    current_funds = models.DecimalField(max_digits=15, decimal_places=2, null=False, default=0)
    goal_founds = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    is_payment = models.BooleanField(default=True)
    still_exist = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name}'

class Movements(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    savings = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    salary_funds_before = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    salary_funds_after = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    savings_funds_before = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    savings_funds_after = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    date = models.DateTimeField(default=timezone.now())
    payment_method = models.CharField(max_length=200, blank=True, null=True, default="-")
    detail = models.TextField(max_length=350, blank=True, null=True, default="-")
    is_savings_withdraw = models.BooleanField(default=False)
    still_exist = models.BooleanField(default=True)

    def __str__(self):
        return f'''{self.category}^ {self.amount}^ {self.savings}^ {self.total_amount}^ {self.salary_funds_before}^ 
{self.salary_funds_after}^ {self.savings_funds_before}^ {self.savings_funds_after}^ {self.date}^ {self.payment_method}^ {self.detail}'''