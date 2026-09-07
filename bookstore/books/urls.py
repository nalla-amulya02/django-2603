from rest_framework.routers import DefaultRouter

from .views import bookView

router = DefaultRouter()
router.register('books',bookView)

urlpatterns = router.urls

