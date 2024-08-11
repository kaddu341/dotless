from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyARdotless",
    version="0.0.10",
    description="ML utils library for predicting Arabic diacritics.",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaddu341/dotless",
    author="dot-ammar",
    license="BSD-3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    
    install_requires=[
        "numpy",
        "tashaphyne",
        "transformers",
        "tensorflow",
    ],
    
    extras_require={
        "dev": ["pytest", "twine"],
    },
    python_requires=">=3.11",
    package_data={
        # Explicitly include specific files in the packages
        '': ['roots.txt', 'arwiki.wordlist'],
    },
    include_package_data=True,
    zip_safe=False
)