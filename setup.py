from setuptools import setup

setup(
    name="shared_config_storage",
    version="1.1",
    author="Francesco Milani",
    author_email="fmilani@bink.com",
    description="shared configurations storage",
    url='https://git.bink.com/prototypes/shared-config-storage.git',
    packages=[
        'shared_config_storage',
        'shared_config_storage/ubiquity',
        'shared_config_storage/credentials'
    ],
    include_package_data=True,
    install_requires=[
        'pycryptodome'
    ],
    license="Internal",
    zip_safe=True,
    classifiers=("Programming Language :: Python :: 3",),
)
