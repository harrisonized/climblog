from setuptools import setup, find_packages

version='1.0'

setup(
    name='climblog',
    description="Harrison's climbing app",
    version=version,
    author='Harrison Wang',
    author_email='harrisonized@gmail.com',
    url='https://github.com/harrisonized/climblog',
    packages=find_packages(),
    include_package_data=True,
)
