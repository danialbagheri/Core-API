from django.db import models


class AmazonOrder(models.Model):
    ORDER_STATUS_PENDING = 'Pending'
    ORDER_STATUS_UNSHIPPED = 'Unshipped'
    ORDER_STATUS_PARTIALLY_SHIPPED = 'PartiallyShipped'
    ORDER_STATUS_SHIPPED = 'Shipped'
    ORDER_STATUS_CANCELED = 'Canceled'
    ORDER_STATUS_UNFULFILLABLE = 'Unfulfillable'
    ORDER_STATUS_INVOICE_UNCONFIRMED = 'InvoiceUnconfirmed'
    ORDER_STATUS_PENDING_AVAILABILITY = 'PendingAvailability'
    ORDER_STATUS_CHOICES = (
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_UNSHIPPED, 'Unshipped'),
        (ORDER_STATUS_PARTIALLY_SHIPPED, 'Partially Shipped'),
        (ORDER_STATUS_SHIPPED, 'Shipped'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
        (ORDER_STATUS_UNFULFILLABLE, 'Unfulfillable'),
        (ORDER_STATUS_INVOICE_UNCONFIRMED, 'Invoice Unconfirmed'),
        (ORDER_STATUS_PENDING_AVAILABILITY, 'Pending Availability'),
    )

    FULFILLMENT_TYPE_AFN = 'AFN'
    FULFILLMENT_TYPE_MFN = 'MFN'
    FULFILLMENT_TYPE_CHOICES = (
        (FULFILLMENT_TYPE_AFN, 'AFN'),
        (FULFILLMENT_TYPE_MFN, 'MFN'),
    )

    ORDER_TYPE_STANDARD_ORDER = 'StandardOrder'
    ORDER_TYPE_LOAD_LEAD_TIME_ORDER = 'LoadLeadTimeOrder'
    ORDER_TYPE_PREORDER = 'Preorder'
    ORDER_TYPE_BACK_ORDER = 'BackOrder'
    ORDER_TYPE_SOURCING_ON_DEMAND_ORDER = 'SourcingOnDemandOrder'
    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_STANDARD_ORDER, 'Standard Order'),
        (ORDER_TYPE_LOAD_LEAD_TIME_ORDER, 'Load Lead Time Order'),
        (ORDER_TYPE_PREORDER, 'Preorder'),
        (ORDER_TYPE_BACK_ORDER, 'Back Order'),
        (ORDER_TYPE_SOURCING_ON_DEMAND_ORDER, 'Sourcing on Demand Order'),
    )

    purchase_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    earliest_delivery_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    amazon_order_id = models.CharField(
        max_length=128
    )

    order_status = models.CharField(
        max_length=128,
        choices=ORDER_STATUS_CHOICES,
    )

    fulfillment_type = models.CharField(
        max_length=128,
        choices=FULFILLMENT_TYPE_CHOICES,
    )

    order_type = models.CharField(
        max_length=128,
        choices=ORDER_TYPE_CHOICES,
    )
