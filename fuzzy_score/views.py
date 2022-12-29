from django.shortcuts import render
from django.http import HttpResponse
from .models import PPIScore, scores_for_threshold, SCORE_THRESHOLDS


def index(request):
    print(request.GET)
    prot1 = request.GET.get("protein1", "")
    prot2 = request.GET.get("protein2", "")
    context = {
        "ppi_score": None,
        "prot1": prot1,
        "prot2": prot2,
    }
    if prot1 and prot2:
        try:
            ppi_score = PPIScore.objects.get(protein1=prot1, protein2=prot2)
            context["ppi_score_value"] = ppi_score.score
            res_row_values, i = scores_for_threshold(ppi_score.score)
            context.update(res_row_values)
            context["tab"] = SCORE_THRESHOLDS[1:]
            context["i"] = i
        except PPIScore.DoesNotExist:
            pass
    return render(request, 'fuzzy_score/index.html', context)

