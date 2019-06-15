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

class ListTextWidgetTag(forms.TextInput):
    def __init__(self, data_list, name,tag_model, *args, **kwargs):
        super(ListTextWidgetTag, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self._tag_model = tag_model
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidgetTag, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'
        tag_div='''
                <div>
                <a href='#' class='tag' v-for = "%s in %s"> {{%s}} <span class="cross">X</span></a> 
                </div>
                ''' %(self._tag_model,self._tag_model+"s",self._tag_model)
        data_list+=tag_div

        return (text_html + data_list)




#http://jsfiddle.net/Wky2Z/11/