from .base import StripeMixin
from .schemas import CustomerSchema, PaymentSchema, ChargeSchema, ChargeExistingCardSchema, SubscriptionSchema


class Customer(StripeMixin):

    def create(self, **data) -> dict:
        """
        Create a customer on stripe
        :param data:
        :return: dict

        Example response:
            {"stripe": {
                "customer": {
                    "id": "cus_LD6ZS1ADhiqDqQ",
                    "object": "customer",
                    "address": null,
                     "balance": 0,
                     "created": 1645705418,
                     "currency": null,
                     "default_source": null,
                     "delinquent": false,
                     "description": null,
                     "discount": null,
                     "email": "test_webmaster@test.com",
                     "invoice_prefix": "6EE900EB",
                     "invoice_settings": {
                        "custom_fields": null,
                        "default_payment_method": null,
                        "footer": null
                        },
                    "livemode": false,
                    "metadata": {"pk": "2"},
                    "name": "None None",
                    "next_invoice_sequence": 1,
                    "phone": null,
                    "preferred_locales": [],
                    "shipping": null,
                    "tax_exempt": "none"
                    }
                }
            }
        """
        try:
            body = CustomerSchema().load(data)
            return self.stripe.Customer.create(**body)
        except Exception as e:
            print(e)


class Payment(StripeMixin):

    def charge(self, **data):
        """
        Initaite a charge to a card
        :param data:
        :return:

        Example response:
            {
              "id": "pi_3KaicXHzzIMXxbBC15vrM88u",
              "object": "payment_intent",
              "last_payment_error": null,
              "livemode": false,
              "next_action": null,
              "status": "requires_payment_method",
              "amount": 13900,
              "amount_capturable": 0,
              "amount_received": 0,
              "application": null,
              "application_fee_amount": null,
              "automatic_payment_methods": null,
              "canceled_at": null,
              "cancellation_reason": null,
              "capture_method": "automatic",
              "charges": {
                "object": "list",
                "data": [
                ],
                "has_more": false,
                "total_count": 0,
                "url": "/v1/charges?payment_intent=pi_3KaicXHzzIMXxbBC15vrM88u"
              },
              "client_secret": "pi_3KaicXHzzIMXxbBC15vrM88u_secret_wBXvcrI4feFshFOsOBXUoAYiv",
              "confirmation_method": "automatic",
              "created": 1646667433,
              "currency": "usd",
              "customer": "cus_LHHAqNx1u0mFYi",
              "description": null,
              "invoice": null,
              "metadata": {
              },
              "on_behalf_of": null,
              "payment_method": null,
              "payment_method_options": {
                "card": {
                  "installments": null,
                  "network": null,
                  "request_three_d_secure": "automatic"
                }
              },
              "payment_method_types": [
                "card"
              ],
              "processing": null,
              "receipt_email": null,
              "review": null,
              "setup_future_usage": "off_session",
              "shipping": null,
              "source": null,
              "statement_descriptor": null,
              "statement_descriptor_suffix": null,
              "transfer_data": null,
              "transfer_group": null
            }

        """
        if data.get("payment_method"):
            return self.charge_existing_card(**data)
        return self.charge_new_card(**data)

    def charge_new_card(self, **data):
        """
        Create a customer on stripe
        :param data:
        :return:
        """
        try:
            body = ChargeSchema().load(data)
            return self.stripe.PaymentIntent.create(**body)
        except Exception as e:
            print(e)

    def charge_existing_card(self, **data):
        """
        Charge a customers existing card on stripe
        :param data:
        :return:
        """
        try:
            data.pop("setup_future_usage", None)
            data.update(confirm=True, off_session=True)
            body = ChargeExistingCardSchema().load(data)
            return self.stripe.PaymentIntent.create(**body)
        except Exception as e:
            print(e)


class Subscription(StripeMixin):

    resource = 'subscriptions'

    def create(self, **data):
        """
        Start a subscription
        :param data:
        :return:
        """
        try:
            body = SubscriptionSchema().load(data)
            return self.stripe.Subscription.create(**body)
        except Exception as e:
            print(e)

    async def async_retrieve(self, sub_id):
        """
        Get a subscription by ID asyncronously
        Args:
            sub_id:

        Returns:

        """
        return await self.async_stripe.make_request(self.resource, "get", data={"id": sub_id})

