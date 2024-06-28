from django.shortcuts import render, redirect, HttpResponse
from app.models import Student, Staff, LostItem, FoundItem
from django.core.files.storage import default_storage
from django.conf import settings
import os
from django.db.models import Q



def home(request):
    if request.method == 'GET':
        return render(request, 'welcome.html')


def registration(request):
    user_id = request.session.get('user_id',None)
    if user_id is not None:
        return redirect('dashboard')

    if request.method == 'GET':
        return render(request, 'registration.html',{'current_user_type':'student','roll_number':'','password':''})

    if request.method == 'POST' and request.POST['user'] == 'student':
        roll_number = request.POST.get('roll_number')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(roll_number=roll_number)
        except Student.DoesNotExist:
            return render(request,'registration.html',{'roll_number_error': True, 'current_user_type':'student','roll_number':roll_number, 'password':password})
        if student.created:
            return render(request,'registration.html',{'account_exists':True, 'current_user_type':'student'})
        student.password = password
        student.created = True
        student.save()
        request.session['account_created'] = True
        return redirect('account_created_successfully')

    if request.method == 'POST' and request.POST['user'] == 'staff':
        staff_d = request.POST.get('roll_number')
        password = request.POST.get('password')
        try:
            staff = Staff.objects.get(staff_id=staff_d)
        except Staff.DoesNotExist:
            return render(request,'registration.html',{'staff_id_error': True , 'current_user_type':'staff'})
        if staff.created:
            return render(request,'registration.html',{'staff_account_exists':True , 'current_user_type':'staff'})
        staff.password = password
        staff.created = True
        staff.save()
        request.session['account_created'] = True
        return redirect('account_created_successfully')


def account_created_successfully(request):
    if request.session.get('account_created'):
        del request.session['account_created']
        return render(request, 'account_created.html')
    else:
        return redirect('registration')



def login(request):
    user_id = request.session.get('user_id', None)
    if user_id is not None:
        return redirect('dashboard')

    if request.method == 'GET':
        return render(request, 'login.html', {'current_user_type':'student'})
    
    user_type = request.POST['user']
    if request.method == 'POST' and user_type == 'student':
        roll_number = request.POST['roll_number']
        password = request.POST['password']
        try:
            student = Student.objects.get(roll_number=roll_number, password=password)
        except Student.DoesNotExist:
            return render(request, 'login.html', {'current_user_type':'student', 'student_credential_error':True})
        request.session['user_id'] = student.id
        request.session['user-type'] = 'student'
        return redirect('dashboard')

    if request.method == 'POST' and user_type == 'staff':
        staff_id = request.POST['staff_id']
        password = request.POST['password']
        try:
            staff = Staff.objects.get(staff_id=staff_id, password=password)
        except Student.DoesNotExist:
            return render(request, 'login.html', {'current_user_type':'staff', 'staff_credential_error':True})
        request.session['user_id'] = staff.id
        request.session['user-type'] = 'staff'
        return redirect('dashboard')



def dashboard(request):
    user_id = request.session.get('user_id', None)
    if user_id == None:
        return redirect('login')
    else:
       return render(request, 'dashboard.html')




