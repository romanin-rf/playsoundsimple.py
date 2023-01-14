import os
import setuptools

# * Функция получения полных путей к файлам в папках и подпапках
def globalizer(dirpath: str) -> list:
    files = []
    folder_abspath = os.path.abspath(dirpath)
    if os.path.isdir(folder_abspath):
        for i in os.listdir(folder_abspath):
            path = folder_abspath + os.sep + i
            if os.path.isdir(path):
                for _i in globalizer(path):
                    files.append(_i)
            elif os.path.isfile(path):
                files.append(path)
    elif os.path.isfile(folder_abspath):
        files.append(folder_abspath)
    return files

# * Ну, setup
setuptools.setup(
    name='playsoundsimple.py',
    version='0.5.5',
    description='A simple library for playing sound files',
    keywords='playsoundsimple',
    packages=setuptools.find_packages(),
    author_email='semina054@gmail.com',
    url="https://github.com/romanin-rf/playsoundsimple.py",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
	long_description_content_type="text/markdown",
    package_data={
        "playsoundsimple": globalizer(
            os.path.join(os.path.dirname(__file__), "playsoundsimple", "data")
        )
    },
	include_package_data=True,
    author='romanin-rf',
    license='MIT',
    install_requires=["sounddevice", "soundfile"],
    setup_requires=["sounddevice", "soundfile"]
)