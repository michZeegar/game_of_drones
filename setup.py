from setuptools import setup

setup(name='game-of-drones',
      version='0.0.2',
      description='An extension to openai gym for controlling a drone.',
      url='',
      author='Michael Seegerer & Domenico Thomaselli',
      author_email='michael.seegerer@tum.de',
      license='I dont care',
      packages=['gameofdrones'],
      install_requires=['gym', 'numpy', 'box2d-py', 'pyopengl', 'pillow', 'pyrr', 'glfw'],
      zip_safe=False)
