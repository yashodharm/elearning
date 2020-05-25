from django.conf.urls import url
from . import views as webinar_views
from users import views as user_views

urlpatterns = [
    url(r'^$', webinar_views.webinars, name='webinars'),
    url(r'^student/(?P<webinar_name>[\w ]+)/$', user_views.webinar_homepage, name='webinar_homepage'),
    url(r'^student/(?P<webinar_name>[\w ]+)/charge/$', user_views.charge_webinar ,name='charge_webinar'),
    url(r'^student/(?P<webinar_name>[\w ]+)/charge/test/$', user_views.charged_webinar, name="test_webinar"),
    url(r'^student/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/$', user_views.student_webinar,
        name='student_webinar'),
    
    url(r'^professor/(?P<webinar_name>[\w ]+)/$', webinar_views.webinar, name='professor_webinar'),
    url(r'^professor/(?P<webinar_name>[\w ]+)/delete/$', webinar_views.delete_webinar, name='delete_webinar'),
    url(r'^professor/(?P<webinar_name>[\w ]+)/edit/$', webinar_views.update_webinar, name='edit_webinar'),

    url(r'^professor/(?P<webinar_name>[\w ]+)/students/$', webinar_views.list_students_webinar, name='list_students_webinar'),
    url(r'^professor/(?P<webinar_name>[\w ]+)/students/(?P<student_id>[\d ]+)/remove/$',
        webinar_views.remove_students_webinar, name='remove_students_webinar'),
    url(r'^professor/(?P<webinar_name>[\w ]+)/students/(?P<student_id>[\d ]+)/add/$',
        webinar_views.add_students_webinar, name='add_students_webinar'),

    url(r'^professor/(?P<webinar_name>[\w-]+)/(?P<slug>[\w-]+)/$', webinar_views.session, name='session'),
    url(r'^professor/edit/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/$',
        webinar_views.update_session, name='edit_session'),
    url(r'^professor/delete/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/$',
        webinar_views.delete_session, name='delete_session'),

    url(r'^professor/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<txt_id>[\d ]+)/txt/edit/$',
        webinar_views.update_text_block, name='edit_txt_webinar'),
    url(r'^professor/txt/delete/(?P<txt_id>[\d ]+)/$', webinar_views.delete_text_block, name='delete_txt_webinar'),

    url(r'^professor/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<yt_id>[\d ]+)/link/edit/$',
        webinar_views.update_yt_link, name='edit_link_webinar'),
    url(r'^professor/link/delete/(?P<yt_id>[\d ]+)/$', webinar_views.delete_yt_link, name='delete_link_webinar'),

    url(r'^professor/(?P<webinar_name>[\w ]+)/(?P<slug>[\w-]+)/(?P<gd_id>[\d ]+)/gdlink/edit/$',
        webinar_views.update_gd_link, name='edit_gdlink_webinar'),
    url(r'^professor/gdlink/delete/(?P<gd_id>[\d ]+)/$', webinar_views.delete_gd_link, name='delete_gdlink_webinar'),
    url(r'^professor/file/delete/(?P<file_id>[\d ]+)/$', webinar_views.delete_file, name='delete_file_webinar'),
    
]
