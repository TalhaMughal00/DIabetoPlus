from django.contrib import admin
from predictor.models import Predictions
from Glucose_Record.models import GRecords
from Home.models import feedback

class PredictionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'bmi', 'blood_glucose_level', 'prediction_result', 'date')
admin.site.register(Predictions, PredictionsAdmin)

class GRecordsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date','mor_fast','mor_after','evening','night_fast','night_after')
admin.site.register(GRecords, GRecordsAdmin)

class feedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feed', 'created_at')
    search_fields = ['feed']
admin.site.register(feedback, feedbackAdmin)