from django.db import models


class Faq(models.Model):
    updated = models.DateTimeField(
        auto_now=True,
    )

    question = models.CharField(
        max_length=450,
    )

    answer = models.TextField(
        null=True,
        blank=True,
    )

    public = models.BooleanField(
        default=True,
    )

    product = models.ManyToManyField(
        to='product.Product',
        blank=True,
        related_name='faqs',
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.question
