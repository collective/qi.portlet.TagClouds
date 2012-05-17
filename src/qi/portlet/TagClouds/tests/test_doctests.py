from unittest import TestSuite
import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite
from qi.portlet.TagClouds.tests.base import TagCloudsFunctionalTestCase

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    suite = TestSuite([
        ZopeDocFileSuite(
            'tests/edit_after_removal.txt', package='qi.portlet.TagClouds',
            test_class=TagCloudsFunctionalTestCase,
            optionflags=optionflags)])
    return suite
