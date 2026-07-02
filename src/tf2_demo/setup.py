import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tf2_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ritu',
    maintainer_email='ritushwarneupane111@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [ 'tf_broadcaster = tf2_demo.static_broadcaster:main',
                            'dynamic_broadcaster = tf2_demo.dynamic_broadcaster:main',
                            'tf_listener = tf2_demo.tf2_listener:main',],
    },
)
