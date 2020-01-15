# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
from .apis import DialogHistoryApiView, MessagesApiView

urlpatterns = [
    # url(
    #     regex=r'^dialogs/(?P<username>[\w.@+-]+)$',
    #     view=views.DialogListView.as_view(),
    #     name='dialogs_detail'
    # ),
    # url(
    #     regex=r'^dialogs/$',
    #     view=views.DialogListView.as_view(),
    #     name='dialogs'
    # ),
    url(
        regex=r'^dialogs-new/(?P<username>[\w.@+-]+)$',
        view=views.DialogNewListView.as_view(),
        name='dialogs-new'
    ),
    url(
        regex=r'^dialogs-new/$',
        view=views.DialogNewListView.as_view(),
        name='dialogs-new'
    ),
    url(
        regex=r'^api/dialog-history/$',
        view=DialogHistoryApiView.as_view(),
        name='dialogs-history'
    ),
    url(
        regex=r'^api/message-in-dialog/(?P<dialog_id>\d+)/$',
        view=MessagesApiView.as_view(),
        name='messages-in-dialog'
    ),
    url(
        regex=r'^dialogs-sidebar/$',
        view=views.DialogSideBarView.as_view(),
        name='dialogs-sidebar'
    ),

]
