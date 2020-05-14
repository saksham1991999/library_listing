
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

#
# longitude = 77.03179
# latitude = 25.470804
# user_location = Point(longitude, latitude)
# distance = 2000
#
# class Home(generic.ListView):
#     model = library
#     context_object_name = 'shops'
#     #queryset = library.objects.annotate(distance=Distance('location',user_location)).order_by('distance')
#     # queryset = library.objects.annotate(distance=user_location.distance('location')).order_by('distance')
#     template_name = 'libraries.html'
#     # queryset = library.objects.filter(location__distance_lte=(user_location, D(m=distance))).distance(user_location).order_by('distance')
#     libraries = library.objects.all()
#     print(libraries)
#     distance2 = Distance(libraries[0].location, libraries[1].location)
#     distance3 = libraries[1].location.distance(libraries[8].location)
#     print(distance3)
#
# def HomeView(request):
#     libraries = library.objects.all()
#     distance = 2000
#     ref_location = Point(77.03179, 25.470804, srid=4326)
#     ref_location = GEOSGeometry('SRID=4326;POINT(77.03179 25.470804)')
#     # libraries = library.objects.filter(location__distance_lte=(ref_location, D(m=distance))).distance(
#     #     ref_location).order_by('distance')
#
#     # libraries = library.objects.filter(location__distance_lte=(ref_location, D(m=200000))).annotate(distance=Distance("location", ref_location)).order_by("distance")
#     libraries = library.objects.annotate(distance=Distance("location", ref_location))
#
#     for library_ref in libraries:
#         distance = library_ref.location.distance(ref_location)
#         print(distance)
#     print(libraries)
#     context = {
#         'libraries':libraries,
#     }
#     return render(request, 'libraries.html', context)
#
# def AddLibraryView(request):
#     libraryform = forms.LibraryForm
#
#     context = {
#         'libraryform':libraryform,
#     }
#     return render(request, 'addlibrary.html', context)
#
#
# # res = yourmodel.objects.filter(location__distance_lte=(ref_location, D(m=distance))).distance(ref_location).order_by('distance')
#
# def Testing(request):
#     print()
#
#

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

from . import models, forms
from blog.models import post

def HomeView(request):
    if request.method == 'POST':
        print('-------------------POIST REQUEST-------------------')
        print(request.POST)
        email = request.POST['email']
        newsletter_qs = models.newsletter.objects.create(email=email)
        if request.user.is_authenticated:
            newsletter_qs.name = request.user.username
        newsletter_qs.save()
        return redirect('core:home')
    else:
        libraries = models.library.objects.all()[:6]
        blogposts = post.objects.all()[:3]
        testimonials = models.testimonial.objects.all()[:3]
        cities = models.library.objects.all().values_list('city', flat=True).distinct()
        context = {
            'libraries': libraries,
            'blogposts':blogposts,
            'testimonials':testimonials,
            'cities':cities,
        }
        return render(request, 'index.html', context)

def LibrariesView(request):
    allLibraries = models.library.objects.all()
    amenities = models.ammenities.objects.all()
    search_term = ''
    city = ''

    ref_location = GEOSGeometry('SRID=4326;POINT(77.03922300000001 28.45692)')


    for i in range(10):
        print()
    print(request.GET)

    if 'city' in request.GET:
        city = request.GET['city']
        allLibraries = allLibraries.filter(city__icontains=city)

    if 'seats' in request.GET:
        seats = request.GET['seats']
        allLibraries = allLibraries.filter(no_of_seats=seats)

    if 'search' in request.GET:
        search_term = request.GET['search']
        allLibraries = allLibraries.filter(name__icontains=search_term)



    if 'latitude' in request.GET and 'longitude' in request.GET:
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        ref_location = GEOSGeometry('SRID=4326;POINT('+str(latitude)+' ' + str(longitude) +')')

    allLibraries = models.library.objects.annotate(distance=Distance("location", ref_location)).order_by('distance')[
                   0:6]
    paginator = Paginator(allLibraries, 25)
    page = request.GET.get('page')
    allLibraries = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    context = {
        'libraries': allLibraries,
        'params': params,
        'search_term': search_term,
        'amenities': amenities,
        'city': city,
    }
    return render(request, 'libraries.html', context)

