from setuptools import find_packages, setup

package_name = 'my_go2_project'

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
    maintainer='allre',
    maintainer_email='allre@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'camera_viewer = my_go2_project.camera_viewer:main',
            'yolo_detector = my_go2_project.yolo_detector:main',
            'person_greeter = my_go2_project.person_greeter:main',
        ],
    },
)
