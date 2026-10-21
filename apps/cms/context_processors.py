from .models import SiteConfiguration

def site_settings(request):
    config, _ = SiteConfiguration.objects.get_or_create(pk=1)
    return {'site_config': config}
