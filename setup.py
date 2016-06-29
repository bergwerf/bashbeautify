from setuptools import setup

setup(
    name = 'bashbeautify',
    version = '0.1.2',
    description = 'A beautifier for Bash shell scripts written in Python.',
    license = 'GPLv2',
    author = 'Herman Bergwerf',
    author_email = 'hermanbergwerf@gmail.com',
    url = 'https://github.com/hermanbergwerf/bashbeautify',
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
    keywords = ['automation', 'bash', 'format', 'beautify'],
    py_modules = ['bashbeautify'],
    entry_points = {'console_scripts': ['bashbeautify = bashbeautify:main']},
)
