from setuptools import setup

setup(
    name='chatwizard',
    version='0.1.0',
    description="Discord bot to encourage positiveness within a server by analyzing and scoring each member's behavior.",
    author='Ulas Onat Alakent',
    author_email='ulas.alakent@columbia.edu',
    maintainer='Ulas Onat Alakent',
    maintainer_email='ulas.alakent@columbia.edu',
    url='https://github.com/ulasonat/ChatWizard',
    install_requires=[
        'openai',
        'discord'
    ]
)