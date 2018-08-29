import os

from setuptools import find_packages, setup


def get_file(file):
    return open(os.path.join(os.path.dirname(__file__), file))


def read(fname):
    with get_file(fname) as f:
        return f.read()


def line_read(fname):
    lines = list(get_file(fname))
    return list(filter(None, [line.strip() for line in lines]))


def project_packages(project, package_dir):
    packages = [project]
    packages.extend([
        '{project}.{package}'.format(project=project, package=package)
        for package in find_packages(package_dir)
    ])
    return packages


project = 'sniputils'
package_dir = 'src'
version = __import__(package_dir).get_version()

setup(
    name=project,
    license='MIT',
    version=version,
    python_requires='>=2.7',
    description='utils snippets for zthxxx',
    long_description=read('README.md'),
    author='zthxxx',
    author_email='zthxxx.me@gmail.com',
    url='https://github.com/zthxxx/sniputils',
    packages=project_packages(project, package_dir),
    package_dir={project: package_dir},
    install_requires=line_read('requirements.txt')
)
