
import uuid
from django.http import HttpResponse
from base.models import UserInteraction
from django.db.models import F

class UniqueIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):
        user_id = request.COOKIES.get('user_id')

        if not user_id:
            user_id = generate_unique_id()
            response = self.get_response(request)
            response.set_cookie('user_id', user_id, max_age=86400 * 60)
        else:
            response = self.get_response(request)
            same_url = UserInteraction.objects.filter(user_id=user_id,visited_url=request.path).count()
            if user_id and request.path.startswith('/blog/') and same_url < 20:
                visited_url = request.path
                UserInteraction.objects.create(user_id=user_id, visited_url=visited_url)

                interaction_count = UserInteraction.objects.filter(user_id=user_id).count()
                if interaction_count > 1000:
                    oldest_interactions = UserInteraction.objects.filter(user_id=user_id).order_by('timestamp')[:50]
                    oldest_interaction_ids = oldest_interactions.values_list('id', flat=True)
                    UserInteraction.objects.filter(id__in=oldest_interaction_ids).delete()

        return response


def generate_unique_id():
    return str(uuid.uuid4()).replace("-", "")[:20]
