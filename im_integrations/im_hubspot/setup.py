import setuptools

setuptools.setup(
    name='im_hubspot',
    version='1.0.0',
    package_dir={'im.hubspot': 'im.hubspot'},
    packages=['im.hubspot'],
    install_requires=['hubspot-api-client']
)
