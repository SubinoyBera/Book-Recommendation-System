# This is the setup file for the project. It is used to package the entire project as a Python package.
# It includes metadata about the project, such as its name, version, author, description, etc.

from setuptools import find_packages,setup
from typing import List

# The constant is used to check if the package is being installed in editable mode.
CONNECTOR = '-e .'

def get_requirements(file_name:str) -> List[str]: 
    """
    Reads the requirements file and returns the list of package requirements for the development
    of the project.
    Args:
        file_name(str): Name of the requirements file. 
    Returns:
        List[str]: The list of package requirements.
    """
    requirements = []
    with open(file_name) as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace('\n','') for i in requirements]
        if CONNECTOR in requirements:
            requirements.remove(CONNECTOR)

    return requirements

# Read the long description from the README file.
with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()

# Setup the project package.
setup(
    name = "Book Recommendation System",
    version = "0.0.1",
    author = "Subinoy Bera",
    author_email = "subinoyberadgp@gmail.com",
    description = "End to End AI Book Recommender",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/SubinoyBera/Book-Recommender-System",
    install_requires = get_requirements("requirements-dev.txt"),
    packages = find_packages(where="src"),
    package_dir = {"", "src"},
    python_requires = ">=3.10",
    license = "MIT"
)