# DjangoEditDeleteTable
A Django widget allow easy jQuery DataTables sorting and pagination for a queryset of objects.  Provides an edit and delete link for each item in the queryset that redirects to standard edit/delete views with the object's pk as a url argument.

Example as used in get_context_data of a class-based view:
```python
def get_context_data(self, **kwargs):
        objects = models.objects.all()
        widget = widgets.EditDelete(
            item_attrs=('attr1', 'attr2'))
        widget.choices = objects
        object_table = playerwidget.render("objects", None)
        context = super().get_context_data(**kwargs)
        context['object_table'] = object_table
        return context
```
        
Render it in the template like: {{ objects }}.


Recommended Datatables Javascript to disallow sorting on the edit/delete columns:

```javascript
<script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css"></link>

<script>
$(document).ready(function(){
    $('#object_table').DataTable({
        "order": [],
        "columnDefs": [{
        "targets"  : 'no-sort',
        "orderable" : false,
    }]
    });
});
</script>
```

Modified from https://djangosnippets.org/snippets/518/ for use with Python 3, Django 1.7.
