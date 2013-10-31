# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.35'
long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='qi.portlet.TagClouds',
      version=version,
      description="A configurable plone portlet that displays tag clouds",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.0',
          'Framework :: Plone :: 4.1',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='plone,tag,cloud,portlet',
      author='Yiorgis Gozadinos',
      author_email='ggozad@jarn.com',
      url='https://github.com/collective/qi.portlet.TagClouds',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['qi', 'qi.portlet'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      install_requires=[
          'plone.app.form',
          'plone.app.layout',
          'plone.app.portlets',
          'plone.app.vocabularies',
          'plone.memoize',
          'plone.portlets',
          'Products.CMFCore',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'collective.testcaselayer',
              'Products.PloneTestCase',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
