from django.urls import path
from IdentityManager import views as identity_views


urlpatterns = [
    path(
        "identify",
        identity_views.IdentityIdentifyViewset.as_view({"post": "create"}),
    ),
]
