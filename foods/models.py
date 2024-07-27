# foods/models.py
from django.db import models

class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    date = models.DateField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, related_name='items', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    carbs = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.food_name

class FoodImage(models.Model):
    image = models.ImageField(upload_to='food_images/')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
