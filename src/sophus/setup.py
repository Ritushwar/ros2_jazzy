from setuptools import find_packages, setup

package_name = 'sophus'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
        'console_scripts': [
            'cam_subscriber = sophus.camera_subscriber:main',
            'relay_node = sophus.relay_node:main',
            'cam_publisher = sophus.camera_publisher:main',
        ],
    },
)
