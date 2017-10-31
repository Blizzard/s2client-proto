#!/usr/bin/python
"""Module setuptools script."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess
import sys

from distutils.spawn import find_executable
from setuptools import setup
from setuptools.command.build_py import build_py

import s2clientprotocol.build

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))
PROTO_DIR = os.path.join(SETUP_DIR, 's2clientprotocol')


if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
  protoc = os.environ['PROTOC']
else:
  protoc = find_executable('protoc')


def proto_files(root):
  """Yields the path of all .proto files under the root."""
  for (dirpath, _, filenames) in os.walk(root):
    for filename in filenames:
      if filename.endswith('.proto'):
        yield os.path.join(dirpath, filename)


def compile_proto(source, python_out, proto_path):
  """Invoke Protocol Compiler to generate python from given source .proto."""
  if not protoc:
    sys.exit('protoc not found. Is the protobuf-compiler installed?\n')

  protoc_command = [
      protoc,
      '--proto_path', proto_path,
      '--python_out', python_out,
      source,
  ]
  if subprocess.call(protoc_command) != 0:
    sys.exit('Make sure your protoc version >= 2.6. You can use a custom '
             'protoc by setting the PROTOC environment variable.')


class BuildPy(build_py):

  def run(self):
    for proto_file in proto_files(PROTO_DIR):
      compile_proto(proto_file, python_out=SETUP_DIR, proto_path=SETUP_DIR)
    with open(os.path.join(PROTO_DIR, '__init__.py'), 'a') as f:
      pass
    build_py.run(self)


setup(
    name='s2clientprotocol',
    version=s2clientprotocol.build.game_version(),
    description='StarCraft II - client protocol.',
    author='Blizzard Entertainment',
    author_email='jrepp@blizzard.com',
    license='MIT',
    url='https://github.com/Blizzard/s2client-proto',
    packages=[
        's2clientprotocol',
    ],
    install_requires=[
        'protobuf',
    ],
    cmdclass={
        'build_py': BuildPy,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries',
    ],
)
