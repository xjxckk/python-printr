from setuptools import setup

setup(
    name = 'python_printr',
    packages = ['printr'],
    version = '2026.4.15',
    install_requires=['coloredlogs'],
    description = 'printr',
    url = 'https://github.com/xjxckk/python-printr/',
    download_url = 'https://github.com/xjxckk/python-printr/archive/refs/tags/v0.1.tar.gz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )