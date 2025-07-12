from django.shortcuts import render, redirect, get_object_or_404 ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm, SkillSwapRequestForm
from .models import Profile, SkillSwapRequest

# Landing/Homepage
def landing_page(request):
    return render(request, 'landing_page.html')

# Dashboard after login
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Notification/messages page (renamed to avoid conflict with django.contrib.messages)
@login_required
def notifications_view(request):
    return render(request, 'messages.html')

# View swap requests (both sent and received)
@login_required
def swap_requests(request):
    received = SkillSwapRequest.objects.filter(receiver=request.user)
    sent = SkillSwapRequest.objects.filter(sender=request.user)
    return render(request, 'swap_requests.html', {
        'received_requests': received,
        'sent_requests': sent,
    })



# View and browse other users' profiles
@login_required
def skill_search(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'skill.html', {'profiles': profiles})

# Handle skill swap request form
@login_required
def send_swap_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        form = SkillSwapRequestForm(request.POST)
        if form.is_valid():
            swap_request = form.save(commit=False)
            swap_request.sender = request.user
            swap_request.receiver = receiver
            swap_request.save()
            return redirect('swap_requests')
    else:
        form = SkillSwapRequestForm()

    return render(request, 'swap_request_form.html', {
        'form': form,
        'receiver': receiver
    })

# Profile management (update/create)
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Split skills into list if input is a comma-separated string
            offered = form.cleaned_data['skills_offered']
            wanted = form.cleaned_data['skills_wanted']

            if isinstance(offered, str):
                form.instance.skills_offered = [skill.strip() for skill in offered.split(',') if skill.strip()]
            if isinstance(wanted, str):
                form.instance.skills_wanted = [skill.strip() for skill in wanted.split(',') if skill.strip()]

            form.save()
            return redirect('profile')  # ✅ Redirect after successful POST

    else:
        form = ProfileForm(instance=profile, initial={
            'skills_offered': ', '.join(profile.skills_offered) if isinstance(profile.skills_offered, list) else profile.skills_offered,
            'skills_wanted': ', '.join(profile.skills_wanted) if isinstance(profile.skills_wanted, list) else profile.skills_wanted,
        })

    return render(request, 'profile.html', {'form': form})  # ✅ This line is **essential**

# Accept a swap request
@login_required
def accept_swap_request(request, request_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=request_id, receiver=request.user)
    swap_request.status = 'Accepted'
    swap_request.save()
    messages.success(request, 'You accepted the skill swap request.')
    return redirect('swap_requests')

# Reject a swap request
@login_required
def reject_swap_request(request, request_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=request_id, receiver=request.user)
    swap_request.status = 'Rejected'
    swap_request.save()
    messages.warning(request, 'You rejected the skill swap request.')
    return redirect('swap_requests')

@login_required
def save_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Handle comma-separated skill strings
            offered = form.cleaned_data.get('skills_offered')
            wanted = form.cleaned_data.get('skills_wanted')

            if isinstance(offered, str):
                form.instance.skills_offered = [skill.strip() for skill in offered.split(',') if skill.strip()]
            if isinstance(wanted, str):
                form.instance.skills_wanted = [skill.strip() for skill in wanted.split(',') if skill.strip()]

            form.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'skills_offered': ', '.join(profile.skills_offered) if isinstance(profile.skills_offered, list) else profile.skills_offered,
            'skills_wanted': ', '.join(profile.skills_wanted) if isinstance(profile.skills_wanted, list) else profile.skills_wanted,
        })

    return render(request, 'profile.html', {'form': form})
