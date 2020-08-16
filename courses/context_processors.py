from django.conf import settings as django_settings

'''
   Some variables can be defined in settings.py and used trought templates
   This script exposes the variables in varlist
'''
def settings(request):
    settings_in_templates = {}
    # Fill in varlist the settings you want to expose to the templates.
    varlist = ['FILTER_INITIAL_NAME','PAYSERVER_URLRETURN','PAYSERVER_URLCANCEL']
    for attr in varlist: 
        if (hasattr(django_settings, attr)):
            settings_in_templates[attr] = getattr(django_settings, attr)
    return {
        'settings': settings_in_templates,
    }	
