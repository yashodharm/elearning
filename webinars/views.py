from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from pinax.referrals.models import Referral


@login_required
def webinars(request):
    user=request.user
    
    
    
    if request.user.is_site_admin:
        queryset = Webinar.objects.all()
    else:
        queryset = Webinar.objects.filter(for_everybody=True )
        queryset2 = Webinar.objects.filter(students=user)
        

    context = {
        "title": "Webinars",
        "queryset": queryset,
        "queryset2":queryset2,
    }
    if "pinax-referral" in request.COOKIES.keys():
        ref=request.COOKIES['pinax-referral']
        code, session_key=ref.split(':')

        profile = UserProfile.objects.get(username=request.user.username)
        
        if not profile.parent:
            #  print('hi')
            #  print(ref)

            #  print("hi")
             
             refer=Referral.objects.get(code=code)
            #  print(type(refer))
             parent = UserProfile.objects.get(referral=refer)
             profile.parent = parent
             profile.save()

    if "parent" in request.COOKIES.keys():
             profile = UserProfile.objects.get(username=request.user.username)

       
            #  print('hi')
            #  print(ref)

            #  print("hi")
             pare=request.COOKIES['parent']
            
            #  print(type(refer))
             parent = UserProfile.objects.get(username=pare)
             profile.parent = parent
            #  print("hi")
             

             profile.save()
            #  print(profile.parent.username)
            #  print("hi")
        # print(profile.parent)
    return render(request, "users/webinar.html", context)


@user_passes_test(lambda user: user.is_professor)
def webinar(request, webinar_name=None):
    add_Session_form = AddSessionForm(request.POST or None)
    queryset_Session = Session.objects.filter(webinar__webinar_name=webinar_name)
    # for i in queryset_Session:
    #     print(i.webinar.webinar_name)
    
    context = {
        "title": webinar_name,
        "add_Session_form": add_Session_form,
        "queryset_Session": queryset_Session,
        "webinar_name": webinar_name,
        "path": "Profile",
        "redirect_path": "profile",
    }
    
    if add_Session_form.is_valid():
        
        instance = add_Session_form.save(commit=False)
        instance.webinar = Webinar.objects.get(webinar_name=webinar_name)
        instance.save()
        
        return redirect(reverse('professor_webinar', kwargs={'webinar_name': webinar_name}))
    
    return render(request, "webinars/webinar.html", context)


@user_passes_test(lambda user: user.is_professor)
def session(request, webinar_name=None, slug=None):
    place = Session.objects.get(webinar__webinar_name=webinar_name, slug=slug)

    add_link_form = AddLinkForm(request.POST or None)
    add_txt_form = AddTxtForm(request.POST or None)
    add_gdlink_form=AddGDLinkForm(request.POST or None)
    file_upload_form = FileUploadForm(request.POST or None, request.FILES or None)

    queryset_txt_block = TextBlockW.objects.filter(text_block_fk__id=place.id)
    queryset_yt_link = YTLinkW.objects.filter(yt_link_fk__id=place.id)
    queryset_files = FileUploadW.objects.filter(file_fk__id=place.id)
    queryset_gdlink = gdlinkW.objects.filter(gd_link_fk__id=place.id)

    
    context = {
        "title": place.session_name,
        "webinar_name": webinar_name,
        "slug": slug,
        "add_link_form": add_link_form,
        "add_txt_form": add_txt_form,
        "add_gdlink_form": add_gdlink_form,
        "queryset_yt_link": queryset_yt_link,
        "queryset_txt_block": queryset_txt_block,
        "queryset_files": queryset_files,
        "queryset_gdlink": queryset_gdlink, 
        "path": "Profile",
        "redirect_path": "profile",
        "file_upload_form": file_upload_form,
    }

    if add_link_form.is_valid() and 'add_link' in request.POST:
        instance = add_link_form.save(commit=False)
        instance.yt_link_fk = Session.objects.get(id=place.id)

        key = add_link_form.cleaned_data.get("link")

        if 'embed' not in key and 'youtube' in key:
            key = key.split('=')[1]
            instance.link = 'https://www.youtube.com/embed/' + key

        instance.yt_link_fk = Session.objects.get(id=place.id)
        instance.save()
        return redirect(reverse('session', kwargs={'webinar_name': webinar_name,
                                                   'slug': slug}))

    if add_gdlink_form.is_valid() and 'add_gdlink' in request.POST:
        
        instance = add_gdlink_form.save(commit=False)
        instance.gd_link_fk = Session.objects.get(id=place.id)

        instance.gdlink = add_gdlink_form.cleaned_data.get("link")
        instance.save()

        return redirect(reverse('session', kwargs={'webinar_name': webinar_name,
                                                   'slug': slug}))


        
    if add_txt_form.is_valid() and 'add_text' in request.POST:
        instance = add_txt_form.save(commit=False)
        print("hi")
        instance.text_block_fk = Session.objects.get(id=place.id)
        # instance.lesson = add_txt_form.get('lesson')
        instance.save()
        return redirect(reverse('session', kwargs={'webinar_name': webinar_name,
                                                   'slug': slug}))

    if file_upload_form.is_valid() and 'add_file' in request.POST:
        instance = file_upload_form.save(commit=False)
        instance.file_fk = Session.objects.get(id=place.id)
        instance.save()
        return redirect(reverse('session', kwargs={'webinar_name': webinar_name,
                                                   'slug': slug}))

    return render(request, "webinars/Session.html", context)


