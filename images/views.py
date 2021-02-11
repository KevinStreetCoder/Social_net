from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action

@login_required
def image_create(request):
    if request.method == "POST":
        #means form is save
        form = ImageCreateForm(data = request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            #assign current user to the item
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, "Image was added successfully")

            #redirect to new created item details
            return redirect(new_item.get_absolute_url())

    else:
        #build form data provided by the bookmarker via GET
        form = ImageCreateForm(data = request.GET)
    return render(request,
                    'images/image/create.html',
                  {'section': 'images', 
                    'form': form}
                                )

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)     
    return render(request,
                  'images/image/detail.html',                   
                  {'section': 'images',                    
                  'image': image})
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get("action")
    if image_id and action:
        try: 
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user,'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})   

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an interger deliver first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            #if the request is AJAX and the page is out of range
            #return an empty page
            return HttpResponse
        #if page out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                        "images/image/list_ajax.html",
                        {
                            'section':'images',
                            'images': images
                        }
        )
    return render(request,
                    "images/image/list.html",
                    {
                        'section':'images',
                        'images': images
                     }
        ) 

