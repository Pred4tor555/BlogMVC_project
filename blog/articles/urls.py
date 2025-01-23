from rest_framework import routers

from articles.models import Articles
from articles.views import ArticlesViewSet

# создаем маршруты по умолчанию и убираем слэш в конце
router = routers.DefaultRouter(trailing_slash=False)
# регистрируем маршрут и привязываем контроллер
router.register('articles', viewset=ArticlesViewSet)

# добавляем сгенерированные маршруты в коллекцию urlpatterns
urlpatterns = router.urls
