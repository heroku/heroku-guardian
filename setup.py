import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')
TESTS_REQUIRE = []


def get_version():
    init = open(
        os.path.join(
            HERE,
            "heroku_guardian",
            "bin",
            "version.py"
        )
    ).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setuptools.setup(
    name="heroku_guardian",
    include_package_data=True,
    version=get_version(),
    author="Ashish Patel",
    author_email="patel.ashish@salesforce.com",
    description="Simple and easy to use security checks for the Heroku platform.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/heroku/heroku_guardian",
    packages=setuptools.find_packages(exclude=['test*', 'tmp*']),
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'click',
        'colorama',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": "heroku-guardian=heroku_guardian.bin.cli:main"},
    zip_safe=True,
    keywords='heroku roles policy policies privileges security',
    python_requires='>=3.6',
)