def ContactView(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            print('Form saved Successfully')
            messages.success(
                request,
                'Message sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
        else:
            print(form.errors)
            print('form not valid')
        return redirect('core:contact')
    else:
        form = forms.ContactForm()
        context = {
            'contactform': form,
        }
        return render(request, 'contact.html', context)

def LibraryView(request, id):
    library = get_object_or_404(models.library, id = id)
    library.views = int(library.views + 1)
    library.save()
    images = models.library_images.objects.filter(library=library)
    ammenities = library.ammenities.all()
    payment_methods = library.payment_methods.all()

    if request.method == 'POST':
        form = forms.EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Enquiry sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('core:library', id)
        else:
            return redirect('core:library', id)

    else:
        enquiryform = forms.EnquiryForm()
        context = {
            'library': library,
            'images': images,
            'ammenties': ammenities,
            'payment_methods':payment_methods,
            'enquiryform': enquiryform,

        }
        # if request.user.is_authenticated():
        # bookmarkedlibraries = models.bookmark.objects.filter(user=request.user)[0]
        # bookmarkedlibraries = bookmarkedlibraries.libraries
        #
        # comparinglibraries = models.comparison.objects.filter(user=request.user)[0]
        # comparinglibraries = comparinglibraries.libraries
        # context['bookmarkedlibraries'] = bookmarkedlibraries
        # context['comparinglibraries'] = comparinglibraries
        return render(request, 'library.html', context)

def BugReportView(request):
    if request.method == 'POST':
        form = forms.BugReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Enquiry sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('core:reportbug')
        else:
            print(form.errors)
            return redirect('core:reportbug')

    else:
        bugreportform = forms.BugReportForm()
        context = {
            'bugreportform': bugreportform,
        }
        return render(request, 'reportbug.html', context)

def TestimonialsView(request):
    if request.method == 'POST':
        form = forms.TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Enquiry sent Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
            return redirect('core:testimonial')
        else:
            print(form.errors)
            return redirect('core:testimonial')
    else:
        testimonialform = forms.TestimonialForm()
        context = {
            'testimonialform': testimonialform,
        }
        return render(request, 'testimonialform.html', context)

def FAQView(request):
    faqs = models.faq.objects.all()
    context = {
        'faqs':faqs,
    }
    return render(request, 'faq.html', context)

def FAQDetailView(request, id):
    faq = get_object_or_404(models.faq, id=id)
    context = {
        'faq':faq,
    }
    return render(request, 'faqdetail.html', context)

@login_required
def UserProfileView(request):
    if request.method == "POST":
        print(request)
        user = models.User(email=request.user.email)
        form = forms.UserProfileForm(request.POST, instance=request.user)
        # fname = form[]
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Changes Saved Successfully',
                extra_tags='alert alert-success alert-dismissible fade show'
            )
        return redirect('core:userprofile')
    else:
        form = forms.UserProfileForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'dashboard/userprofile.html', context)

@login_required
def myLibraries(request):
    libraries = models.library.objects.filter(owner = request.user)
    context = {
        'libraries': libraries,
    }
    return render(request, 'dashboard/mylibraries.html', context)

@login_required
def editLibrary(request, id):
    library = get_object_or_404(models.library, id=id)
    if library.owner == request.user:
        if request.method == 'POST':
            form = forms.LibraryForm(request.POST, instance=library)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'library Details Saved Successfully',
                    extra_tags='alert alert-success alert-dismissible fade show'
                )
                return redirect('core:mylibraries')
            else:
                return redirect('core:editlibrary', id)
        else:
            form = forms.LibraryForm(instance=library)
            context = {
                'form': form,
            }
            return render(request, 'dashboard/addlibrary.html', context)
    else:
        messages.success(
            request,
            'You are not allowed to edit the library Details',
            extra_tags='alert alert-success alert-dismissible fade show'
        )
        return redirect('core:mylibraries')

