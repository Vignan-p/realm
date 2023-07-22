from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignInForm, SignUpForm
from .models import Profile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignInForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignInForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import messages


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

import random
import requests
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from .forms import SignInForm


def index(request):
    return render(request, "index.html")


User = get_user_model()

from realm.models import CustomUser


API_KEY = "ed4c96e3-157b-11ee-addf-0200cd936042"

from django.shortcuts import redirect


def signin(request):
    if request.method == "POST":
        if "mobile" in request.POST:
            try:
                user_mobile_number = request.POST["mobile"]
                user = CustomUser.objects.get(mobile_number=user_mobile_number)
                print(user)
                # Generate a random OTP
                otp = str(random.randint(100000, 999999))

                # Send OTP to the user's mobile number
                send_otp_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/{user_mobile_number}/{otp}"

                response = requests.post(send_otp_url)
                if response.status_code == 200:
                    # OTP sent successfully
                    request.session["session_id"] = response.json().get("Details")
                    request.session[
                        "mobile_number"
                    ] = user_mobile_number  # Store mobile number in session
                    return render(
                        request,
                        "otp_verification.html",
                        {"mobile_number": user_mobile_number},
                    )

                # Failed to send OTP
                error_message = response.json().get("Status")
                return render(request, "signin.html", {"error_message": error_message})

            except CustomUser.DoesNotExist:
                error_message = "Invalid or non-existent mobile number."
                return render(request, "signin.html", {"error_message": error_message})

        # Process the username and password login
        username = request.POST["username"]
        password = request.POST["password"]

        if "otp" in request.POST:
            otp = request.POST["otp"]
            session_id = request.session.get("session_id")
            mobile_number = request.session.get("mobile_number")

            # Verify the OTP
            verify_otp_url = (
                f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{session_id}/{otp}"
            )

            response = requests.get(verify_otp_url)
            if (
                response.status_code == 200
                and response.json().get("Status") == "Success"
            ):
                # OTP verification successful
                user = authenticate(
                    request, username=mobile_number, password=""
                )  # Authenticate with mobile number

                if user is not None:
                    # User is authenticated
                    login(request, user)

                    # Fetch the profiles of the signed-in user
                    profiles = Profile.objects.filter(user=user)

                    if profiles.exists():
                        return render(request, "profile.html", {"profiles": profiles})
                    else:
                        # No profiles found for the user, redirect to profiles page
                        return redirect("profiles")

                else:
                    # Authentication failed
                    error_message = "Invalid username or password."
                    return render(
                        request, "signin.html", {"error_message": error_message}
                    )
            else:
                # OTP verification failed
                error_message = "Invalid OTP."
                return render(request, "signin.html", {"error_message": error_message})

        else:
            # Process the username and password login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # User is authenticated
                login(request, user)

                # Fetch the profiles of the signed-in user
                profiles = Profile.objects.filter(user=user)

                if profiles.exists():
                    return render(request, "profile.html", {"profiles": profiles})
                else:
                    # No profiles found for the user, redirect to profiles page
                    return redirect("profiles")

            else:
                # Authentication failed
                error_message = "Invalid username or password."
                return render(request, "signin.html", {"error_message": error_message})

    return render(request, "signin.html")


import requests


def otp_verification(request):
    user_mobile_number = request.session.get("mobile_number")
    if request.method == "POST":
        user_entered_otp = ""
        for i in range(1, 7):
            digit = request.POST.get(f"otp{i}")
            if not digit or not digit.isdigit():
                error_message = "Please enter a valid OTP."
                return render(
                    request,
                    "otp_verification.html",
                    {
                        "error_message": error_message,
                        "mobile_number": user_mobile_number,
                    },
                )
            user_entered_otp += digit

        session_id = request.session.get("session_id")
        # Verify the entered OTP
        verify_otp_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{session_id}/{user_entered_otp}"

        response = requests.post(verify_otp_url)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("Status") == "Success":
                # OTP verification successful

                # Get the user associated with the mobile number
                try:
                    user = CustomUser.objects.get(mobile_number=user_mobile_number)
                except CustomUser.DoesNotExist:
                    error_message = "Invalid or non-existent mobile number."
                    return render(
                        request,
                        "otp_verification.html",
                        {
                            "error_message": error_message,
                            "mobile_number": user_mobile_number,
                        },
                    )

                # Fetch the profiles associated with the user
                profiles = Profile.objects.filter(user=user)

                if profiles.exists():
                    return render(request, "profile.html", {"profiles": profiles})
                else:
                    # No profiles found for the user, redirect to profiles page
                    return redirect("profiles")

            else:
                # OTP verification failed
                error_message = json_response.get("Details")
                return render(
                    request,
                    "otp_verification.html",
                    {
                        "error_message": error_message,
                        "mobile_number": user_mobile_number,
                    },
                )

        # Failed to verify OTP
        error_message = "Failed to verify OTP."
        return render(
            request,
            "otp_verification.html",
            {"error_message": error_message, "mobile_number": user_mobile_number},
        )

    return render(
        request, "otp_verification.html", {"mobile_number": user_mobile_number}
    )


