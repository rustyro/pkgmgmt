from dataclasses import dataclass


class Hubspot:
    """

    """
    def __init__(self, settings):
        """
        Initialization of the hubspot class
        :param settings: settings obj with related values for hubspot
        """
        self.name = "hubspot"

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
