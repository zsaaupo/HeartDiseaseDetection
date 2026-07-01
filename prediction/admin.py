from django.contrib import admin

from .models import PredictionRecord


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "get_prediction_display_label", "probability_percent", "risk_level")
    list_filter = ("risk_level", "prediction")
    ordering = ("-created_at",)
    readonly_fields = [f.name for f in PredictionRecord._meta.fields]

    def has_add_permission(self, request):
        # Records should only ever be created via the prediction workflow.
        return False