from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            username = form.cleaned_data["username"]
            mobile_number = form.cleaned_data["mobile_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if the username, email, or mobile number already exist
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            elif User.objects.filter(mobile_number=mobile_number).exists():
                messages.error(request, "Mobile number is already in use.")
            else:
                # Create a new user
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                user.mobile_number = (
                    mobile_number  # Save the mobile number in the user model
                )
                user.save()

                # Create a default profile for the user during signup
                profile_name = username
                profile = Profile(
                    user=user, name=profile_name, mobile_number=mobile_number
                )
                profile.save()

                login(request, user)
                subject = "Signup Success"
                context = {"username": username}
                html_message = render_to_string("signup_success_email.html", context)
                plain_message = strip_tags(html_message)
                from_email = "realmdefend@gmail.com"
                to_email = user.email

                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    [to_email],
                    html_message=html_message,
                )
                return redirect("signin")
        else:
            # If the form is not valid, display the error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


from .forms import VideoUploadForm
from .models import Video


import zipfile
import os


def movie_upload(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)

            # Save the video and thumbnail files
            video.video_file = request.FILES["video_file"]
            video.thumbnail = request.FILES["thumbnail"]
            video.save()

            # Unzip the video file if it is a zip file
            if video.video_file.name.endswith(".zip"):
                zip_file_path = video.video_file.path
                target_directory = os.path.dirname(zip_file_path)

                with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                    zip_ref.extractall(target_directory)

                # Remove the zip file after extraction
                os.remove(zip_file_path)

                # Change the value of video_file to have .m3u8 extension
                new_video_file_name = (
                    os.path.splitext(video.video_file.name)[0] + ".m3u8"
                )
                video.video_file.name = new_video_file_name
                video.save(update_fields=["video_file"])

            return redirect(
                "movie_upload"
            )  # Redirect to the videos page after successful upload
    else:
        form = VideoUploadForm()
    return render(request, "video_upload.html", {"form": form})


from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    # Retrieve the logged-in user
    user = request.user
    # Retrieve all profiles associated with the logged-in user
    profiles = Profile.objects.filter(user=user)
    return render(request, "profile.html", {"user": user, "profiles": profiles})


@login_required
def add_profile(request):
    user = request.user
    profile_count = Profile.objects.filter(user=user).count()

    if profile_count >= 4:
        return redirect("profile")

    if request.method == "POST":
        profile_name = request.POST["profile_name"]
        profile_photo = request.FILES.get(
            "profile_photo"
        )  # Updated field name to 'profile_photo'
        child_profile = request.POST.get("child_profile")
        pin = request.POST.get("pin")  # Get the 'pin' value from the form
        confirm_pin = request.POST.get("cpin")

        if pin == confirm_pin:
            child_profile = True if child_profile == "1" else False

            existing_profile = Profile.objects.filter(
                user=user, name=profile_name
            ).first()
            if existing_profile:
                return redirect("profiles")

            profile = Profile(
                user=user,
                name=profile_name,
                photo=profile_photo,
                child_profile=child_profile,
                pin=pin,
            )  # Save 'pin' to the profile
            profile.save()

            profile_count += 1
            if profile_count >= 4:
                add_profile_disabled = True
            else:
                add_profile_disabled = False

            return redirect("profiles")
        else:
            error_message = "PIN and Confirm PIN do not match"
            return render(
                request,
                "add_profile.html",
                {"add_profile_disabled": False, "error_message": error_message},
            )

    return render(request, "add_profile.html", {"add_profile_disabled": False})


def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    is_first_profile = Profile.objects.filter(user=request.user).first() == profile
    if request.method == "POST":
        name = request.POST.get("name")
        profile.name = name

        if "profile_picture" in request.FILES:
            profile.photo = request.FILES["profile_picture"]

        profile.save()

        return redirect("profiles")
    context = {
        "profile": profile,
        "is_first_profile": is_first_profile,
    }
    return render(request, "edit_profile.html", context)


def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.delete()
    return redirect("profiles")


from django.shortcuts import get_object_or_404
from .models import Genres, Video


from django.shortcuts import render


