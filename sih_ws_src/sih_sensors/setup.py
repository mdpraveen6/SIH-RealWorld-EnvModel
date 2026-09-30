from setuptools import find_packages, setup

package_name = 'sih_sensors'

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
    maintainer='venkataramana',
    maintainer_email='venkataramana@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'sensor_server = sih_sensors.sensor_manager:main',
        'sensor_interfaces = sih_sensors.sensor_interfaces:main',
        'lidar_relay = sih_sensors.lidar_relay:main',
        ],
    },
)
