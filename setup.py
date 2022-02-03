import os
import setuptools

setuptools.setup(
    name='playsoundsimple',
    version='0.1',
    description='A simple library for playing sound files.',
    keywords='playsoundsimple',
    packages=setuptools.find_packages(exclude=["tests"]),
    author_email='semina054@gmail.com',
    url="https://github.com/romanin-rf/playsoundsimple.py",
    zip_safe=False,
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    author='ProgrammerFromParlament',
    license='MIT'
)
