from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'OpenCV simplified wrapper in pure python'
LONG_DESCRIPTION = 'TEST version'

# Setting up
setup(
        name="cvSimpton", 
        version=VERSION,
        author="JiayouQin",
        author_email="<jiayouQincn@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['opencv-python'], 
        keywords=['python', 'opencv','cvSimpton'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)