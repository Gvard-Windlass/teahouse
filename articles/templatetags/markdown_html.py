from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

import markdown as md
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from urllib.parse import urljoin

register = template.Library()

class ImgBaseTreeprocessor(Treeprocessor):
    def run(self, root):
        base_folder = urljoin(settings.MEDIA_URL, 'article_images/')
        
        imgs = root.iter('img')
        for img in imgs:
            img.set('src', urljoin(base_folder, img.get('src')))


class ImgBase(Extension):
    def extendMarkdown(self, md):
        # register the new treeprocessor with priority 15 (run after 'inline')
        md.treeprocessors.register(ImgBaseTreeprocessor(md), 'imgbase', 15)


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code', ImgBase()])