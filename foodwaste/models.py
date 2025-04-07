from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Dish Model
class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# FoodEntry Model
class FoodEntry(models.Model):
    EATEN_CHOICES = [
        ('Full', 'Full Meal'),
        ('Half', 'Half Meal'),
        ('Few', 'A Few Bites'),
    ]

    WASTE_CHOICES = [
        ('None', 'No Waste'),
        ('Some', 'Some Waste'),
        ('Lot', 'A Lot of Waste'),
    ]


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    liked = models.BooleanField()
    eaten_amount = models.CharField(max_length=10, choices=EATEN_CHOICES)
    waste_amount = models.CharField(max_length=10, choices=WASTE_CHOICES)
    waste_reason = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.dish.name} - {self.date}"

# DishReport Model
class DishReport(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    total_waste = models.FloatField(default=0.0)
    average_rating = models.FloatField(default=0.0)
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.dish.name} on {self.report_date}"
