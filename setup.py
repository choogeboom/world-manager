from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='World-Manager-CLI',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        world-manager=cli.cli:cli
    """,
)