from django.apps import AppConfig


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'

    def ready(self):
        # Warm up the ML model + scaler once, at Django startup, so the
        # first prediction request doesn't pay a cold-load cost and so any
        # missing-artifact errors surface immediately instead of on first use.
        from ml import predictor  # noqa: F401
