from setuptools import find_packages, setup

package_name = 'sih_slam'

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
        'odom_node = sih_slam.odom_node:main',
        'sensor_tf_node = sih_slam.sensor_tf_node:main',
        'gazebo_odom_relay = sih_slam.gazebo_odom_relay:main',
        ],
    },
)
