import base64
from zope.interface import implements

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName


class SubjectsVocabulary(object):
    """Vocabulary factory for subjects.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        subjects = list(catalog.uniqueValuesFor('Subject'))
        subjects.sort()
        terms = [SimpleTerm(value=k, token=base64.b64encode(k), title=k)
                 for k in subjects]
        return SimpleVocabulary(terms)


SubjectsVocabularyFactory = SubjectsVocabulary()
