from setuptools import find_packages, setup

install_requires = [
    'numpy',
    'matplotlib',
]


setup(name='mpl_animation',
      version='0.1.0',
      description='Matplotlib animations made easy.',
      packages=find_packages('.'),
      install_requires=install_requires,
      zip_safe=False)
