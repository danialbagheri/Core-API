from django.db import models
from django.db.models.expressions import OrderBy
# Create your models here.



class Faq(models.Model):
    question = models.CharField(max_length=450)
    answer = models.TextField(blank=True, null=True)
    public = models.BooleanField(default=True)
    product = models.ManyToManyField('product.Product', blank=True, related_name="faqs")

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.question
    