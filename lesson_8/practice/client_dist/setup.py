from setuptools import setup, find_packages

setup(name="py_mess_mk_client",
      version="0.0.2",
      description="Mess Client",
      author="Mikhail Mihailov",
      author_email="mike.mike@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
