import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
        name='django-syntax-colorize',
        version='0.1',
        description='A django app that provides a filters for working with syntax' \
                'highlighting via the Pygments library.',
        long_description=readme,
        author='Will Larson',
        author_email='lethain@gmail.com',
        url='https://github.com/lethain/django-syntax-colorize',
        packages=find_packages(),
        include_package_data=True,
        install_requires=['pygments', 'lxml'],
        classifiers=[
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Framework :: Django',
            ],
        )

