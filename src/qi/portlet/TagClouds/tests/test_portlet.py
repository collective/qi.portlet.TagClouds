from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from qi.portlet.TagClouds import tagcloudportlet

from qi.portlet.TagClouds.tests.base import TagCloudsTestCase


class TestPortlet(TagCloudsTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='qi.portlet.TagClouds.TagCloudPortlet')
        self.assertEquals(portlet.addview,
                          'qi.portlet.TagClouds.TagCloudPortlet')

    def test_interfaces(self):
        portlet = tagcloudportlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='qi.portlet.TagClouds.TagCloudPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   tagcloudportlet.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = tagcloudportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, tagcloudportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assignment = tagcloudportlet.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, tagcloudportlet.Renderer))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    return suite
