from cStringIO import StringIO
from urllib2 import urlopen
from urlparse import urljoin

from lxml import etree

import settings


DELICIOUS_BASE_URL = 'http://feeds.delicious.com/v2/rss/'
DELICIOUS_BASE_LENGTH = len(DELICIOUS_BASE_URL)

BASE_LENGTH = len(settings.BASE_URL)

URL_PREFIX = 'gourmetfeeds/f/'
URL_PREFIX_LENGTH = len(URL_PREFIX)


def get_url(source_url, username):
    if source_url.startswith(DELICIOUS_BASE_URL):
        feed_part = source_url[DELICIOUS_BASE_LENGTH:]

        url = urljoin(settings.BASE_URL,
                      URL_PREFIX + username + "/" + feed_part)

        return url


def get_source_url_from_path(url):
    """Assume for now, it is just the portion that comes after the
    base URL and isn't absolute."""
    source_url = url

    if source_url.startswith('/'):
        source_url = source_url[1:]
    source_url = urljoin(DELICIOUS_BASE_URL, source_url)
    if source_url.endswith('/'):
        source_url = source_url[:-1]

    return source_url


class DeliciousFeedRss(object):
    GUID_URL_BASE = 'http://www.delicious.com/url/'
    GUID_URL_BASE_LENGTH = len(GUID_URL_BASE)

    GUID_LENGTH = 32

    def __init__(self, source_url, our_url):
        self.source_url = source_url
        self.our_url = our_url
        self.rss = urlopen(self.source_url)

        self.parser = etree.XMLParser(strip_cdata=False)
        self.tree = etree.parse(self.rss, self.parser)

        self._update_atom_link()

    def _update_atom_link(self):
        link = self.tree.find('channel/{http://www.w3.org/2005/Atom}link')
        link.attrib['href'] = self.our_url

    def _extract_guid(self, guid_url):
        guid = guid_url

        if guid.startswith(DeliciousFeedRss.GUID_URL_BASE):
            guid = guid[DeliciousFeedRss.GUID_URL_BASE_LENGTH:]

        guid = guid[:DeliciousFeedRss.GUID_LENGTH]

        return guid

    def get_item_guids(self):
        guids = [self._extract_guid(guid.text)
                 for guid in self.tree.findall("channel/item/guid")]

        return guids

    def remove_item_with_guid(self, guid):
        # Find a more efficient way of doing this
        guid_elements = self.tree.findall("channel/item/guid")
        for element in guid_elements:
            if element.text.find(guid) != -1:
                item = element.getparent()
                item.getparent().remove(item)
                break

    def get_rss(self):
        rss_output = StringIO()
        self.tree.write(rss_output,
                        xml_declaration="<?xml version='1.0' encoding='UTF-8'?>",
                        encoding='UTF-8')
        rss_output_string = rss_output.getvalue()
        rss_output.close()

        return rss_output_string

