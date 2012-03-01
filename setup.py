from setuptools import setup

setup(
    name='Check Phrase',
    version='0.8',
    long_description=__doc__,
    packages=['chkphrase'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.8',
        'Flask-SQLAlchemy>=0.15',
        'Jinja2>=2.6',
        'MySQL-python==1.2.3',
        'SQLAlchemy==0.7.5',
        'Werkzeug==0.8.3',
        'wsgiref==0.1.2']
)
