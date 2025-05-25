"""
Setup configuration for LeoForge
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="leoforge",
    version="1.0.0",
    author="LeoForge Team",
    author_email="team@leoforge.ai",
    description="AI-Powered Leo Smart Contract Generator for Aleo Blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LeoForge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "leoforge=src.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "leoforge": ["*.md", "*.txt"],
    },
) 