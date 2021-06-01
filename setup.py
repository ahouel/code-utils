
from setuptools import setup, find_packages
import os
import unittest

PATH_ROOT = os.path.dirname(__file__)


def get_test_suite():
    """
    Prepare a test-suite callable with:
        python setup.py test
    """
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


def load_requirements(
        path_dir=PATH_ROOT,
        file_name='install.txt',
        comment_char='#'):
    with open(os.path.join(path_dir, 'requirements', file_name), 'r') as file:
        lines = [ln.strip() for ln in file.readlines()]
    reqs = []
    for ln in lines:
        if ln.startswith("-r"):
            reqs += load_requirements(
                filename=os.path.join(
                    os.path.dirname(file),
                    ln.split(" ")[1]))
        # filer all comments
        if comment_char in ln:
            ln = ln[:ln.index(comment_char)].strip()
        # skip directly installed dependencies
        if ln.startswith('http'):
            continue
        if ln:  # if requirement is not empty
            reqs.append(ln)
    return reqs


def read_file(file):
    with open(file) as f:
        content = f.read()
    return content


# https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras
# Define package extras. These are only installed if you specify them.
# From remote, use like `pip install PACKAGE_NAME[dev, docs]`
# From local copy of repo, use like `pip install ".[dev, docs]"`
extras = {
    #     # 'docs': load_requirements(file_name='docs.txt'),
    #     'examples': load_requirements(file_name='examples.txt'),
    #     'extra': load_requirements(file_name='extra.txt'),
    #     'test': load_requirements(file_name='test.txt')
}
# extras['dev'] = extras['extra'] + extras['test']
# extras['all'] = extras['dev'] + extras['examples']  # + extras['docs']


requirements = load_requirements(file_name='install.txt')

# # Get the long description from the README file
readme = read_file(os.path.join(PATH_ROOT, "README.md"))


# Configure the package build and distribution
#   @see https://github.com/pypa/setuptools_scm
#
# To record the files created use:
#   python setup.py install --record files.txt
setup(
    name='deemea-python-utils',  # Required
    version='0.0.1',  # Required
    author='Florian Müller-Fouarge',
    author_email='florian.muller-fouarge@deemea.com',
    description='A small package with broadly usable utility functions',
    long_description=readme,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/Deemea/python_utils',  # Optional
    license='MIT',

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    # A list of strings or a comma-separated string providing descriptive
    # meta-data.
    keywords=[
        'utils',
        'folder listing',
        'folder walk'
        ],  # Optional

    packages=find_packages(exclude=['tests', 'tests/*', ]),  # Required

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    include_package_data=True,
    platforms='any',
    setup_requires=[],
    install_requires=requirements,   # Optional
    extras_require=extras,
    python_requires='>=3.0',

    test_suite='setup.get_test_suite',
    tests_require=["coverage"],

    # Classifiers help users find your project by categorizing it.
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Natural Language :: English',
        # How mature is this project? Common values are
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 4 - Beta',
        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
