from Products.PloneTestCase import PloneTestCase
from Products.Five.testbrowser import Browser
from qi.portlet.TagClouds import testing


PloneTestCase.setupPloneSite()


class TagCloudsTestCase(PloneTestCase.PloneTestCase):
    """We use this base class for all the tests in this package.
    """
    layer = testing.layer


class TagCloudsFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """We use this class for functional integration tests.
    """
    layer = testing.layer

    def getCredentials(self):
        return '%s:%s' % (PloneTestCase.default_user,
            PloneTestCase.default_password)

    def getBrowser(self, loggedIn=True):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            auth = 'Basic %s' % self.getCredentials()
            browser.addHeader('Authorization', auth)
        return browser
