import json

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render

from prediction.models import PredictionRecord


def dashboard_view(request):
    all_records = PredictionRecord.objects.all()

    total_predictions = all_records.count()
    positive_predictions = all_records.filter(prediction=1).count()
    negative_predictions = all_records.filter(prediction=0).count()

    recent_records = all_records[:10]

    # --- Chart 1: Prediction outcome breakdown (Positive vs Negative) ---
    outcome_chart_data = {
        "labels": ["Positive (Heart Disease)", "Negative (No Heart Disease)"],
        "values": [positive_predictions, negative_predictions],
    }

    # --- Chart 2: Risk level breakdown ---
    risk_counts = {"Low": 0, "Medium": 0, "High": 0}
    for row in all_records.values("risk_level").annotate(count=Count("id")):
        risk_counts[row["risk_level"]] = row["count"]

    risk_chart_data = {
        "labels": list(risk_counts.keys()),
        "values": list(risk_counts.values()),
    }

    # --- Chart 3: Predictions over time (by date) ---
    trend_qs = (
        all_records
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )
    trend_chart_data = {
        "labels": [row["date"].strftime("%Y-%m-%d") for row in trend_qs],
        "values": [row["count"] for row in trend_qs],
    }

    context = {
        "total_predictions": total_predictions,
        "positive_predictions": positive_predictions,
        "negative_predictions": negative_predictions,
        "recent_records": recent_records,
        "outcome_chart_json": json.dumps(outcome_chart_data),
        "risk_chart_json": json.dumps(risk_chart_data),
        "trend_chart_json": json.dumps(trend_chart_data),
    }
    return render(request, "dashboard/dashboard.html", context)
