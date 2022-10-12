from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Order(models.Model):
    SIZES = (
        ('SMALL', 'small'), ('MEDIUM', 'medium'), ('LARGE', 'large')
    )
    STATUS = (
        ('PENDING', 'pending'), ('IN_TRANSIT', 'inTransit'), ('DELIVERED', 'delivered')
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=SIZES, default=SIZES[0][0])
    order_status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0][0])
    # url = models.ImageField(null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Order {self.size} by {self.customer.id}"
