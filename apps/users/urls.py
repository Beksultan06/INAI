from django.urls import path
from rest_framework.routers import DefaultRouter
    
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
    
from apps.users.views import UserAPI, UserRegisterAPI, KuraAPI

router = DefaultRouter()
router.register(r"users-list", UserAPI, basename='api-list-users')
router.register(r"create-users", UserRegisterAPI, basename='create-users')
router.register(r"kura", KuraAPI, basename='kura')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
