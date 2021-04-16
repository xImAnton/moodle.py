import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()


setuptools.setup(
    name="moodle-xImAnton",
    version="1.0.0",
    author="xImAnton_",
    description="A Python Wrapper for the Moodle Mobile API",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/xImAnton/moodlecrawler",
    project_urls={
        "Bug Tracker": "https://github.com/xImAnton/moodlecrawler/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8"
)
