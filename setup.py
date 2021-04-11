from setuptools import setup

setup(
    name = 'PlanScore-CLI',
    url = 'https://github.com/PlanScore/PlanScore-CLI',
    author = 'Michal Migurski',
    description = '',
    packages = [
        'planscore_cli',
        ],
    test_suite = 'planscore.tests',
    package_data = {
        },
    install_requires = [
        ],
    extras_require = {
        },
    entry_points = dict(
        console_scripts = [
            'planscore-client = planscore_cli.client:main',
            ]
        ),
)
