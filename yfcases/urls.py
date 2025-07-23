from django.urls import path,include,re_path
from django.contrib.auth import views as auth_views
from .views import *

app_name='yfcase'

urlpatterns = [
  # 登入
  path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
  #忘記密碼
  path('password-reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
  path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
  path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
  path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),

  # path('',YfcaseListView.as_view(),name="home" ),
  path('',yfcase_list,name="home" ),
  path('all/',yfcase_list_all,name="home_all" ),
  path('all_include_close/',yfcase_list_all_include_close,name="home_all_include_close" ),
  path('yfcase/<int:pk>/',YfcaseDetailView.as_view(),name="yfcase_detail" ),
  path('yfcase/create/',YfcaseCreateView.as_view(),name="yfcase_create" ),
  path('yfcase/<int:pk>/update/',YfcaseUpdateView.as_view(),name="yfcase_update"),
  path('yfcase/<int:pk>/delete/',YfcaseDeleteView.as_view(),name="yfcase_delete"),
  # Land
  path('yfcase/<int:yfcase_id>/land/create/',land_create,name="land_create" ),
  path('yfcase/<int:yfcase_id>/land/update/<int:id>/',land_update,name="land_update" ),
  path('yfcase/<int:yfcase_id>/land/delete/<int:id>/',land_delete,name="land_delete" ),
  # Build
  path('yfcase/<int:yfcase_id>/build/create/',build_create,name="build_create" ),
  path('yfcase/<int:yfcase_id>/build/update/<int:id>/',build_update,name="build_update" ),
  path('yfcase/<int:yfcase_id>/build/delete/<int:id>/',build_delete,name="build_delete" ),
  # Aucion
  path('yfcase/<int:yfcase_id>/auction/create/',auction_create,name="auction_create" ),
  path('yfcase/<int:yfcase_id>/auction/update/<int:id>/',auction_update,name="auction_update" ),
  # Survey
  path('yfcase/<int:yfcase_id>/survey/create/',survey_create,name="survey_create" ),
  path('yfcase/<int:yfcase_id>/survey/update/<int:id>/',survey_update,name="survey_update" ),
  # ObjectBuild
  path('yfcase/<int:yfcase_id>/objectbuild/create/',objectbuild_create,name="objectbuild_create" ),
  path('yfcase/<int:yfcase_id>/objectbuild/update/<int:id>/',objectbuild_update,name="objectbuild_update" ),
  path('yfcase/<int:yfcase_id>/objectbuild/delete/<int:id>/',objectbuild_delete,name="objectbuild_delete" ),
  # ScoreA
  path('yfcase/<int:yfcase_id>/scorea/update/<int:id>/',score_a_adj,name="score_a_update" ),
  path('yfcase/<int:yfcase_id>/scorea/delete/<int:id>/',score_a_clean,name="score_a_delete" ),
  # ScoreB
  path('yfcase/<int:yfcase_id>/scoreb/update/<int:id>/',score_b_adj,name="score_b_update" ),
  path('yfcase/<int:yfcase_id>/scoreb/delete/<int:id>/',score_b_clean,name="score_b_delete" ),
  # ScoreC
  path('yfcase/<int:yfcase_id>/scorec/update/<int:id>/',score_c_adj,name="score_c_update" ),
  path('yfcase/<int:yfcase_id>/scorec/delete/<int:id>/',score_c_clean,name="score_c_delete" ),
  # FinalDecision
  path('yfcase/<int:yfcase_id>/finaldecision/create/',finaldecision_create,name="finaldecision_create" ),
  path('yfcase/<int:yfcase_id>/finaldecision/update/<int:id>/',finaldecision_update,name="finaldecision_update" ),
  path('yfcase/<int:yfcase_id>/finaldecision/delete/<int:id>/',finaldecision_delete,name="finaldecision_delete" ),
  # SubSigntrueA
  path('yfcase/<int:yfcase_id>/subsignturea/update/<int:id>/',subsignture_a_update,name="subsignture_a_update" ),
  path('yfcase/<int:yfcase_id>/subsignturea/delete/<int:id>/',subsignture_a_delete,name="subsignture_a_delete" ),
  # SubSigntrueB
  path('yfcase/<int:yfcase_id>/subsigntureb/update/<int:id>/',subsignture_b_update,name="subsignture_b_update" ),
  path('yfcase/<int:yfcase_id>/subsigntureb/delete/<int:id>/',subsignture_b_delete,name="subsignture_b_delete" ),
  # Result
  path('yfcase/<int:yfcase_id>/result/create/',result_create,name="result_create" ),
  path('yfcase/<int:yfcase_id>/result/update/<int:id>/',result_update,name="result_update" ),

  path('ajax/load-townships/', load_townships, name='ajax_load_townships'),
  
  # 匯出資料
  path('export-excel/',export_yfcase,name='export'),


]
