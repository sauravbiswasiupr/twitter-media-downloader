from setuptools import setup, find_packages

setup(
    name='twitter-media-downloader',
    version='1.0.0',
    packages=find_packages(include='downloader'),
    url='https://github.com/sauravbiswasiupr/twitter-media-downloader',
    install_requires=['tweepy'],
    entry_points={
        'console_scripts': [
            'twitter-media-dl=downloader.__main__:main'
        ]
    },
    license='Apache License 2.0',
    author='sauravbiswas',
    author_email='sauravmaximus@gmail.com',
    description='Download images and videos belonging to a particular twitter account',
)
