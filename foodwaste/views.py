from django.shortcuts import render, redirect
from .forms import FoodEntryForm
from .models import FoodEntry, Dish, DishReport
from django.contrib import messages
from django.db.models import Avg, Sum
from collections import defaultdict
import json  

def home_view(request):
    return render(request, 'foodwaste/home.html')

def food_entry_view(request):
    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your food entry has been submitted.")
            return redirect('home')  # 👈 Redirect to homepage
    else:
        form = FoodEntryForm()

    return render(request, 'foodwaste/food_entry.html', {'form': form})

WASTE_MAP = {
    'None': 0,
    'Some': 1,
    'Lot': 2,
}

def report_view(request):
    entries = FoodEntry.objects.all()
    report_data = defaultdict(lambda: {"total_waste": 0, "ratings": [], "count": 0})

    for entry in entries:
        dish_name = entry.dish.name.capitalize()
        waste_value = WASTE_MAP.get(entry.waste_amount, 0)
        report_data[dish_name]["total_waste"] += waste_value
        report_data[dish_name]["ratings"].append(entry.rating)
        report_data[dish_name]["count"] += 1

    formatted_report = []
    for dish, data in report_data.items():
        ratings = data["ratings"]
        avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
        waste_pct = round((data["total_waste"] / (2 * data["count"])) * 100) if data["count"] > 0 else 0

        formatted_report.append({
            "dish": dish,
            "total_waste": waste_pct,
            "average_rating": avg_rating,
        })

    formatted_report.sort(key=lambda x: x["average_rating"], reverse=True)

    return render(request, "foodwaste/report.html", {
        "report_data": formatted_report,
        "report_data_json": json.dumps(formatted_report)  # 👈 JSON for JS
    })


def full_report_view(request):
    entries = FoodEntry.objects.all().order_by('-date')  # 👈 fixed here
    return render(request, "foodwaste/full_report.html", {"entries": entries})





