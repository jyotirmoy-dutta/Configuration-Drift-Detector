from setuptools import setup, find_packages

setup(
    name='configdrift',
    version='0.1.0',
    description='Cross-platform Configuration Drift Detector (CLI & GUI)',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'rich',
        'PyQt5',
        'colorama',
        'click',
        'diff-match-patch',
    ],
    entry_points={
        'console_scripts': [
            'configdrift = configdrift.__main__:main',
        ],
    },
    include_package_data=True,
    python_requires='>=3.8',
) 