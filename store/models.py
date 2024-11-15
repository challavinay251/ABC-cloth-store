from django.db import models
from django.contrib.auth.models import User

class Design(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='design_images/')

    def __str__(self):
        return self.name

class Collection(models.Model):
    design = models.ForeignKey(Design, related_name='collections', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='collection_images/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.design.name}'

class Order(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)  # Changed from 'Collection' to 'collection'
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order for {self.collection.name} by {self.customer_name}'  # Changed from 'Collection' to 'collection'

class Review(models.Model):
    collection = models.ForeignKey(Collection, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=100, blank=True, null=True)  # Optional name
    content = models.TextField()
    rating = models.IntegerField()  # Rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name or self.user.username} for {self.collection.name}"
