"""
Django 4 compatible breadcrumb template tags.
Replacement for unmaintained django-bootstrap-breadcrumbs package.
"""
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def clear_breadcrumbs(context):
    """Clear all breadcrumbs from context."""
    # Use context.dicts[0] to modify the top-level context
    context.dicts[0]['breadcrumbs'] = []
    return ''


@register.simple_tag(takes_context=True)
def breadcrumb(context, label, url_or_viewname, *args):
    """
    Add a breadcrumb to the context.

    Args:
        label: The text to display for the breadcrumb
        url_or_viewname: Either a URL path or a view name to reverse
        *args: Arguments to pass to reverse() if url_or_viewname is a view name
    """
    # Use context.dicts[0] to ensure we modify the top-level context
    if 'breadcrumbs' not in context.dicts[0]:
        context.dicts[0]['breadcrumbs'] = []

    # Try to reverse the URL if it looks like a view name
    if url_or_viewname and not url_or_viewname.startswith('/'):
        try:
            url = reverse(url_or_viewname, args=args)
        except NoReverseMatch:
            # If reverse fails, treat it as a plain URL
            url = url_or_viewname
    else:
        url = url_or_viewname

    context.dicts[0]['breadcrumbs'].append({
        'label': label,
        'url': url
    })
    return ''


@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, template_name=None):
    """
    Render breadcrumbs as Bootstrap 5 breadcrumb navigation.

    Args:
        template_name: Optional custom template for rendering (ignored, kept for compatibility)
    """
    breadcrumbs = context.get('breadcrumbs', [])

    if not breadcrumbs:
        return ''
    
    html = ['<ul class="custom-breadcrumbs">']

    for i, crumb in enumerate(breadcrumbs):
        is_last = (i == len(breadcrumbs) - 1)

        if is_last:
            html.append(f'<li aria-current="page">{escape(crumb["label"])}</li>')
        else:
            html.append(f'<li><a href="{escape(crumb["url"])}">{escape(crumb["label"])}</a><span>/</span></li>')

    html.append('</ul>')

    return mark_safe(''.join(html))
