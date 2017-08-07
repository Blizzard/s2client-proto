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
      compile_proto(proto_file, python_out=PROTO_DIR, proto_path=PROTO_DIR)
    with open(os.path.join(PROTO_DIR, '__init__.py'), 'a') as f:
      pass
    build_py.run(self)


setup(
    name='s2clientprotocol',
    version='1.0',
    description='StarCraft II - client protocol.',
    author='Blizzard',
    author_email='jrepp@blizzard.com',
    license='MIT',
    packages=[
        's2clientprotocol',
    ],
    install_requires=[
        'protobuf',
    ],
    cmdclass={
        'build_py': BuildPy,
    },
)
