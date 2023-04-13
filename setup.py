from setuptools import find_packages, setup


def read_file(filename):
    """Return the content of a file"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


setup(
    name="azure-devops-formatter",
    version="0.0.1",
    author="azubis 22",
    description="Azure Devops Reporter",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/px-d/azure-devops-formatter",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD",
    ],
    include_package_data=True,
    packages=find_packages(exclude="tests"),
    install_requires=[
        "behave >= 1.2.6",
        "behave < 2.0.0",
        "requests >= 2.28.2",
        "pystache >= 0.6.0"
        # "azure-cli >= 2.47.0",
    ],
)
