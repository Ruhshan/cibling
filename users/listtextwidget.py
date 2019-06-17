from django import forms

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)


class ListTextWidgetDynamic(forms.TextInput):
    def __init__(self, item, name, *args, **kwargs):
        super(ListTextWidgetDynamic, self).__init__(*args, **kwargs)
        self._name = name
        self._item = item
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidgetDynamic, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        data_list+"\n{% verbatim %}"
        data_list+='''
        <option v-for="%s in %s">{{%s}}</option>
        ''' %(self._item, self._item+"s", self._item)
        # for item in self._list:
        #     data_list += '<option value="%s">' % item
        data_list += '</datalist>'


        return (text_html + data_list)

class TagWidget(forms.TextInput):
    def __init__(self, name,selectedTagsModel,existingTagsModel, *args, **kwargs):
        super(TagWidget, self).__init__(*args, **kwargs)
        self._name = name


        self.attrs.update({'element-id': self._name,
                           ":typeahead":"true",
                           "v-model":selectedTagsModel,
                           ":existing-tags":existingTagsModel,
                           "placeholder":"Add an "+name.title(),
                           "style":"height:auto",
                           "name":self._name,
                           "id":self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(TagWidget, self).render(name, value, attrs=attrs)
        text_html = text_html.replace("input","tags-input")


        return text_html


