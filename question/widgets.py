from django.forms.widgets import MultiWidget, TextInput
from django.utils.safestring import mark_safe

class ComponentWidget(MultiWidget):
    label = ('Name', 'Lifespan', 'Expected number of users', 'Cost')
    
    @staticmethod
    def parse(string):
        label = ('Name', 'Lifespan', 'Expected number of users', 'Cost')
        
        parsed = string[3:-2].split("', u'")
        parsed = parsed[:1] + [float(i) for i in parsed[1:]]
        return dict(zip(label, parsed))
    
    def __init__(self, attrs=None):
        widgets = [TextInput, TextInput, TextInput, TextInput]
        super(ComponentWidget, self).__init__(widgets, attrs=attrs)
    
    def decompress(self, value):
        if value:
            return eval(value)
        return [None, None, None, None]
    
    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
                
#            output.append('%s: ' % self.label[i])
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
            output.append('</td><td>')
        return mark_safe(self.format_output(output))


class MultiActorWidget(MultiWidget):
    ACTORS = {
        0 : 'NGO',
        1 : 'Government',
        2 : 'Household',
    }
    
    @staticmethod
    def parse(string):
        parsed = string[3:-2].split("', u'")
        if parsed == ['']:
            return string
        else:
            return parsed
    
    def __init__(self, widgets, attrs=None):
        super(MultiActorWidget, self).__init__(widgets, attrs=attrs)
    
    def decompress(self, value):
        if value:
            return eval(value)
        return [None, None, None]
    
    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
                
            output.append('<p class="actor">%s</p>' % self.ACTORS[i])
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        return mark_safe(self.format_output(output))