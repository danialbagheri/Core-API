from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.


class Reply(models.Model):
    '''
    This models keeps all the replies to the reviews.
    '''
    user_name = models.CharField(
        max_length=200, blank=True, null=True, default="Linco Care")
    user_email = models.EmailField(
        max_length=254, blank=True, null=True, default="")
    comment = models.TextField()


class Review(models.Model):
    '''
    if the user is authenticated we save the user otherwise the name and the
    email.
    '''
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name="user",
                             blank=True, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    score = models.PositiveIntegerField()
    approved = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    like = models.PositiveIntegerField(default=0, blank=True, null=True)
    dislike = models.PositiveIntegerField(default=0, blank=True, null=True)
    reply = models.ManyToManyField(
        Reply, related_name="review", verbose_name="Replies", blank=True)
    # media = models.FileField()

    class Meta:
        ordering = ("-date_created",)

    @ property
    def name(self):
        """
        Returns the stored user name.
        """
        if self.user is not None:
            return self.user.get_full_name()
        elif self.customer_name is None:
            return "Anonymous"
        else:
            return self.customer_name

    @ property
    def email(self):
        """
        Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        else:
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
