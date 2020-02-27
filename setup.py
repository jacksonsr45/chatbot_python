from setuptools import setup


setup(
   name='chatbot_python',
   version='1.0',
   description='A simple chat bot with python.',
   license="MIT",
   author='jacksonsr45@gmail.com',
   author_email='jacksonsr45@gmail.com',
   url="http://gnjsistemas.com/",
   packages=[
        'app',
        'teste',
   ],  #same as name
   install_requires=[
        'chatterbot',
        'chatterbot_corpus',
        'setuptools',
        'source',
        'aws-sam-cli',
        ], #external packages as dependencies
   scripts=[
       
           ]
)