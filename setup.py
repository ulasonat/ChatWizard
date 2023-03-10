from setuptools import setup, find_packages

setup(
    name='ChatWizard',
    version='0.012',
    packages=find_packages(),
    install_requires=[
        'discord',
        'openai',
        'prompts',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
