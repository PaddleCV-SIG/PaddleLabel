import pathlib
from setuptools import setup, find_packages, Extension

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding="utf-8")

with open("requirements.txt") as fin:
    REQUIRED_PACKAGES = fin.read()

setup(
    name="pplabel",
    version="0.0.1",
    description="标注",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PaddleCV-SIG/PP-Label",
    author="PaddleCV-SIG",
    author_email="linhandev@qq.com",
    license="Apache Software License",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES
    # entry_points={
    #     "console_scripts": [
    #         "pplabel=pplabel",
    #     ]
    },
)
