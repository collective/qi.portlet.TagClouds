Changelog
=========

1.35
----

* Update buildout.cfg to Plone 4.2, gitignore build products [gyst]
* Change import to work with Plone 4.1.x and Plone 4.2.x [lccruz]

1.34
----

* Moved collective.testcaselayer from the install_requires to a 'test'
  extras_require. [maurits]
* Do not require cmf.ManagePortal to add or edit the portlet [erral]

1.33
----
* Enable (language-independent) content across multiple INavigationRoot
  Folders to be searched for tags [gyst]
* Change import of IVocabularyFactory in order to work with Plone 4.0.x and
  Plone 4.1.x [erico_andrei]
* Added Brazilian Portuguese translation [erico_andrei]

1.32
----
* Removed the member id from the cache key in portlet. Credits to dimo for
  reporting. [ggozad]
* Switched to using native plone vocabulary for workflow states on portlet
  edit form. [piv]
* Remove old file structure now that everything moved to src/ subfolder.
  [kdeldycke]
* Added german translation [kiwisauce]

1.31
----
* Fixed a case where the edit form is invoked and a previously selected
  keyword does not exist anymore. [ggozad]
* Fixed cache key for multiple sites. Thanks to Guido Stevens [ggozad]
* Plone 4 compatibility. [ggozad]
* Moved to using collective.testcaselayer for testing. [ggozad]

1.30
----
* The product is now accompanied with proper tests. [ggozad]
* Added filtering by keyword. Thanks to lzdych for the idea and 
  discussions. [ggozad]
* All important parameters (workflow states, portal types and search path) 
  are now present in the search links. [ggozad]
* Moved vocabularies. [ggozad]
* Removed the settings shouldRestrictBySubject and shouldRestrictByTypes. 
  Now just using sane defaults. [ggozad]
* Modified the caching mechanism, so that it takes into account the portlet
  settings. This ensures separate caching for separate portlets. [ggozad]
* Added the member in the portlet cache key. This will increase the
  calculations necessary, but is important as it was possible to cache private
  objects as well. [ggozad]
* Added the number of items found under the tag in the *title* of the links.
  [lzdych]
* Up french translation with new msgids. [toutpt]
* Add translation of workflow states vocabulary. [toutpt]

1.21
----

* Fixed caching policy for multilingual sites, resolves: #2 [lzdych]
* Added quoting of tag links: fixes not working search by tags with special
  chars. [lzdych]
* Added czech translation. [lzdych]
* extended html markup to support rounded corners, resolves: #1. [lzdych]

1.20
----

* Added french translation. [toutpt]

1.11
----------------

* Added workflow states to the configuration options. [ggozad]
* Added maximum tags to display to the configuration options. [ggozad]

1.1
----------------

* Added root folder to search under. [ggozad]

1.0
----------------

* Initial release [ggozad]
