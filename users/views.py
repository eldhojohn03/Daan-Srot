from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from .models import *

def home_view(request):
    set=Transaction.objects.filter(approvefromorg=True,advertise=True)
    donations=[]
    for data in set:
        instance1=Donor.objects.get(username=data.donor_username)
        instance2=Organization.objects.get(username=data.org_username)
        donation={'person':instance1.name,'amount':data.amount,'orgname':instance2.org_name}
        donations.append(donation)
    return render(request, 'home.html', {'donations':donations})

def adminsignup(request):
    logout(request)
    if request.method == 'POST':
        username='admin123'
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = Admin.objects.create_user(username=username,name=name,phone=phone,password=password,usertype='admin')
        user.save()

        return redirect('login-view')
    else:
        return render(request, 'adminsignup.html')

def donorsignup(request):
    if request.method == 'POST' and request.POST['type']!='None':
        donortype = request.POST['type']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = Donor.objects.create_user(username=email,donortype=donortype,name=name,phone=phone,address=address,password=password,usertype='donor')
        user.save()

        return redirect('login-view')
    else:
        return render(request, 'donorsignup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        # instance=Organization.objects.get(username=user)
        # instance.usertype='org'
        # instance.save()
        if user is not None:
            login(request, user)
            # Redirect to a success page or somewhere else
            if user.usertype=='donor':
                return redirect('donor-home')
            elif user.usertype=='org':
                return redirect('org-home')
            elif user.usertype=='admin':
                return redirect('admin-dashboard')
        else:
            # Return an invalid login error message
            return render(request, 'login.html', {'error_message': 'Invalid username/email or password.'})
    else:
        return render(request, 'login.html')

@login_required(login_url="/login/")
def donorhome(request):
    # Assuming places and needs are provided from the backend
    user=request.user
    user=Donor.objects.get(username=user)
    places = []
    needs = ['clothes','educational','food','medicine']

    # Assuming organizations are retrieved from the database
    organizations = Organization.objects.filter(approved=True)
    for org in organizations:
        if org.city not in places:
            places.append(org.city)
    # Getting the filter_option from the request GET parameters
    filter_option = request.GET.get('filter_option', 'None')

    context = {
        'places': places,
        'needs': needs,
        'organizations': organizations,
        'filter_option': filter_option,
        'donorname':user.name
    }

    return render(request, 'donorhome.html', context)

@login_required(login_url="/login/")
def donorprofile(request):
    donor=request.user
    print(donor)
    #donor = get_object_or_404(Donor, pk=donor_id)
    donor=Donor.objects.filter(username=donor)
    print(donor[0].username)
    return render(request, 'donorprofile.html', {'donor': donor[0]})

@login_required(login_url="/login/")
def donororg(request,pk):
    # Retrieve organization details from the database or any other source
    user=request.user
    user=CustomUser.objects.get(username=user)
    if user.usertype != 'donor':
        return redirect('login-view')
    organization = Organization.objects.get(pk=pk) 
    context = {
        'org_name': organization.org_name,
        'registration_no': organization.registration_no,
        'city': organization.city,
        'state': organization.state,
        'phone': organization.phone,
        'org_address': organization.org_address,
        'unique_id': organization.unique_id,
        'org_type': organization.org_type,
        'name_treasurer': organization.name_treasurer,
        'name_secretary': organization.name_secretary,
        'name_chairman': organization.name_chairman,
        'acc_name':organization.acc_holder_name,
        'acc_no':organization.acc_number,
        'ifsc':organization.ifsc,
        'upi_id':organization.upi_id
    }
    # my_object = Transaction.objects.first()  
    # my_object.delete()
    if request.method == 'POST':
        instance=Transaction()
        instance.donor_username=user
        instance.org_username=Organization.objects.get(pk=pk).username
        try:
            last_entry = Transaction.objects.last()
            num=last_entry.transaction_id + 1
        except :
            num=100000
        instance.transaction_id=num
        advertise=request.POST.get('advertise')
        if advertise:
            instance.advertise=advertise
        instance.amount=request.POST.get('amount')
        instance.save()

    return render(request, 'donororg.html', context)

def orgsignup(request):
    if request.method == 'POST':
        organization_name = request.POST.get('organization_name')
        registration_number = request.POST.get('registration_number')
        phone=request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address = request.POST.get('address')
        ngo_id = request.POST.get('ngo_id')
        org_type = request.POST.get('org_type')
        username = request.POST.get('email')
        treasurer_name = request.POST.get('treasurer_name')
        secretary_name = request.POST.get('secretary_name')
        chairman_name = request.POST.get('chairman_name')
        acc_holder_name = request.POST.get('acc_holder_name')
        acc_number = request.POST.get('acc_number')
        ifsc = request.POST.get('ifsc')
        upi_id = request.POST.get('upi_id')
        password=request.POST.get('password')

        # Creating and saving Organization object
        organization = Organization.objects.create_user(
            usertype='org',
            username=username,
            password=password,
            org_name=organization_name,
            registration_no=registration_number,
            phone=phone,
            city=city,
            state=state,
            org_address=address,
            unique_id=ngo_id,
            org_type=org_type,
            name_treasurer=treasurer_name,
            name_secretary=secretary_name,
            name_chairman=chairman_name,
            acc_holder_name=acc_holder_name,
            acc_number=acc_number,
            ifsc=ifsc, 
            upi_id=upi_id 
        )
        organization.save()
        return redirect('login-view')  # Redirect after successful submission
    else:
        return render(request, 'orgsignup.html')

@login_required(login_url="/login/")
def orgprofile(request):
    user=request.user
    user=Organization.objects.filter(username=user).first()
    organization = Organization.objects.filter(username=user).first()
    return render(request, 'orgprofile.html', {'organization': organization})

@login_required(login_url="/login/")
def orghome(request):
    org=request.user
    if org.usertype !='org':
        return redirect('login-view')
    org=Organization.objects.filter(username=org)
    org=org[0]
    print(org.approved)
    print(org.username)
    print(org)
    # mymodel=Needs.objects.first()
    # print(mymodel)
    # mymodel.delete()
    #print(Needs.objects.filter(org_username=org.username))
    if request.method == 'POST' and org.approved and not org.disapproved:
        clothes = request.POST.get('clothes', False) and True
        educational = request.POST.get('educational', False)  and True
        food = request.POST.get('food', False) and True
        medicine = request.POST.get('medicine', False) and True
        description = request.POST.get('description', None)

        # Create a new Donation object and save it to the database
        # Check if a Needs object exists for the organization
        existing_donation = Needs.objects.filter(org_username=org.username).first()

        if existing_donation:
            # Update existing donation
            existing_donation.clothes = clothes
            existing_donation.educational = educational
            existing_donation.food = food
            existing_donation.medicine = medicine
            existing_donation.description = description
            existing_donation.save()
            print(existing_donation)
        else:
            # Create a new donation
            print('No existing donation found, creating a new one')
            donation = Needs.objects.create(
                org_username=org.username,
                clothes=clothes,
                educational=educational,
                food=food,
                medicine=medicine,
                description=description
            )

        return render(request, 'orghome.html',{'result':'Updated'})  # Redirect after successful submission
    else:
        if org.approved and not org.disapproved:
            return render(request, 'orghome.html',{'result':''})
        condition=False
        if org.disapproved:
            condition=True
        
        return render(request, 'applicationstatus.html',context={'condition':condition})

@login_required(login_url="/login/")
def orgapproval(request):
    set=Transaction.objects.filter(approvefromorg=False)
    donations=[]
    for data in set:
        instance1=Donor.objects.get(username=data.donor_username)
        donation={'id':data.pk,'username':instance1.username,'name':instance1.name,'amount':data.amount}
        donations.append(donation)
    if request.method == 'POST':
        # Process form submission
        approve_ids = request.POST.getlist('approve')
        for donation_id in approve_ids:
            # Update the donation record(s) based on the IDs marked for approval
            donation = Transaction.objects.get(pk=donation_id)
            donation.approvefromorg = True
            donation.save()
        
        # Redirect to a success page or another view
        return render(request, 'orgapprove.html', {'donations': donations})  

    else:
        return render(request, 'orgapprove.html', {'donations': donations})

@login_required(login_url="/login/")
def adminorglist(request):
    # Assuming you have a model named Organization with fields 'name', 'place', and 'type'
    organizations = Organization.objects.filter(approved=False,disapproved=False)
    print(organizations)
    return render(request, 'adminorglist.html', {'organizations': organizations})

@login_required(login_url="/login/")
def adminorg(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    user=request.user
    user=Admin.objects.filter(username=user)
    user=user[0]
    print(user)
    if request.method == 'POST':
        # Check if the form was submitted
        if 'approved' in request.POST:
            # If the 'approved' checkbox is checked, perform the approval action
            organization.approved = True  # Assuming 'approved' is a boolean field in the Organization model
            organization.verifiername=user.name
            organization.save()
            # Redirect to a success page or another view
            return redirect('admin-dashboard')  # Replace '/success/' with the appropriate URL

    return render(request, 'adminorg.html', {'organization': organization})

def logoutUser(request):
    logout(request)
    return redirect('home-view')