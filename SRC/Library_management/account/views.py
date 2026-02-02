from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout,
    update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction

from .forms import UserRegisterForm, UserForm, ChangeUserProfileForm
from .models import UserProfile
from library.models import BorrowRecord


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("/account/register/")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("/account/register/")

        user = User.objects.create_user(username=username, email=email, password=password)

        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            gender=gender,
            date_of_birth=date_of_birth or None,
            address=address
        )

        messages.success(request, "Registration successful. Please log in.")
        return redirect("/account/login/")
    else:
        return render(request, "account/register.html")

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "No user profile found.")
                return redirect('account:login')
            if user.is_superuser:
                return redirect('/admin/')
            elif profile.role == 'librarian':
                return redirect('Librarian:managebook')
            else:
                return redirect('library:home')
        else:
            messages.error(request, "Username or password is incorrect.")
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("account:login")


@login_required
@transaction.atomic
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    total_borrowed = BorrowRecord.objects.filter(user=profile).count()
    currently_borrowed = BorrowRecord.objects.filter(user=profile, status='borrowed').count()
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ChangeUserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("account:profile")
        else:
            messages.error(request, "There was an error updating your profile. Please check the form fields.")
    else:
        user_form = UserForm(instance=user)
        profile_form = ChangeUserProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user": user,
        "total_borrowed": total_borrowed,        
        "currently_borrowed": currently_borrowed 
    }
    return render(request, "account/profile.html", context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('library:home')
        else:
            messages.error(request, 'Please check your information.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change-password.html', {'form': form})


def regis_by_fb(request):
    return render(request, 'account/regis_by_fb.html')


def regis_by_gg(request):
    return render(request, 'account/regis_by_gg.html')
