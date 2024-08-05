from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "address")


class MenuItem(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    dish_name = models.CharField(max_length=255)
    price = models.FloatField()
    restaurant = models.ForeignKey(
        Restaurant, related_name="menu_items", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.dish_name} - {self.restaurant.name}"
