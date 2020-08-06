from django.conf import settings as django_settings

def settings(request):
    settings_in_templates = {}
    # Fill in varlist the settings you want to expose to the templates.
    varlist = ["FILTER_INITIAL_NAME"]
    for attr in varlist: 
        if (hasattr(django_settings, attr)):
            settings_in_templates[attr] = getattr(django_settings, attr)
    return {
        'settings': settings_in_templates,
    }	
