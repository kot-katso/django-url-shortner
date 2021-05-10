from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .utils import isValidURL

from hashlib import md5

from .models import Url


# Create your views here.
def home(request):

    # create a dict for store
    rq_old_input = []

    try:
        # try to get the old input via  the session
        old_input = request.session['old_input']
        # if old input
        if old_input:
            rq_old_input = old_input
    except KeyError:
        pass

    context = {
        'rvalues': rq_old_input 
    }   

    if "old_input" in request.session.keys():
        del request.session["old_input"]

    return render(request, 'index.html', context)


def shortner(request, hash_cd):
    is_vlaid = get_object_or_404(Url, hash_code=hash_cd)

    return redirect(is_vlaid.actual_url)
    

def list_url(request):
    urls = Url.objects.all().order_by('-created_at')

    context = {
        'urls': urls
    }

    return render(request, 'list.html', context)


def edit_url(request, pk):

    if request.method == 'POST':
        
        # get the url 
        url = request.POST['url']

        # get pk 
        pk = request.POST['pk']

        req_url = Url.objects.filter(pk=pk)

        if not req_url:

            messages.error(request, 'There is something wrong!')
            return redirect('/edit/' + pk)
        
        else:

             # check the url is vlaid 
            if(isValidURL(url) == False):
                request.session['old_input'] = request.POST
                messages.error(request, 'Url is invalid!')
                return redirect('/edit/' + pk)

            # create the url
            host = request.get_host()
            random_code = md5(url.encode()).hexdigest()[:10] 

            hash_link = 'http://'+host+'/shortner/'+random_code

            Url.objects.filter(pk=pk).update(actual_url=url, hash_url=hash_link, hash_code=random_code)

            request.session['old_input'] = ''

            messages.success(request, 'Edited Successfully!')
            return redirect('list_url')


    obj = get_object_or_404(Url, pk=pk)

    # create a dict for store
    rq_old_input = []

    try:
        # try to get the old input via  the session
        old_input = request.session['old_input']
        # if old input
        if old_input:
            rq_old_input = old_input
    except KeyError:
        pass

    context = {
        'url': obj,
        'rvalues': rq_old_input 
    }

    if "old_input" in request.session.keys():
        del request.session["old_input"]


    return render(request, 'edit_url.html', context)

@require_http_methods(["POST"])
def create_url(request):

    # get the url 
    url = request.POST['url']


    # check the url is vlaid 
    if(isValidURL(url) == False):
        messages.error(request, 'Url is invalid!')
        request.session['old_input'] = request.POST
        return redirect('home')

    # create the url in the database
    host = request.get_host()
    random_code = md5(url.encode()).hexdigest()[:10] 

    hash_link = 'http://'+host+'/shortner/'+random_code

    create = Url(actual_url=url, hash_url=hash_link, hash_code=random_code)
    create.save()
    request.session['old_input'] = ''
    messages.success(request, 'Created Successfully!')

    return redirect('home')

@require_http_methods(["POST"])
def delete_url(request):
    url = get_object_or_404(Url, pk=request.POST['pk'])
    url.delete()
    messages.success(request, 'Deleted Successfully!')

    return redirect('list_url')
