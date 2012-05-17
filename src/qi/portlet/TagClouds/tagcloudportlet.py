from time import time
from operator import itemgetter
from zope.interface import implements
from zope import schema
from zope.formlib import form
from zope.i18n import translate
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.layout.navigation.root import getNavigationRoot
from plone.memoize import ram

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import url_quote

from qi.portlet.TagClouds.vocabularies import SubjectsVocabularyFactory
from qi.portlet.TagClouds import TagCloudPortletMessageFactory as _


def _cachekey(method, self):
    """Time, language, settings based cache
    XXX: If you need to publish private items you should probably
    include the member id in the cache key.
    """
    portal_state = getMultiAdapter((self.context, self.request),
        name=u'plone_portal_state')
    portal_url = portal_state.portal_url()
    lang = self.request.get('LANGUAGE', 'en')
    return hash((portal_url, lang, self.data,
                 time() // self.data.refreshInterval))


class ITagCloudPortlet(IPortletDataProvider):

    portletTitle = schema.TextLine(
        title = _(u"Portlet title"),
        description = _(u"The title of the tagcloud."),
        required = True,
        default = u"Tag Cloud")

    levels = schema.Int(
        title = _(u"Number of different sizes"),
        description = _(u"This number will also determine the biggest size."),
        required = True,
        min = 1,
        max = 6,
        default = 5)

    count = schema.Int(
        title = _(u"Maximum number of shown tags."),
        description = _(u"If greater than zero this number will limit the " \
        "tags shown."),
        required = True,
        min = 0,
        default = 0)

    restrictSubjects = schema.List(
        required = False,
        title = _(u"Restrict by keywords"),
        description = _(u"Restrict the keywords searched. Leaving " \
        "this empty will include all keywords"),
        value_type = schema.Choice(vocabulary =
            'qi.portlet.TagClouds.subjects'))

    filterSubjects = schema.List(
        required = False,
        title = _(u"Filter by keywords"),
        description = _(u"Filter the keywords searched. Only items " \
        "categorized with at least all the keywords selected here " \
        "will be searched. The keywords selected here will be " \
        "omitted from the tag clouds. Leaving the field empty will " \
        "disable filtering"),
        value_type = schema.Choice(vocabulary =
            'qi.portlet.TagClouds.subjects'),
        )

    restrictTypes = schema.List(
        required = False,
        title = _(u"Restrict by types"),
        description = _(u"Restrict the content types. Leaving this empty " \
        "will include all user-friendly content types."),
        value_type = schema.Choice(vocabulary =
            'plone.app.vocabularies.ReallyUserFriendlyTypes'),
        )

    root = schema.Choice(
            title=_(u"Root node"),
            description=_(u"You may search for and choose a folder " \
                          "to act as the root of the navigation tree. " \
                          "Leave blank to use the Plone site root."),
            required=False,
            source=SearchableTextSourceBinder({'is_folderish': True},
                                              default_query='path:'))
    wfStates = schema.List(
            required = True,
            title = _(u"Workflow states to show"),
            description = _(u"Which workflow states to include in the " \
                            "search."),
            value_type = schema.Choice(vocabulary =
                                       'plone.app.vocabularies.WorkflowStates'))

    refreshInterval = schema.Int(
        title = _(u"Refresh interval"),
        description = _(u"The maximum time in seconds for which the portal"\
            " will cache the results. Be careful not to use low values."),
        required = True,
        min = 1,
        default = 3600,
        )


class Assignment(base.Assignment):
    """
    """

    implements(ITagCloudPortlet)

    def __init__(self, portletTitle="TagCloud", levels=5,
        count=0, restrictSubjects=[], filterSubjects=[],
        restrictTypes=[], root=u"", wfStates=[], refreshInterval=3600):

        self.portletTitle = portletTitle
        self.levels = levels
        self.count = count
        self.restrictSubjects = restrictSubjects
        self.filterSubjects = filterSubjects
        self.restrictTypes = restrictTypes
        self.wfStates = wfStates
        self.refreshInterval = refreshInterval
        self.root = root

    @property
    def title(self):
        """
        """
        return "Tag Cloud portlet"


class Renderer(base.Renderer):
    """
    """

    render = ViewPageTemplateFile('tagcloudportlet.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.portal_url = getToolByName(context, 'portal_url')()
        self.catalog = getToolByName(context, 'portal_catalog')
        self.putils = getToolByName(context, 'plone_utils')
        self.levels = data.levels
        self.wfStates = data.wfStates
        self.count = data.count
        self.restrictTypes = data.restrictTypes
        self.root = data.root

    @ram.cache(_cachekey)
    def getTags(self):
        tagOccs = self.getTagOccurrences()
        # If count has been set sort by occurences and keep the "count" first

        if self.count:
            sortedOccs = sorted(tagOccs.items(),
                                key=itemgetter(1),
                                reverse=True)[:self.count]
            tagOccs = dict(sortedOccs)

        thresholds = self.getThresholds(tagOccs.values())
        tags = list(tagOccs.keys())
        tags.sort()
        res = []
        for tag in tags:
            d = {}
            size = self.getTagSize(tagOccs[tag], thresholds)
            if size == 0:
                continue
            d["text"] = tag
            d["class"] = "cloud" + str(size)
            href= self.portal_url + \
                "/search?Subject%3Alist="+url_quote(tag)
            #Add type restrictions to search link
            href = href+ "".join(["&portal_type%3Alist="+url_quote(ptype)
                for ptype in self.restrictTypes])
            #Add workflow restrictions to search link
            href = href+ "".join(["&review_state%3Alist="+url_quote(wstate)
                for wstate in self.wfStates])
            #Add path to search link
            if self.root:
                href = href+"&path=%s"%getNavigationRoot(self.context,
                    relativeRoot=self.root)
            d["href"]=href
            d["count"] = translate(
                _(u'${count} items', mapping={'count': tagOccs[tag]}),
                context=self.request)
            res.append(d)
        return res

    def getPortletTitle(self):
        return self.data.portletTitle

    def getSearchSubjects(self):
        if self.data.restrictSubjects:
            result = self.data.restrictSubjects
        else:
            result = list(self.catalog.uniqueValuesFor('Subject'))
        for filtertag in self.data.filterSubjects:
            if filtertag in result:
                result.remove(filtertag)
        return result

    def getSearchTypes(self):
        if self.data.restrictTypes:
            return self.data.restrictTypes
        else:
            return self.putils.getUserFriendlyTypes()

    def getTagOccurrences(self):
        types = self.getSearchTypes()
        tags = self.getSearchSubjects()
        filterTags = self.data.filterSubjects
        tagOccs = {}
        query = {}
        query['portal_type'] = types
        if self.data.root:
            query['path'] = getNavigationRoot(
                self.context,
                relativeRoot=self.data.root)
        if self.wfStates:
            query['review_state'] = self.wfStates
        for tag in tags:
            result = []
            if filterTags:
                query['Subject'] = {'query': filterTags+[tag],
                                    'operator': 'and'}
            else:
                query['Subject'] = tag
            result = self.catalog.searchResults(**query)
            if result:
                tagOccs[tag] = len(result)

        return tagOccs

    def getTagSize(self, tagWeight, thresholds):
        size = 0
        if tagWeight:
            for t in thresholds:
                size += 1
                if tagWeight <= t:
                    break
        return size

    def getThresholds(self, sizes):
        """This algorithm was taken from Anders Pearson's blog:
         http://thraxil.com/users/anders/posts/2005/12/13/scaling-tag-clouds/
        """
        if not sizes:
            return [1 for i in range(0, self.levels)]
        minimum = min(sizes)
        maximum = max(sizes)
        return [pow(maximum - minimum + 1, float(i) / float(self.levels))
            for i in range(0, self.levels)]

    @property
    def available(self):
        return self.getSearchTypes() and self.getSearchSubjects()


class AddForm(base.AddForm):
    """
    """

    form_fields = form.Fields(ITagCloudPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget

    def create(self, data):
        """
        """
        return Assignment(**data)


class EditForm(base.EditForm):
    """
    """
    form_fields = form.Fields(ITagCloudPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget

    def __call__(self):
        subjectFields = ['restrictSubjects', 'filterSubjects']
        for fieldname in subjectFields:
            field = self.form_fields.get(fieldname).field
            existing = field.get(self.context)
            subject_vocab = SubjectsVocabularyFactory(self.context)
            all_subjects = set([t.title for t in subject_vocab])
            valid = all_subjects.intersection(existing)
            if not valid == set(existing):
                field.set(self.context, list(valid))
        return super(EditForm, self).__call__()
