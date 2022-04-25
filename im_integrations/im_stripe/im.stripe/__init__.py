from dataclasses import dataclass
from .base import StripeMixin
from .services import Customer, Payment, Subscription


class Stripe:
    """

    """
    def __init__(self, settings):
        """
        Initialization of the Stripe class
        :param settings: settings obj with related values for stripe
        """

        self.customer = Customer(settings.STRIPE_API_KEY)
        self.payment = Payment(settings.STRIPE_API_KEY)
        self.sub = Subscription(settings.STRIPE_API_KEY)
        self.stripe = StripeMixin(settings.STRIPE_API_KEY).stripe
        self.base = StripeMixin(settings.STRIPE_API_KEY)
        self.webhook = self.stripe.Webhook
        self.errors = self.stripe.error

    @dataclass
    class BillingReason:
        subscription_create = "subscription_create"

    @dataclass
    class Status:
        paid = "paid"
        fail = "failed"
        open = "open"
        void = "void"

    @dataclass
    class SubscriptionStatus:
        active = "active"  # subcription is paid for and active
        incomplete = "incomplete"  # subcription has been initiated but not paid for and still in a 23h window
        incomplete_expired = "incomplete"  # subcription has been in incomplete state above 23hrs
        trailing = "trailing"  # subcription has a trial period that's yet to expire
        past_due = "past_due"  # subcriptions lastest_invoice payment failed and will be retried
        canceled = "canceled"  # subcription has been canceled either by user or because of max out payment attempts
        unpaid = "unpaid"  # subcriptions lastest_invoice payment failed multiple times (this may be canceled
        # depending) on subscription settings

        active_statuses = [active, trailing, past_due]
        inactive_statuses = [incomplete_expired, incomplete, canceled, unpaid]
