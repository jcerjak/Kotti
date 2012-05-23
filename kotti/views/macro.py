import colander
from kotti.util import _

class TableOfContentsMacroSchema(colander.MappingSchema):
    depth = colander.SchemaNode(
        colander.Number(), title=_("Depth"), default=1)   

class TableOfContentsMacro(object):
    schema = TableOfContentsMacroSchema()
    name = 'table-of-contents'
    title = _(u'Table of contents')
    def render(self, context, request, body, appstruct):
        contents = dict(
            title = 'Heading1',
            anchor = None,
            children = [
                dict(
                    title= 'Heading2',
                    anchor = None,
                    children = []
                    ),
                ]
            )
        if len(contents):
            return render(
                'kotti:templates/macro/table-of-contents.pt',
                dict(contents=contents),
                request,
                )

def process_macros(self, context, request):
    # Shamelessly stolen from Wordpress (shortcodes)
    # TODO: Change regex (we don't want shortcode style (open/close tag ...))
    names = []
    for macro in config.kotti['macros']:
        name = macro.name
    regex = """\\[(\\[?)({names})\\b([^\\]\\/]*(?:\\/(?!\\])[^\\]\\/]*)*?)(?:(\\/)\\]|\\](?:([^\\[]*(?:\\[(?!\\/\\2\\])[^\\[]*)*)\\[\\/\\2\\])?)(\\]?)""".format(names=names)
    import re
    for match in re.finditer(macro_regex, text):
        name = match.group(0)
    
    kotti.view.render_view_to_response(context, request, )
    return text

class Registry(object):
    def __init__(self):
        self.__list = []
    def all(self):
        return self.__list
    def register(self, macro):
        self.__list.append(macro)

registry = Registry()

def includeme():
    registry.register(TableOfContentsMacro)
