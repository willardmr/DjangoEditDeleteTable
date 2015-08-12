from string import capwords
from django.forms import CheckboxInput, SelectMultiple, Select
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from datetime import datetime
from django.utils import timezone

class EditDelete(Select):
    """
    Provides selection of items via checkboxes, with a table row
    being rendered for each item, the first cell in which contains the
    checkbox.
    Only for use with a ModelMultipleChoiceField
    """
    def __init__(self, item_attrs, model_name=None,
                 edit=True, delete=True, *args, **kwargs):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callables in item_attrs will be called with the item to be
            displayed as the sole parameter.

            Any callable attribute names specified will be called and have
            their return value used for display.

            All attribute values will be escaped.
        """
        super(EditDelete, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs
        self.edit = edit
        self.delete = delete
        self.model_name = model_name

    def render(self, name, value,
               attrs=None, choices=()):
        if value is None:
            value = []
        output = []
        output.append('<table id={} class="display">'.format(escape(name)))
        head = self.render_head()
        output.append(head)
        body = self.render_body(name, value, attrs)
        output.append(body)
        output.append('</table>')
        return mark_safe('\n'.join(output))

    def render_head(self):
        output = []
        output.append('<thead>')
        for item in self.item_attrs:
            output.append('<th>{}</th>'.format(clean_underscores(escape(item))))
        if self.edit:
            output.append('<th class="no-sort">Edit</th>')
        if self.delete:
            output.append('<th class="no-sort">Remove</th>')
        output.append('</tr></thead>')
        return ''.join(output)

    def render_body(self, name, value, attrs):
        output = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        for choice in self.choices:
            if choice.pk:
                # If an ID attribute was given, add a numeric index as a
                # suffix, so that the checkboxes don't all have the same
                # ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='{}_{}'.format((attrs['id'])))
                item = choice
                output.append('<tr>')
                for attr in self.item_attrs:
                    if callable(attr):
                        content = attr(item)
                    elif callable(getattr(item, attr)):
                        content = getattr(item, attr)()
                    else:
                        content = getattr(item, attr)
                        if type(content) == datetime:
                            content = timezone.make_naive(content)
                            content = content.date()
                    output.append('<td>{}</td>'.format(escape(content)))
                if not self.model_name:
                    self.model_name = type(choice).__name__
                if self.edit:
                    output.append('<td><a href="/manage/{}/{}/">edit</a>\
                        </td>'.format(self.model_name, choice.pk))
                if self.delete:
                    output.append('<td><a href="/manage/{}/{}/delete">\
                        remove</a></td>'.format(self.model_name, choice.pk))
                output.append('</tr>')
        output.append('</tbody>')
        return ''.join(output)

def clean_underscores(string):
    """
    Helper function to clean up table headers.  Replaces underscores
    with spaces and capitalizes words.
    """
    s = capwords(string.replace("_", " "))
    return s
