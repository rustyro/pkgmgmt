from marshmallow import Schema, fields, EXCLUDE


class CustomerMeta(Schema):
    pk = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class CustomerSchema(Schema):
    """ Schema to tokenize a card """
    email = fields.Email(required=True)
    name = fields.String(required=True)
    phone = fields.String(required=False)
    metadata = fields.Nested(CustomerMeta, required=True)
    payment_method = fields.String(required=False)

    class Meta:
        unknown = EXCLUDE


class CurrencyNumericField(fields.Float):
    """
    This field converts whatever value it receives into smallest currency unit by multiplying
    the value by 100. also when it receives a value, it divides it by 100
    """

    def _serialize(self, value, attr, obj, **kwargs):
        return value / 100

    def _deserialize(self, value, attr, obj, **kwargs):
        return int(float(value * 100))


class ChargeSchema(Schema):
    amount = CurrencyNumericField(required=True)
    currency = fields.String(required=True)
    customer = fields.String(required=False, allow_none=False)
    idempotency_key = fields.String(required=False, allow_none=False)
    setup_future_usage = fields.String(required=False, allow_none=False)

    class Meta:
        unknown = EXCLUDE


class ChargeExistingCardSchema(ChargeSchema):
    customer = fields.String(required=True, allow_none=False)
    payment_method = fields.String(required=True, allow_none=False)
    off_session = fields.Boolean(required=False, allow_none=True, default=True)
    confirm = fields.Boolean(required=False, allow_none=True, default=True)

    class Meta:
        unknown = EXCLUDE


class PaymentSchema(Schema):
    """ Schema to tokenize a card """
    email = fields.Email(required=True)
    name = fields.String(required=True)
    phone = fields.String(required=True)
    metadata = fields.Nested(CustomerMeta, required=True)

    class Meta:
        unknown = EXCLUDE


class ItemsSchema(Schema):
    price = fields.String(required=True, allow_none=False)
    quantity = fields.Integer(required=False, allow_none=False)


class SubscriptionSchema(Schema):
    """ Schema to create a subscription """

    customer = fields.String(required=True)  # stripe customer ID "cus_xxxxxx"
    payment_behavior = fields.String(required=False)
    proration_behavior = fields.String(required=False, default="none")
    expand = fields.List(fields.String(), required=False)
    items = fields.Nested(ItemsSchema, required=True, many=True)
    billing_cycle_anchor = fields.Integer(required=False, allow_none=False)

    # Todo: Add other acceptable fields here from the stripe API to imporve the wrapper

    class Meta:
        unknown = EXCLUDE