@login_required
def addLibrary(request):
    # user = models.User.objects.get(email = request.user.email)
    if request.method == "POST":
        print(request)
        form = forms.LibraryForm(request.POST, request.FILES)

        imagesform = forms.ImagesForm(request.POST, request.FILES)
        uploadedimages = request.FILES.getlist('image')
        print(imagesform)

        longitude = 77.03179
        latitude = 25.470804
        lib_location = Point(longitude, latitude)
        print(form.errors)
        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.owner = request.user
            new_form.location = lib_location
            new_form.save()

            if imagesform.is_valid():
                for image in uploadedimages:
                    imageinput = models.library_images(library=new_form, image = image)
                    imageinput.save()

            messages.success(
                            request,
                            'Library Added Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('core:mylibraries')

    form = forms.LibraryForm()
    imagesform = forms.ImagesForm()
    context = {
        'form': form,
        'imagesform': imagesform,
    }
    return render(request, 'dashboard/addlibrary.html', context)

@login_required
def deleteLibrary(request, id):
    library = get_object_or_404(models.library, id = id )
    if library.owner == request.user:
        library.delete()
        messages.success(
            request,
            'library Deleted Successfully',
            extra_tags='alert alert-success alert-dismissible fade show'
        )
    else:
        messages.error(
            request,
            'You can not delete the library',
            extra_tags='alert alert-danger alert-dismissible fade show'
        )
    return redirect('core:mylibraries')

@login_required
def hideLibrary(request, id):
    library = get_object_or_404(models.library, id=id)
    if library.owner == request.user:
        library.visible = False
        library.save()
    return redirect('core:mylibraries')

@login_required
def showLibrary(request, id):
    library = get_object_or_404(models.library, id=id)
    if library.owner == request.user:
        library.visible = True
        library.save()
    return redirect('core:mylibraries')

@login_required
def BookmarkView(request):
    bookmarks = models.bookmark.objects.filter(user=request.user).first()
    context = {
        'bookmark': bookmarks,
    }
    return render(request, 'dashboard/bookmarks.html', context)

@login_required
def add_to_bookmark(request, id):
    library = get_object_or_404(models.library, id = id)
    bookmark_qs = models.bookmark.objects.filter(user = request.user)
    if bookmark_qs.exists():
        bookmark = bookmark_qs[0]
        if bookmark.libraries.filter(id = id).exists():
            messages.info(request, "library Already Bookmarked")
        else:
            bookmark.libraries.add(library)
            messages.info(request, "Successfully Bookmarked")
    else:
        bookmark = models.bookmark.objects.create(user=request.user)
        bookmark.libraries.add(library)
        messages.info(request, "Successfully Bookmarked")
    return redirect("core:bookmarks")

@login_required
def remove_from_bookmark(request, id):
    library = get_object_or_404(models.library, id = id)
    bookmark_qs = models.bookmark.objects.filter(user = request.user)
    if bookmark_qs.exists():
        bookmark = bookmark_qs[0]
        if bookmark.libraries.filter(id = id).exists():
            bookmark.libraries.remove(library)
            messages.info(request, "library removed from your Bookmarks")
    else:
        messages.info(request, "library does not exist in your Bookmarks")
    return redirect("core:bookmarks")


def ComparisonView(request):
    if 'compare' in request.session:
        print('----------- COMPARE VIEW -----------------')
        print(request.session['compare'])
        libraries =  models.library.objects.all()
        library_ids = request.session['compare']
        if len(library_ids) > 1:
            library1 = None
            library2 = None
            library3 = None
            library_ids = library_ids[-3:]
            print(library_ids)
            try:
                library1 = models.library.objects.get(id = library_ids[0])
            except:
                pass
            try:
                library2 = models.library.objects.get(id = library_ids[1])
            except:
                pass
            try:
                library3 = models.library.objects.get(id = library_ids[2])
            except:
                pass
            print(library1, library2, library3)
            ammenities = models.ammenities.objects.all()
            context = {
                'libraries': libraries,
                'library1': library1,
                'library2': library2,
                'library3': library3,
                'ammenities': ammenities,
            }
            return render(request, 'dashboard/comparelibraries.html', context)
    return redirect('core:libraries')


    compare_qs = models.comparison.objects.filter(user=request.user)
    if compare_qs.exists():
        compare_qs = compare_qs[0]
        libraries = compare_qs.libraries.all()
        if len(libraries) > 1:
            library1 = None
            library2 = None
            library3 = None
            try:
                library1 = libraries[0]
            except:
                pass
            try:
                library2 = libraries[1]
            except:
                pass
            try:
                library3 = libraries[2]
            except:
                pass

            ammenities = models.ammenities.objects.all()
            context = {
                'libraries': libraries,
                'library1':library1,
                'library2':library2,
                'library3':library3,
                'ammenities':ammenities,
            }
            return render(request, 'dashboard/comparelibraries.html', context)
        else:
            messages.info(request, "You just have 1 Library in Compare List")
            return redirect('core:libraries')
    else:
        messages.info(request, "Add to libraries to Compare list to compare")
        return redirect('core:libraries')


def add_to_compare(request, id):
    library = get_object_or_404(models.library, id = id)
    print(request.session)
    if 'compare' in request.session:
        print('-------------ALREADY HAVE LIBRARIES TO COMPARE')
        library_ids = request.session['compare']
        library_ids.append(id)
        request.session['compare'] = library_ids
        print(request.session['compare'])
    else:
        request.session['compare'] = [id]
    return redirect('core:compare')


def remove_from_compare(request, id):
    library_ids = request.session['compare']
    library_ids.remove(id)
    request.session['compare'] = library_ids
    return redirect('core:compare')

def TandCView(request):
    context = {}
    return render(request, 't&c.html', context)

def PrivacyPolicyView(request):
    context = {}
    return render(request, 'privacypolicy.html', context)


'''
#API
class AmmenitiesView(viewsets.ModelViewSet):
    queryset = models.ammenities.objects.all()
    serializer_class = serializers.AmmenitiesSerializer

class PaymentMethodsView(viewsets.ModelViewSet):
    queryset = models.payment_methods.objects.all()
    serializer_class = serializers.PaymentMethodsSerializer


class LibraryView(viewsets.ModelViewSet):
    queryset = models.library.objects.all()
    serializer_class = serializers.LibrarySerializer

class library_detail(viewsets.ModelViewSet):
    queryset = models.library.objects.all()
    serializer_class = serializers.LibrarySerializer
'''