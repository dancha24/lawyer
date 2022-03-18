from settings.models import Settings


def editset(request):
    name, created = Settings.objects.get_or_create(name='Название')
    return {
        'nameprog': name.value,
    }
