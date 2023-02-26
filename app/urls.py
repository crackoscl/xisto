
from django.urls import include, path
from rest_framework import routers
from .views import Principal,DacingView

router = routers.DefaultRouter()
router.register(r'', DacingView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('',Principal.as_view(),name='principal'),
    path('api/', include(router.urls)),
]