def player(request, video_id):
    video = Video.objects.get(id=video_id)
    video_url = video.video_file.url
    print(video_url)
    return render(request, "player.html", {"video_url": video_url})


import datetime


def home(request):
    categories = Genres.objects.all()
    videos = Video.objects.all()

    genre_id = request.GET.get("genre_id")
    if genre_id:
        genre = get_object_or_404(Genres, id=genre_id)
        videos = videos.filter(genres=genre)

    return render(
        request, "category_list.html", {"categories": categories, "videos": videos}
    )


def schedule(request):
    current_time = datetime.datetime.now()
    videos = Video.objects.filter(scheduled_time__lte=current_time)
    return render(request, "scheduled_video.html", {"videos": videos})


def video_list(request, genre_id):
    genre = Genres.objects.get(pk=genre_id)
    videos = Video.objects.filter(genres=genre)
    thumbnails = Video.objects.all()
    context = {"genre": genre, "videos": videos, "thumbnails": thumbnails}
    return render(request, "video_list.html", context)


def search(request):
    videos = Video.objects.all()
    return render(request, "search.html", {"videos": videos})


def search_kids(request):
    videos = Video.objects.exclude(content_age_rating="18+")
    return render(request, "search.html", {"videos": videos})


def kid_home(request):
    categories = Genres.objects.all()
    videos = Video.objects.exclude(content_age_rating="18+")
    genre_id = request.GET.get("genre_id")
    if genre_id:
        genre = get_object_or_404(Genres, id=genre_id)
        videos = videos.filter(genres=genre)

    return render(request, "home1.html", {"categories": categories, "videos": videos})


def home_kids(request):
    categories = Genres.objects.exclude(
        name__in=["Crime", "Thriller", "Romantic", "Horror"]
    )
    videos = Video.objects.exclude(content_age_rating="18+")

    genre_id = request.GET.get("genre_id")
    if genre_id:
        genre = get_object_or_404(Genres, id=genre_id)
        videos = videos.filter(genres=genre)

    return render(
        request, "category_list1.html", {"categories": categories, "videos": videos}
    )


def video_list1(request, genre_id):
    genre = get_object_or_404(Genres, pk=genre_id)
    videos = Video.objects.exclude(content_age_rating="18+").filter(genres=genre)
    context = {"genre": genre, "videos": videos}
    return render(request, "video_list.html", context)


def logout_view(request):
    logout(request)
    return redirect("index")


def movie_details(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "movie.html", {"video": video})


def unlock_pin(request):
    if request.method == "POST":
        name = request.POST.get("profilename", "")
        digit1 = request.POST.get("digit1", "")
        digit2 = request.POST.get("digit2", "")
        digit3 = request.POST.get("digit3", "")
        digit4 = request.POST.get("digit4", "")

        submitted_pin = digit1 + digit2 + digit3 + digit4

        # Assuming you have a Profile model with 'pin', 'child_profile', and 'name' fields
        from .models import Profile

        try:
            profile = Profile.objects.get(name=name)

            # Check the submitted PIN against the fetched profile's PIN
            if profile.pin == submitted_pin:
                child_profile = profile.child_profile
                print("Child Profile:", child_profile)  # Print the value for debugging

                if child_profile == 0:
                    return redirect("home")
                else:
                    return redirect("home_kids")
            else:
                return render(request, "pin.html", {"error_message": "Invalid PIN"})

        except Profile.DoesNotExist:
            # Profile does not exist
            return render(request, "pin.html", {"error_message": "Invalid Name"})
    else:
        # GET request or other method
        return render(request, "pin.html")


from django.urls import reverse


def unlock(request):
    if request.method == "POST":
        name = request.POST.get("profilename", "")
        digit1 = request.POST.get("digit1", "")
        digit2 = request.POST.get("digit2", "")
        digit3 = request.POST.get("digit3", "")
        digit4 = request.POST.get("digit4", "")

        submitted_pin = digit1 + digit2 + digit3 + digit4

        # Assuming you have a Profile model with 'pin', 'child_profile', and 'name' fields
        from .models import Profile

        try:
            profile = Profile.objects.get(name=name)

            # Check the submitted PIN against the fetched profile's PIN
            if profile.pin == submitted_pin:
                edit_profile_url = reverse("edit_profile", args=[profile.id])
                return redirect(edit_profile_url)
            else:
                return render(
                    request, "pin_edit.html", {"error_message": "Invalid PIN"}
                )

        except Profile.DoesNotExist:
            # Profile does not exist
            return render(request, "pin_edit.html", {"error_message": "Invalid Name"})
    else:
        # GET request or other method
        return render(request, "pin_edit.html")
