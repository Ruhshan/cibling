from django.conf import settings
def chat_context(request):
    return {'CHAT_BASE_URL':settings.CHAT_SERVER_BASE_URL}