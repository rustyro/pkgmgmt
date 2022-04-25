import stripe
import aiohttp


class AsyncStripe:

    resources = dict(
        subscriptions=stripe.Subscription,
        payment_intent=stripe.PaymentIntent
    )

    def __init__(self, api_key):
        """"""
        self.api_key = api_key
        self.base_url = 'https://api.stripe.com/v1'

    def __build_url(self, resource, id=None):
        uri = f"{self.base_url}/{resource}"
        if id:
            uri = f"{uri}/{id}"
        return uri

    def __build_response(self, resource, data):
        """
        Make a response using the corresponding stripe object class
        Args:
            resource: stripe object resource name
            data:

        Returns:

        """
        if "error" in data:
            resp = stripe.ErrorObject.construct_from(data, self.api_key)
        else:
            resource_class = self.resources.get(resource)
            resp = resource_class.construct_from(data, self.api_key)
        return resp

    async def make_request(self, resource, method, data=None, params=None):
        """
        Make an asynchronous http request
        Args:
            resource: The Stripe resource you're making the request to. E.G subscriptions, invoices, payment_intent ...
            method: The HTTP request method
            data: Data to be sent in the request or used to build the url
            params: Request params

        Returns:
            stripe.stripe_object.StripeObject
        """
        if method not in ['get', 'post']:
            raise ValueError(f"unsupported http method {method}")
        headers = dict(
            Authorization=f"Bearer {self.api_key}"
        )
        id = data.get("id") if data else None
        uri = self.__build_url(resource, id=id)
        async with aiohttp.ClientSession(headers=headers) as conn:
            method_conn = getattr(conn, method)
            async with method_conn(uri) as res:
                result = await res.json()
                return self.__build_response(resource, result)


class StripeMixin(object):
    """ Mixin class for communication with stripe """

    def __init__(self, api_key, **kwargs):
        """

        :param api_key:
        :param kwargs:
        """
        stripe.api_key = api_key
        self.stripe = stripe
        self.async_stripe = AsyncStripe(api_key)

