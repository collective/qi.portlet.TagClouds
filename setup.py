from setuptools import setup, find_packages
import os

version = '1.35'

setup(name='qi.portlet.TagClouds',
      version=version,
      description="A configurable plone portlet that displays tag clouds",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
      'Environment :: Web Environment',
      'Framework :: Plone',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',      
        ],
      keywords='plone,tag,cloud,portlet',
      author='Yiorgis Gozadinos',
      author_email='ggozad@jarn.com',
      url='http://svn.plone.org/svn/collective/qi.portlet.TagClouds',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['qi', 'qi.portlet'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['collective.testcaselayer']},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
