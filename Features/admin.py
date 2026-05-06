from django.contrib import admin
from .models import HeartDiseaseFeature

@admin.register(HeartDiseaseFeature)
class HeartDiseaseFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'sex', 'target', 'max_heart_rate', 'st_depression')
    list_filter = ('sex', 'target', 'chest_pain_type')
    search_fields = ('age',)
