from setuptools import setup

setup(
    name='wpasupplicantconf',
    version='0.2',
    description='Parsing, manipulation and generation of wpa_supplicant.conf files',
    author='Menno Finlay-Smits, Alp Sayin',
    author_email='menno@cacophony.org.nz',
    url='https://github.com/alpsayin/wpasupplicantconf',
    py_modules=['wpasupplicantconf', 'wifi_config_wrapper'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
    ],
)
