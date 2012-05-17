from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.PloneTestCase import installPackage
from collective.testcaselayer.ptc import ptc_layer, BasePTCLayer


class TagCloudLayer(BasePTCLayer):
    """ set up basic testing layer """

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        import qi.portlet.TagClouds
        zcml.load_config('configure.zcml', qi.portlet.TagClouds)
        fiveconfigure.debug_mode = False
        installPackage('qi.portlet.TagClouds', quiet=True)
        self.addProduct('qi.portlet.TagClouds')

layer = TagCloudLayer(bases=[ptc_layer])
