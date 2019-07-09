Skip to content

Search or jump to…

Pull requests
Issues
Marketplace
Explore

@cjloader
0
0 0 chalupaul/ironic_importer
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Security  Insights
ironic_importer/setup.py
 chalupaul fixing imports for flake8
b65b40e 6 hours ago
44 lines (40 sloc)  1.42 KB

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf8' ) as f:
    long_description = f.read()

setup(
        name='ironic_image_factory',
        version='0.9.0',
        description='Updates/Adds/Deletes Glance Images',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/rcbops/ironic_inventory',
        author='cam loader',
        author_email='paul.sims@rackspace.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Operators',
            'Topic :: Openstack :: Ironic',
            'License :: OSI Approved :: Apache2',
            'Programming Language :: Python :: 3',
            ],
        keywords="ironic node registration",
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        python_requires='>=3.5',
        install_requires=[
            'pandas',
            'xlrd',
            'gevent==1.4.0',
            'python-ironicclient',
            'python-ironic_inspector_client',
            'python-keystoneclient',
            'python-novaclient',
            'python-glanceclient',
            ],
        entry_points={
            'console_scripts': [
                'ironic_inventory=ironic_importer.inventory:main',
                ]
            }
)
