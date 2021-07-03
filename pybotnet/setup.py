from distutils.core import setup
setup(
    name='pybotnet',         # How you named your package folder (MyLib)
    packages=['pybotnet'],   # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version='0.15.1',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='gpl-3.0',
    # Give a short description about your library
    description='A Python module for building botnet ,backdoor or trojan with Telegram control panel',
    author='onionj',                   # Type in your name
    author_email='onionj98@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/onionj/pybotnet',
    # I explain this later on
    download_url='https://github.com/onionj/pybotnet/archive/refs/tags/v0.15.1.tar.gz',
    # Keywords that define your package best
    keywords=['onionj pybotnet', 'onionj', 'pybotnet'],
    install_requires=[            # I get to this in a second
        'requests',
        'bs4',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Again, pick a license
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
