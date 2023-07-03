from setuptools import setup, Extension
import setuptools_scm  # noqa  Ensure it’s installed

setup(ext_modules=[Extension("tinyalign._core", sources=["src/tinyalign/_core.pyx"])])
