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
    # # External relationship of the Reviews in case if it is required to review particular SKU (Variant)
    # content_type = models.ForeignKey(
    #     ContentType, on_delete=models.CASCADE)
    # content_id = models.PositiveIntegerField(
    #     u"Content ID", blank=True, null=True)
    # content = GenericForeignKey(ct_field="content_type", fk_field="content_id")
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, verbose_name="user",
                             blank=True, null=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=200, blank=True, null=True)
    user_email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    score = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    helpful = models.PositiveIntegerField(default=0, blank=True, null=True)
    reply = models.ManyToManyField(
        Reply, related_name="review", verbose_name="Replies", blank=True, null=True)

    class Meta:
        ordering = ("-date_created",)

    @ property
    def name(self):
        """
        Returns the stored user name.
        """
        if self.user is not None:
            return self.user.get_full_name()
        else:
            return self.user_name

    @ property
    def email(self):
        """
        Returns the stored user email.
        """
        if self.user is not None:
            return self.user.email
        else:
            return self.user_email

    def save(self, *args, **kwargs):
        if self.score > 5:
            self.score = 5
        super(Review, self).save(*args, **kwargs)
