from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse

import utils
import os
from forms import UploadFileForm
import settings

#Optional dependecy for image_actions
try:
    from PIL import Image
except:
    pass


@login_required
@staff_member_required
def base(request):
    c = RequestContext(request, {
        'settings': settings.JSON,
        'root': reverse("bfm_base")
    })
    return render_to_response('django_bfm/base.html', c)


def admin_options(request):
    opt = {
        "updir": settings.ADMIN_UPDIR,
        "upload": reverse("bfm_upload")
    }
    options = "BFMAdminOptions = " + simplejson.dumps(opt) + ";"
    return HttpResponse(options)


@login_required
@staff_member_required
def list_files(request):
    directory = request.GET.get('directory', '')
    storage = utils.Directory(directory)
    files = storage.collect_files()
    return HttpResponse(simplejson.dumps(files))


@login_required
@staff_member_required
def list_directories(request):
    storage = utils.Directory('')
    d = storage.collect_dirs()
    return HttpResponse(simplejson.dumps(d))


@login_required
@staff_member_required
def file_actions(request):
    directory = request.GET.get('directory', False)
    f = request.GET.get('file', False)
    if directory == False or f == False:
        return HttpResponse(simplejson.dumps(False))
    storage = utils.Directory(directory)
    if request.GET.get('action', False) == 'delete':
        storage.s.delete(f)
    elif request.GET.get('action', False) == 'touch':
        os.utime(storage.s.path(f), None)
    elif request.GET.get('action', False) == 'rename':
        new_name = request.GET.get('new', False)
        if new_name == False:
            return HttpResponse(simplejson.dumps(False))
        else:
            os.rename(storage.s.path(f), storage.s.path(new_name))
    else:
        return HttpResponse(simplejson.dumps(False))
    return HttpResponse(simplejson.dumps(True))


@login_required
@staff_member_required
def file_upload(request):
    directory = request.GET.get('directory', False)
    if directory == False or not request.method == 'POST':
        return HttpResponse(simplejson.dumps(False))
    else:
        form = UploadFileForm(request.POST, request.FILES)
        storage = utils.Directory(directory)
        if form.is_valid():
            f = storage.s.save(request.FILES['file'].name,
                                                        request.FILES['file'])
            resp = {"filename": f, "url": storage.s.url(f)}
            return HttpResponse(simplejson.dumps(resp))
        return HttpResponse(simplejson.dumps(False))


@login_required
@staff_member_required
def image_actions(request):
    if not 'Image' in globals():
        return HttpResponse(simplejson.dumps('Please install PIL!'))
    directory = request.GET.get('directory', False)
    f = request.GET.get('file', False)
    if directory == False or f == False:
        return HttpResponse(simplejson.dumps(False))
    storage = utils.Directory(directory)
    fpath = storage.s.path(f)
    if request.GET.get('action', False) == 'info':
        image = Image.open(fpath)
        s = image.size
        return HttpResponse(simplejson.dumps({'height': s[1], 'width': s[0]}))
    if request.GET.get('action', False) == 'resize':
        image = Image.open(fpath)
        filtr = getattr(Image, request.GET['filter'])
        size = (int(request.GET['new_w']), int(request.GET['new_h']))
        image = image.resize(size, filtr)
        image.save(storage.s.path(storage.s.get_available_name(f)))
    return HttpResponse(simplejson.dumps(True))
