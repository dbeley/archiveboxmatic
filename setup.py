import setuptools
import archiveboxmatic

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="archiveboxmatic",
    version=archiveboxmatic.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Automate ArchiveBox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/archiveboxmatic",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["archiveboxmatic=archiveboxmatic.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["archivebox", "pyyaml", "schedule"],
)
