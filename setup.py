###########
# Imports #
###############################################################################

import os

from setuptools import setup, find_packages

#############
# Variables #
###############################################################################

package_name: str = 'facecheck-attendance'

version: str = '0.1.0'

description: str = '''
facecheck-attendance is a ...
'''

author: str = '\n'.join([
    'Phachara Wuttisetpaiboon',
])

packages: list[str] = find_packages(exclude=['tests', 'tests.*',])

requirements_path = os.path.join('requirements.txt')

#############
# Functions #
###############################################################################


def read_requirements(path: str) -> list[str]:
    """
    Read a requirements text file as a list of dependencies.

    Parameters
    ----------
    path : str
        Path to the requirements text file.

    Returns
    -------
    list[str]
        List of dependencies.
    """
    with open(path, 'r') as file:
        reqs_list: list[str] = file.read().strip().split('\n')

    return reqs_list

########
# Main #
###############################################################################

requirements: list[str] = read_requirements(requirements_path)

setup(
    name=package_name,
    version=version,
    description=description,
    author=author,
    packages=packages,
    python_requires='>=3.9.0',
    install_requires=requirements,
    include_package_data = True,
)

###############################################################################

