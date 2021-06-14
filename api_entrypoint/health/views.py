from django.http import JsonResponse
from django.views import View


class HealthView(View):
    def get(self, request):
        return JsonResponse({'status': 'OK'})
