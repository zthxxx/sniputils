from os import path

from setuptools import find_packages, setup


def read(file):
    with get_file(file) as f:
        return f.read()


def get_file(file):
    file = path.join(path.dirname(__file__), file)
    return open(file, 'r', encoding='utf-8')


def line_read(file):
    lines = list(get_file(file))
    return list(filter(None, [line.strip() for line in lines]))


def read_require(file):
    """
    why not use pip parse_requirements see:
    https://github.com/pypa/pip/issues/2286
    """
    requirements = line_read(file)
    # filter comment in requirements file
    requirements = filter(None, [line.split('#')[0].strip() for line in requirements])
    return list(requirements)


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
    install_requires=read_require('requirements.txt')
)
