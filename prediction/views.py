from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from ml.predictor import predict_patient

from .forms import HeartDiseasePredictionForm
from .models import PredictionRecord


@require_http_methods(["GET", "POST"])
def prediction_form_view(request):
    """Step 1: render the prediction form, and on submit run the model and
    redirect to the result page (Post/Redirect/Get pattern)."""
    if request.method == "POST":
        form = HeartDiseasePredictionForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            # Map the form fields to the exact feature names the saved
            # scaler/model were fitted with.
            model_input = {
                "Thalassemia": cleaned["thalassemia"],
                "Chest_Pain_Type": cleaned["chest_pain_type"],
                "Major_Vessels": cleaned["major_vessels"],
                "ST_Depression": cleaned["st_depression"],
                "Exercise_Induced_Angina": cleaned["exercise_induced_angina"],
                "Max_Heart_Rate": cleaned["max_heart_rate"],
                "ST_Slope": cleaned["st_slope"],
                "Age": cleaned["age"],
                "Sex": cleaned["sex"],
                "Resting_ECG": cleaned["resting_ecg"],
            }

            result = predict_patient(model_input)

            record = PredictionRecord.objects.create(
                age=cleaned["age"],
                sex=cleaned["sex"],
                chest_pain_type=cleaned["chest_pain_type"],
                resting_ecg=cleaned["resting_ecg"],
                max_heart_rate=cleaned["max_heart_rate"],
                exercise_induced_angina=cleaned["exercise_induced_angina"],
                st_depression=cleaned["st_depression"],
                st_slope=cleaned["st_slope"],
                major_vessels=cleaned["major_vessels"],
                thalassemia=cleaned["thalassemia"],
                prediction=result["prediction"],
                probability=result["probability"],
                risk_level=result["risk_level"],
            )

            return redirect("prediction:result", pk=record.pk)
    else:
        form = HeartDiseasePredictionForm()

    return render(request, "prediction/form.html", {"form": form})


def result_view(request, pk):
    """Step 2: dedicated result page for a single prediction record."""
    record = get_object_or_404(PredictionRecord, pk=pk)
    return render(request, "prediction/result.html", {"record": record})


def history_detail_view(request, pk):
    """Read-only detail view of a past prediction (from the history table)."""
    record = get_object_or_404(PredictionRecord, pk=pk)
    return render(request, "prediction/history_detail.html", {"record": record})


@require_http_methods(["POST"])
def history_delete_view(request, pk):
    record = get_object_or_404(PredictionRecord, pk=pk)
    record.delete()
    messages.success(request, "Prediction record deleted successfully.")
    return redirect("dashboard:dashboard")