def my_account(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id == None:
            return redirect('login')
        
        user_type = request.session.get('user-type', None)
        if user_type == 'student':
            user = Student.objects.get(pk=user_id)
        if user_type == 'staff':
            user = Staff.objects.get(pk=user_id)
        return render(request, 'my_account.html', {'phone_number':user.phone_number})
    
    if request.method == 'POST' and request.POST['purpose'] == 'change-password':
        user = Student.objects.get(pk=request.session.get('user_id'))
        user.password = request.POST['confirm-password']
        user.save()
        return redirect('my_account')

    if request.method == 'POST' and request.POST['purpose'] == 'change-phone-number':
        user = Student.objects.get(pk=request.session.get('user_id'))
        user.phone_number = request.POST['new-phone']
        user.save()
        return redirect('my_account')




def report_lost_item(request):
    user_id = request.session.get('user_id', None)
    if user_id == None:
        return redirect('login')

    if request.method == 'GET':
        return render(request, 'report_lost_item.html')

    if request.method == 'POST':
        item_name = request.POST['item-name']
        item_description = request.POST['item-description']
        item_category = request.POST['item-category']
        lost_location = request.POST['location-lost']
        contact_information = request.POST['contact-info']
        
        uploaded_file = request.FILES['item-image']
        file_name = default_storage.get_available_name(uploaded_file.name)
        file_path = os.path.join(os.path.join(settings.MEDIA_ROOT,'lost_item_images'), file_name)

        with default_storage.open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        lost_item = LostItem(item_name=item_name, 
                             description=item_description, 
                             category=item_category,
                             location=lost_location,
                             phone=contact_information,
                             image=file_path,
                             user_id=user_id
                             )
        lost_item.save()
        return redirect('manage_report')




def report_found_item(request):
    user_id = request.session.get('user_id', None)
    if user_id == None:
        return redirect('login')
    
    if request.method == 'GET':
        return render(request, 'report_found_item.html')
    
    if request.method == 'POST':
        item_name = request.POST['item-name']
        item_description = request.POST['item-description']
        item_category = request.POST['item-category']
        lost_location = request.POST['location-lost']
        contact_information = request.POST['contact-info']
        
        uploaded_file = request.FILES['item-image']
        file_name = default_storage.get_available_name(uploaded_file.name)
        file_path = os.path.join(os.path.join(settings.MEDIA_ROOT,'found_item_images'), file_name)

        with default_storage.open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        found_item = FoundItem(item_name=item_name, 
                             description=item_description, 
                             category=item_category,
                             location=lost_location,
                             phone=contact_information,
                             image=file_path,
                             user_id=user_id
                             )
        found_item.save()
        return redirect('manage_report')




def search_lost_item(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id == None:
            return redirect('login')
        
        founds = FoundItem.objects.exclude(user_id=user_id)
        return render(request, 'search_lost_item.html', {'founds':founds})
    
    if request.method == 'POST':
            search_term = request.POST['search-term']
            user_id = request.session.get('user_id', None)
            founds = FoundItem.objects.filter(~Q(user_id=user_id),
                                             Q(item_name__icontains=search_term) | Q(category__icontains=search_term) | Q(description__icontains=search_term))
            return render(request, 'search_lost_item.html', {'founds':founds})




def manage_report(request):
    user_id = request.session.get('user_id', None)
    if user_id == None:
        return redirect('login')

    user_id = request.session['user_id']
    lostitems = LostItem.objects.filter(user_id=user_id)
    founditems = FoundItem.objects.filter(user_id=user_id)
    return render(request, 'manage_reports.html', {'lostitems':lostitems, 'founditems':founditems})


def edit_lost_item(request, item_id):
    if request.method == 'GET':
        try:
            lost_item = LostItem.objects.get(id=item_id, user_id=request.session['user_id'])
        except:
            return redirect('manage_report')
        return render(request, 'edit_lost_item.html', {'lost_item':lost_item})
    
    if request.method == 'POST':
        item = LostItem.objects.get(id=item_id)
        item.item_name = request.POST['item-name']
        item.description = request.POST['item-description']
        item.category = request.POST['item-category']
        item.location = request.POST['location-lost']
        item.phone = request.POST['contact-info']
        item.save()
        return redirect('manage_report')



def edit_found_item(request, item_id):
    if request.method == 'GET':
        try:
            found_item = FoundItem.objects.get(id=item_id, user_id=request.session['user_id'])
        except:
            return redirect('manage_report')
        return render(request, 'edit_found_item.html', {'found_item':found_item})
    
    if request.method == 'POST':
        item = FoundItem.objects.get(id=item_id)
        item.item_name = request.POST['item-name']
        item.description = request.POST['item-description']
        item.category = request.POST['item-category']
        item.location = request.POST['location-lost']
        item.phone = request.POST['contact-info']
        item.save()
        return redirect('manage_report')
  


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('login')



def delete_item(request):
    if request.method == 'POST':
        if request.POST['item-type'] == 'lost':
            LostItem.objects.filter(id=request.POST['item-id']).delete()
        if request.POST['item-type'] == 'found':
            FoundItem.objects.filter(id=request.POST['item-id']).delete()
        return redirect('manage_report')









