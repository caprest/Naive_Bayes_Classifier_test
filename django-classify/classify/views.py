from django.shortcuts import get_object_or_404, render,render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .forms import ClassifyForm
from django.utils import timezone
from .models import URL_LIST
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/apps/machine_learning/')
dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'apps/machine_learning/dictionary_first')

import classifier


def classifying(request):
    if request.method == 'POST': 
        form = ClassifyForm(request.POST) 
        if form.is_valid():             
            url_to_solve = form.cleaned_data["url"]
            url_find = URL_LIST.objects.filter(url=url_to_solve)
            if len(url_find)>0:
                category = url_find[0].category
            else:
                i_classifier = classifier.Classifier(dic_path)
                label = i_classifier.calic_label(url_to_solve)
                category = i_classifier.categories[label]
            q = URL_LIST(url=url_to_solve,pub_date=timezone.now(),category=category)
            q.save()
            id = q.id
            return HttpResponseRedirect('/classify/results/'+str(id) )

        else:
            form = ClassifyForm() 
            error_message = "Error:Please insert URL"
        return render(request,'classify/index.html', {
        'form': form,
        'error_message':error_message
    })
    return render(request,'classify/index.html',{
        'form':ClassifyForm()
    })

def results(request, pk):
    data = get_object_or_404(URL_LIST, pk=pk)
    category = data.category
    url = data.url
    return render(request, 'classify/results.html',
     {'url': url,
     'category':category,
     })