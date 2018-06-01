import os
from setuptools import find_packages, setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def line_read(fname):
    lines = list(open(os.path.join(os.path.dirname(__file__), fname)))
    return list(filter(None, [line.strip() for line in lines]))


version = __import__('src').get_version()

setup(
    name="sniputils",
    license="MIT",
    version=version,
    python_requires=">=3.6",
    description="utils snippets for zthxxx",
    long_description=read('README.md'),
    author="zthxxx",
    author_email="zthxxx.me@gmail.com",
    url="https://github.com/zthxxx/sniputils",
    packages=find_packages(),
    install_requires=line_read('requirements.txt')
)
