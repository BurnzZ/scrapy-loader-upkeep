import os
import codecs
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(this_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(this_dir, 'scrapy_loader_upkeep', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name='scrapy-loader-upkeep',
    version=about['__version__'],
    description=(
        'An alternative to the built-in ItemLoader of Scrapy which focuses on '
        'maintainability of fallback parsers.'),
    long_description=long_description,
    author='Kevin Lloyd Bernal',
    author_email='kevinoxy@gmail.com',
    url='https://github.com/BurnzZ/scrapy-loader-upkeep',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    py_modules=['scrapy_loader_upkeep'],
    install_requires=[
        'scrapy'
    ],
    python_requires='>=3.6',
    classifiers={
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    }
)
