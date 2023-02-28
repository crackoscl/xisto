
from django.urls import include, path
# from rest_framework import routers
from .views import Principal,DancingListApiView,DacingCreateApiView,DacingDestroyApiview,DacingRetriApiView,DacingUpdateApiview

# router = routers.DefaultRouter()
# router.register(r'', DacingView)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('',Principal.as_view(),name='principal'),
#     path('api/', include(router.urls)),
# ]

urlpatterns = [
     path('',Principal.as_view(),name='principal'),
     path('api/',DancingListApiView.as_view(),name='list_dacing'),
     path('api/create_dacing/',DacingCreateApiView.as_view(),name='create_dacing'),
     path('api/retriview_dancing/<str:pk>/',DacingRetriApiView.as_view(),name='retriview_dacing'),
     path('api/update_dancing/<str:pk>/',DacingUpdateApiview.as_view(),name='update_dacing'),
     path('api/delete_dacing/<str:pk>/',DacingDestroyApiview.as_view(),name='delete_dacing')
]

