from . import views


def register_in(router):
    router.register(r'google-auth', views.GoogleAuthViewSet, basename='google-auth')
