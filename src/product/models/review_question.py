from django.db import models

from . import Product


class ReviewQuestion(models.Model):
    products = models.ManyToManyField(
        to=Product,
        related_name='questions',
        through='ProductReviewQuestionRelation',
    )

    text = models.TextField()

    is_multiple_choice_question = models.BooleanField()

    def __str__(self):
        return f'{self.pk}-{self.text}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_multiple_choice_question:
            self.answer_choices.all().delete()

    class Meta:
        verbose_name = 'Review Question'
        verbose_name_plural = 'Review Questions'


class ProductReviewQuestionRelation(models.Model):
    review_question = models.ForeignKey(
        to=ReviewQuestion,
        on_delete=models.CASCADE,
        related_name='product_relations',
        verbose_name='Review Question',
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='question_relations',
    )

    def __str__(self):
        return self.review_question.text

    class Meta:
        verbose_name = 'Review Question'
        verbose_name_plural = 'Review Questions'
