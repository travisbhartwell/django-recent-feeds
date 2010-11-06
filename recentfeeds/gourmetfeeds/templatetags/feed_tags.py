from django import template
from gourmetfeeds import delicious

register = template.Library()

@register.tag
def gourmet_feed_url(parser, token):
     try:
        tag_name, feed = token.split_contents()
     except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
     return GourmetFeedUrlNode(feed)

class GourmetFeedUrlNode(template.Node):
    def __init__(self, feed):
        self.feed = template.Variable(feed)

    def render(self, context):
        try:
            actual_feed = self.feed.resolve(context)
            return delicious.get_url(actual_feed.source, context['user'].username)
        except template.VariableDoesNotExist:
            return ''
