from django.db import models

from product.models import Product, ProductVariant
from review.models import Reply
from user.models import User


class Review(models.Model):
    """
    if the user is authenticated we save the user otherwise the name and the
    email.
    """
    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        null=True,
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="user",
    )

    customer_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    customer_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    source = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    score = models.PositiveIntegerField()

    approved = models.BooleanField(
        default=False,
    )

    recommended = models.BooleanField(
        default=False,
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
    )

    like = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
    )

    dislike = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
    )

    reply = models.ManyToManyField(
        to=Reply,
        blank=True,
        related_name="review",
        verbose_name="Replies",
    )

    opened = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ("-date_created",)

    @ property
    def name(self):
        """
        Returns the stored user name.
        """
        if self.user is not None and self.user.get_full_name() != "":
            return self.user.get_full_name()
        elif self.customer_name is None:
            return "Anonymous"
        return self.customer_name

    @ property
    def email(self):
        """
        Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        return self.customer_email

    @property
    def helpful(self):
        """
        returns the helpfulness of the review
        """
        helpful = 0
        helpful += self.like
        helpful -= self.dislike
        return helpful

    def save(self, *args, **kwargs):
        if self.score > 5:
            self.score = 5
        super(Review, self).save(*args, **kwargs)
