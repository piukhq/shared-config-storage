from setuptools import setup

setup(
    name="shared-config-storage",
    version="0.1",
    author="Francesco Milani",
    author_email="fmilani@bink.com",
    description="shared configurations storage",
    url='https://git.bink.com/prototypes/shared-config-storage.git',
    packages=[
        'shared-config-storage/ubiquity'
    ],
    include_package_data=True,
    install_requires=[],
    license="Internal",
    zip_safe=True,
    classifiers=("Programming Language :: Python :: 3",),
)
