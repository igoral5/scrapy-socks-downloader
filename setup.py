# -*- coding: utf-8 -*-
'''
Created on 19 июн. 2019 г.
setup for scrapy-socks-downloader
@author: ilalimov
'''
from setuptools import setup, find_packages

def get_long_description():
    with open('README.md') as fd:
        return fd.read()

setup(
    name='scrapy-socks-downloader',
    version='0.0.1',
    author='Igor Alimov',
    author_email='igoral@gmail.com',
    license='MIT license',
    long_description=get_long_description(),
    description="Downloader for scrapy over socks proxy",
    url='https://github.com/igoral5/scrapy-socks-downloader',
    packages=find_packages(),
    install_requires=[
        'scrapy',
        'txsocksx',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Framework :: Scrapy',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