@user_passes_test(lambda user: user.is_professor)
def delete_webinar(request, webinar_name=None):
    instance = Webinar.objects.get(webinar_name=webinar_name)
    instance.delete()
    return HttpResponseRedirect(reverse('profile'))


@user_passes_test(lambda user: user.is_professor)
def delete_session(request, webinar_name=None, slug=None):
    instance = Session.objects.get(slug=slug)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def delete_yt_link(request, yt_id=None):
    instance = YTLinkW.objects.get(id=yt_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def delete_gd_link(request, gd_id=None):
    instance = gdlinkW.objects.get(id=gd_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def delete_text_block(request, txt_id=None):
    instance = TextBlockW.objects.get(id=txt_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def delete_file(request, file_id=None):
    instance = FileUploadW.objects.get(id=file_id)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def update_webinar(request, webinar_name=None):
    instance = Webinar.objects.get(webinar_name=webinar_name)
    update_webinar_form = EditWebinarForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "form": update_webinar_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_webinar_form.is_valid():
        webinar_name = update_webinar_form.cleaned_data.get("webinar_name")
        instance = update_webinar_form.save(commit=False)
    
        instance.text = update_webinar_form.cleaned_data.get("text")
        key = update_webinar_form.cleaned_data.get("link")

        if 'embed' not in key and 'youtube' in key:
            key = key.split('=')[1]
            instance.link = 'https://www.youtube.com/embed/' + key

        
        instance.save()
        return redirect(reverse('profile'))

    return render(request, "webinars/edit.html", context)


@user_passes_test(lambda user: user.is_professor)
def update_session(request, webinar_name=None, slug=None):
    instance = Session.objects.get(slug=slug)
    update_Session_form = EditSessionForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "webinar_name": webinar_name,
        "form": update_Session_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_Session_form.is_valid():
        update_Session_form.save()
        return redirect(reverse('professor_webinar', kwargs={'webinar_name': webinar_name}))

    return render(request, "webinars/edit.html", context)


@user_passes_test(lambda user: user.is_professor)
def update_yt_link(request, webinar_name=None, slug=None, yt_id=None):
    instance = YTLinkW.objects.get(id=yt_id)
    update_link_form = EditYTLinkForm(request.POST or None, instance=instance)

    context = {
        "title": "Edit",
        "webinar_name": webinar_name,
        "yt_id": yt_id,
        "slug": slug,
        "form": update_link_form,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if update_link_form.is_valid():
        update_link_form.save()
        return redirect(reverse('session', kwargs={'webinar_name': webinar_name,
                                                   "slug": slug}))

    return render(request, "webinars/edit.html", context)


@user_passes_test(lambda user: user.is_professor)
def update_gd_link(request, webinar_name=None, slug=None, gd_id=None):
    instance = gdlinkW.objects.get(id=gd_id)
    update_link_form = EditGDLinkForm(request.POST or None, instance=instance)

    context = {
        "title": "Edit",
        "webinar_name": webinar_name,
        "gd_id": gd_id,
        "slug": slug,
        "form": update_link_form,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if update_link_form.is_valid():
        update_link_form.save()
        return redirect(reverse('Session', kwargs={'webinar_name': webinar_name,
                                                   "slug": slug}))

    return render(request, "webinars/edit.html", context)

@user_passes_test(lambda user: user.is_professor)
def update_text_block(request, webinar_name=None, slug=None, txt_id=None):
    instance = TextBlockW.objects.get(id=txt_id)
    update_txt_form = EditTxtForm(request.POST or None, instance=instance)

    context = {
        "title": "Edit",
        "webinar_name": webinar_name,
        "text_id": txt_id,
        "form": update_txt_form,
        "slug": slug,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if update_txt_form.is_valid():
        update_txt_form.save()
        return redirect(reverse('Session', kwargs={'webinar_name': webinar_name,
                                                   "slug": slug}))

    return render(request, "webinars/edit.html", context)


@user_passes_test(lambda user: user.is_professor)
def list_students_webinar(request, webinar_name=None):
    webinar = Webinar.objects.get(webinar_name=webinar_name)
    added_students = UserProfile.objects.filter(students_to_webinar=webinar)
    excluded_students = UserProfile.objects.exclude(students_to_webinar=webinar).filter(is_professor=False).filter(
        is_site_admin=False)

    query_first = request.GET.get("q1")
    if query_first:
        excluded_students = excluded_students.filter(username__icontains=query_first)

    query_second = request.GET.get("q2")
    if query_second:
        added_students = added_students.filter(username__icontains=query_second)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit students in webinar " + webinar_name,
        "excluded_students": excluded_students,
        "added_students": added_students,
        "webinar_name": webinar_name,
        "path": path,
        "redirect_path": redirect_path,
    }

    return render(request, "webinars/add_students.html", context)


def add_students_webinar(request, student_id, webinar_name=None):
    student = UserProfile.objects.get(id=student_id)
    webinar = Webinar.objects.get(webinar_name=webinar_name)
    webinar.students.add(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def remove_students_webinar(request, student_id, webinar_name=None):
    student = UserProfile.objects.get(id=student_id)
    webinar = Webinar.objects.get(webinar_name=webinar_name)
    webinar.students.remove(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
