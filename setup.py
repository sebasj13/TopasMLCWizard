import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topasmlcwizard",
    version="1.0.0",
    author="Sebastian Schäfer",
    author_email="sebastian.schaefer@student.uni-halle.de",
    description="GUI to create and edit MLC sequences for TOPAS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sebasj13/TopasMLCWizard",
    project_urls={"Bug Tracker": "https://github.com/sebasj13/TopasMLCWizard/issues",},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "customtkinter",
        "numpy",
        "scipy",
        "Pillow",
        "pydicom"
    ],
    packages=[
        "topasmlcwizard",
        "topasmlcwizardsrc",
    ],
    scripts=["topasmlcwizard/topasmlcwizard.py"],
    entry_points={
        "console_scripts": ["topasmlcwizard=topasmlcwizard.topasmlcwizard:MLCWizard"],
    },
    keywords=["topas", "monte-carlo", "python", "MLC", "GUI"],
    python_requires=">=3.10",
)