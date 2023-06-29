from django.urls import include, path

from app.apps.core.web import views

# Register your urls here

urlpatterns = [
    path("", views.SimpleView.as_view()),
    path("core/", include("app.apps.core.web.urls"))
]

# To register this URLS
# path("core/", include("app.core.web.urls"))
