from setuptools import setup
import shared_config_storage

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name="shared_config_storage",
    version=shared_config_storage.__version__,
    author="Francesco Milani",
    author_email="fmilani@bink.com",
    description="shared configurations storage",
    long_description_content_type="text/markdown",
    long_description=readme,
    url='https://git.bink.com/prototypes/shared-config-storage.git',
    packages=[
        'shared_config_storage',
        'shared_config_storage/ubiquity',
        'shared_config_storage/credentials',
        'shared_config_storage/vault'
    ],
    include_package_data=True,
    install_requires=[
        'pycryptodome',
        'requests',
        'hvac',
    ],
    license="Internal",
    zip_safe=True,
    classifiers=("Programming Language :: Python :: 3",),
)
