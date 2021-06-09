from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .form import ApplyForm, JobForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from.models import Job, Category
from django.contrib.auth.decorators import login_required
from .filters import JobFilter
# Create your views here.


def job_list(request):
    job_list = Job.objects.all()
    #filter pour la recherche
    myfilter = JobFilter(request.GET, queryset=job_list)
    job_list = myfilter.qs

    # afficher les postes de travails dans page HTML
    paginator = Paginator(job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

 
    
    context = {'jobs': page_obj, 'all_jobs': job_list,'myfilter':myfilter}
    return render(request, 'job/job_list.html', context)


def job_detail(request, slug):
    job_detail = Job.objects.get(slug=slug)

    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():

            myform = form.save(commit=False)
            myform.job = job_detail
            myform.save()
            return HttpResponseRedirect('/jobs/')

    else:
        form = ApplyForm()

    context = {'job': job_detail, 'form': form}
    return render(request, 'job/job_detail.html', context)


@login_required
def add_job(request):
    
    if request.method== 'POST':
        form=JobForm(request.POST, request.FILES)
        if form.is_valid():
            myform=form.save(commit=False)
            myform.owner= request.user
            myform.save()
            return redirect(reverse('jobs:job_list'))
        
    else:
        form =JobForm()


    return render(request, 'job/add_job.html',{'form':form})
    
    

   
