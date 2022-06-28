from setuptools import setup, find_packages

version = '0.1.0'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='mkdocs-custom-tags-attributes',
    version=version,
    description='Adding custom attributes using hashtags.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mara-Li/mkdocs-custom-tags-attributes',
    author='Mara-Li',
    author_email='mara-li@outlook.fr',
    license='GPL-3',
    python_requires='>=3.10',
    install_requires=required,
    tests_require=['pytest'],
    packages=find_packages(),
    keywords="mkdocs, custom attributes, pymdownx, markdown extension, markdown, md",
    entry_points={'mkdocs.plugins': ['custom-attributes = custom_attributes.plugin:CalloutsPlugin']}
)
