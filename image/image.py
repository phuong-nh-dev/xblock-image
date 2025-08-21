"""Image XBlock implementation"""
# -*- coding: utf-8 -*-

# Imports ###########################################################
from __future__ import absolute_import
import logging

from xblock.core import XBlock
from xblock.fields import Scope, String
from web_fragments.fragment import Fragment
try:
    from xblock.utils.publish_event import PublishEventMixin  # pylint: disable=ungrouped-imports
    from xblock.utils.resources import ResourceLoader  # pylint: disable=ungrouped-imports
except ModuleNotFoundError:  # For backward compatibility with releases older than Quince.
    from xblockutils.publish_event import PublishEventMixin
    from xblockutils.resources import ResourceLoader

LOG = logging.getLogger(__name__)
RESOURCE_LOADER = ResourceLoader(__name__)


def _(text):
    """
    Dummy ugettext.
    """
    return text


# Classes ###########################################################
@XBlock.needs("i18n")
class ImageBlock(XBlock, PublishEventMixin):
    """
    XBlock providing a full-width image display
    """

    display_name = String(
        display_name=_("Display Name"),
        help=_("This name appears in the horizontal navigation at the top of the page."),
        scope=Scope.settings,
        default="Image Display"
    )
    
    image_url = String(
        display_name=_("Image URL"),
        help=_("The URL for your image."),
        scope=Scope.settings,
        default="https://via.placeholder.com/800x400/0066cc/ffffff?text=Sample+Image"
    )
    
    image_alt = String(
        display_name=_("Alternative Text"),
        help=_("Alternative text describes the image and appears if the image is unavailable. This is important for accessibility."),
        scope=Scope.settings,
        default=""
    )

    # Context argument is specified for xblocks, but we are not using herein
    def student_view(self, context):  # pylint: disable=unused-argument
        """
        Player view, displayed to the student
        """
        fragment = Fragment()

        fragment.add_content(RESOURCE_LOADER.render_django_template(
            "/templates/html/image_view.html",
            context={"self": self},
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/image.css'))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/image_view.js'))

        fragment.initialize_js('ImageBlock')

        return fragment

    # Context argument is specified for xblocks, but we are not using herein
    def studio_view(self, context):  # pylint: disable=unused-argument
        """
        Editing view in Studio
        """
        fragment = Fragment()
        # Need to access protected members of fields to get their default value
        default_name = self.fields['display_name']._default  # pylint: disable=protected-access,unsubscriptable-object
        fragment.add_content(RESOURCE_LOADER.render_django_template(
            "/templates/html/image_edit.html",
            context={'self': self, 'defaultName': default_name},
            i18n_service=self.runtime.service(self, 'i18n'),
        ))
        fragment.add_javascript(RESOURCE_LOADER.load_unicode('public/js/image_edit.js'))
        fragment.add_css(RESOURCE_LOADER.load_unicode('public/css/image_edit.css'))

        fragment.initialize_js('ImageEditBlock')

        return fragment

    # suffix argument is specified for xblocks, but we are not using herein
    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):  # pylint: disable=unused-argument
        """
        Change the settings for this XBlock given by the Studio user
        """
        if not isinstance(submissions, dict):
            LOG.error("submissions object from Studio is not a dict - %r", submissions)
            return {
                'result': 'error'
            }

        if 'display_name' in submissions:
            self.display_name = submissions['display_name']
        if 'image_url' in submissions:
            self.image_url = submissions['image_url']
        if 'image_alt' in submissions:
            self.image_alt = submissions['image_alt']

        return {
            'result': 'success',
        }

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench.
        """
        return [("Image scenario", "<vertical_demo><custom_image/></vertical_demo>")]
