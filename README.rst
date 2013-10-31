====================
qi.portlet.TagClouds
====================

.. contents:: Table of Contents


Introduction
============

.. image:: https://secure.travis-ci.org/collective/qi.portlet.TagClouds.png?branch=master
    :target: http://travis-ci.org/collective/qi.portlet.TagClouds

.. image:: https://coveralls.io/repos/collective/qi.portlet.TagClouds/badge.png?branch=master
    :target: https://coveralls.io/r/collective/qi.portlet.TagClouds

qi.portlet.TagClouds is a plone product that adds tag cloud portlet support.
The following parameters of the portlet are configurable through the web:

* portlet title
* number of different tag sizes
* maximum tags to show
* content types searched (optionally)
* tags (subjects) searched (optionally)   
* section of the site to be searched
* workflow states searched
* filtering by keywords so that a tag cloud of all keywords that are combined
  with the filter keywords is shown

qi.portlet.TagClouds also comes with a simple caching mechanism. Cache remains
valid for a time interval that can be set in the portlet settings.

Installation
============

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        qi.portlet.TagClouds

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``qi.portlet.TagClouds`` and click the 'Activate'
button.

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.
