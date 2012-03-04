from setuptools import setup

setup(
    name='Check Phrase',
    version='0.9',
    long_description=__doc__,
    packages=['chkphrase'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.8',
        'Flask-SQLAlchemy>=0.15',
        'MySQL-python>=1.2.3',
        'SQLAlchemy>=0.7.5',
        'BeautifulSoup>=3.2.1'
        'requests>=0.10.6']
)
