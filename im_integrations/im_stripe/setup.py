import setuptools

setuptools.setup(
    name='im_stripe',
    version='1.0.0',
    package_dir={'im.stripe': 'im.stripe'},
    packages=['im.stripe'],
    install_requires=['stripe']
)
