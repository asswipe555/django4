from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from website import views


from django.views.generic import TemplateView

# 実はページを表示するだけならこのように1行で書くことが出来ます。
index_view = TemplateView.as_view(template_name="registration/homeindex.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # login_requiredで囲むとログイン必須のページになります。
    path("", login_required(index_view), name="homeindex"),
    # この１行でdjangoでデフォルトで用意している以下がすべて入ります。
    # ・ログイン
    # ・ログアウト
    # ・パスワード変更
    # ・パスワード再発行
    path('', include("django.contrib.auth.urls")),
    path('about/',views.AboutView.as_view(),name="about"),
    path('signup/',views.SignUpView.as_view(),name="signup"),
    path('index/',views.trello_view,name="web"),

]