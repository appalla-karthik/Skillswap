from django.apps import AppConfig

class SkillswapAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skillswap_APP'

    def ready(self):
        import sys
        if 'runserver' in sys.argv or 'shell' in sys.argv or 'migrate' in sys.argv:
            import skillswap_APP.signals