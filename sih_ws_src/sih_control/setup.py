from setuptools import setup

package_name = 'sih_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'cmd_vel_relay = sih_control.cmd_vel_relay:main',
        ],
    },
)
