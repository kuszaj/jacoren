from setuptools import setup
from jacoren import (
    __version__ as version,
    __title__ as title,
    __description__ as description,
    __author__ as author,
    __author_email__ as author_email,
    __license__ as license,
)

# Requirements
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

tests_requirements = ['pytest>=3.1.0', 'psutil>=5.2.0']
setup_requirements = ['pytest-runner']


setup(
    name=title,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    license=license,
    packages=['jacoren'],
    package_dir={'jacoren': 'jacoren'},
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=tests_requirements,
    entry_points = {
        'console_scripts': ['jacoren=jacoren._server:main'],
    }
)
