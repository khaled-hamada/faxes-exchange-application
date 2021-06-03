from django.contrib import admin
from django.urls import path
from django.urls import include
from .import views

urlpatterns = [
    path('', views.home, name='login-page'),
    path('logout/', views.logout_view, name='logout-page'),
    path('login/', views.home, name='login-page'),
    path('change-password/', views.change_password, name='change-password'),
    path('dalel/', views.dalel, name='dalel-page'),
    # path('accounts/logout', views.home, name='logout-page'),

    path('taktet/', views.taktet, name='taktet-page'),
    path('newfax', views.newfax, name='newfax-page'),
    path('newfax_sader', views.newfax_sader, name='newfax-page-sader'),
    path('takt', views.takt, name='takt-page'),
    path('search/', views.search, name='search-page'),
    path('approved/<int:fax_type>/', views.approved, name='approved-page'),
    path('unapproved', views.unapproved, name='unapproved-page'),
    path('denied/', views.denied, name='denied-page'),
    path('manager/', views.manager, name='manager-page'),
    path('manager_start/', views.manager_start, name='manager-start-page'),
    path('edit/<int:fax_id>/', views.edit, name='edit-page'),
    path('depts/', views.depts, name='depts-page'),
    path('view/<int:fax_id>/', views.viewfax, name='viewfax-page'),

    path('comment/<int:rel_fax>/', views.add_manager_comment, name='comment-page'),
    path('close_commeting/<int:rel_fax>/', views.close_commeting, name='close-commeting'),
    path('allow_commeting/<int:rel_fax>/', views.allow_commeting, name='allow-commeting'),
    path('comment-page-dept/<int:rel_fax>/', views.add_dept_comment, name='comment-page-dept'),

    path('viewt/<int:fax_id>/', views.viewfaxt, name='viewfaxt-page'),
    path('delete/<int:fax_id>/', views.delete_fax, name='delete-fax'),
    path('forward-fax-to-manager/<int:fax_id>/', views.forward_fax_to_manager, name='forward-fax-to-manager'),
    path('backward-fax-to-vice-manager/<int:fax_id>/', views.backward_fax_to_vice_manager, name='backward-fax-to-vice-manager'),

    path('report_page/', views.report_page, name='report-page'),
    # path('other_user_in', views.get_all_logged_in_users, name='other_user_in'),

]
