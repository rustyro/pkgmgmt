import setuptools

setuptools.setup(
    name='IMIntegrations',
    version='1.0.0',
    package_dir={
        'im.stripe': 'im_stripe/im.stripe',
        'im.hubspot': 'im_hubspot/im.hubspot'
    },
    packages=['im.stripe', 'im.hubspot'],
)
