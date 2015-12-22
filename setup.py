from setuptools import find_packages
from setuptools import setup

setup(
    name='bareon_fuel_extension',
    version='1.0.0',

    description='PoC of installing nailgun extension in separate package',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],
    scripts=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'nailgun.extensions': [
            'bareon = bareon_fuel_extension.extension:BareonExtension',
        ],
    },
    zip_safe=False,
)
