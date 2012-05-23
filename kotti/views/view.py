import warnings

from pyramid.exceptions import NotFound
from pyramid.view import render_view_to_response

from kotti.resources import IContent
from kotti.resources import Document

def render_view_to_response(context, request, name='', secure=True, **data):
    """
    Copied from pyramid.view
    Additional arguments may be passed directly to the view.
    """
    provides = [IViewClassifier] + map_(providedBy, (request, context))
    try:
        reg = request.registry
    except AttributeError:
        reg = get_current_registry()
    view = reg.adapters.lookup(provides, IView, name=name)
    if view is None:
        return None

    if not secure:
        # the view will have a __call_permissive__ attribute if it's
        # secured; otherwise it won't.
        view = getattr(view, '__call_permissive__', view)

    # if this view is secured, it will raise a Forbidden
    # appropriately if the executing user does not have the proper
    # permission
    return view(context, request, **data)

def view_content_default(context, request):
    """This view is always registered as the default view for any Content.

    Its job is to delegate to a view of which the name may be defined
    per instance.  If a instance level view is not defined for
    'context' (in 'context.defaultview'), we will fall back to a view
    with the name 'view'.
    """
    view_name = context.default_view or 'view'
    response = render_view_to_response(context, request, name=view_name)
    if response is None:  # pragma: no coverage
        warnings.warn("Failed to look up default view called %r for %r" %
                      (view_name, context))
        raise NotFound()
    return response

def view_node(context, request):  # pragma: no coverage
    return {}  # BBB

def includeme(config):
    config.add_view('kotti.views.view.view_content_default', context=IContent)

    config.add_view(
        context=Document,
        name='view',
        permission='view',
        renderer='kotti:templates/view/document.pt',
        )
