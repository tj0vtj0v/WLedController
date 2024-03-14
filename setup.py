from distutils.core import setup

setup(
    name='WLedController',
    packages=['WLedController'],
    version='0.3',
    license='MIT',
    description='simple implementation of the json-api from WLeds https://kno.wled.ge/interfaces/json-api/',
    author='Tjorven Burdorf',
    author_email='BurdorfTjorven@gmail.com',
    url='https://github.com/tj0vtj0v/WLedController',
    download_url='https://github.com/tj0vtj0v/WLedController/archive/refs/tags/v_0.3.tar.gz',
    keywords=['WLed', 'IoT', 'Connector', 'API'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
