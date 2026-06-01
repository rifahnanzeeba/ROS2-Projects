from setuptools import find_packages, setup

package_name = 'simple_robot_motion'

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
    maintainer='masaba',
    maintainer_email='masaba@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['move_robot = simple_robot_motion.move_robot:main',
                            'path_follower = simple_robot_motion.path_follower:main',
        ],
    },
)

