"""
Setup script.
"""

from setuptools import setup, find_packages

if __name__ == '__main__':
    with \
            open('test_requirements.txt') as test_requirements, \
            open('README.rst') as readme:
        setup(
            name='django-adapt',
            use_scm_version=True,
            description=(
                'Universal data processing for Django'
            ),
            author='Alexey Kotlyarov',
            author_email='a@koterpillar.com',
            url='https://github.com/koterpillar/django-adapt',
            long_description=readme.read(),
            classifiers=[
                'License :: OSI Approved :: ' +
                'GNU General Public License v3 or later (GPLv3+)',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
            ],

            packages=find_packages(exclude=['tests']),
            include_package_data=True,

            setup_requires=['setuptools_scm'],

            install_requires=[],

            test_suite='tests',
            tests_require=[
                requirement
                for requirement in test_requirements.readlines()
                if not requirement.startswith('-e ')
            ],
        )
