from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post
from .forms import NewPostForm, EditPostForm, FollowForm


def index(request):
    if request.method == "POST":
        new_post_form = NewPostForm(request.POST)
        if new_post_form.is_valid():
            new_post = new_post_form.save(commit=False)
            new_post.creator = request.user
            new_post.save()
            new_post_form.save_m2m()
        new_post_form = NewPostForm()
    else:
        new_post_form = NewPostForm()

    posts = Post.objects.all().order_by("-timestamp")
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = posts_paginator.get_page(page_number)

    return render(
        request,
        "network/index.html",
        {"new_post_form": new_post_form, "posts": page_obj},
    )


@login_required
def following(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(creator__in=following_users).order_by("-timestamp")
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = posts_paginator.get_page(page_number)
    return render(request, "network/index.html", {"posts": page_obj})


@login_required
def edit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id")
    edited_text = data.get("edited_text")

    post = Post.objects.get(pk=post_id)

    if request.user != post.creator:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    form = EditPostForm({"text": edited_text}, instance=post)

    if form.is_valid():
        form.save()
        return JsonResponse({"message": "Post updated successfully."}, status=200)
    else:
        errors = form.errors.get("text")
        return JsonResponse(
            {"error": errors[0] if errors else "Invalid data."}, status=400
        )


def profile_page(request, user_name):
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(creator=user).order_by("-timestamp")
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = posts_paginator.get_page(page_number)
    return render(
        request, "network/profile.html", {"posts": page_obj, "prof_user": user}
    )


@login_required
def add_like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    elif request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        user = request.user

        if user not in post.likes.all():
            post.likes.add(user)

        return JsonResponse({"liked": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

    # TODO add JS and backend for the liking system
    # might need a form
    pass


@login_required
def remove_like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    elif request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)

        return JsonResponse({"liked": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def follow(request, user_id):
    current_user = request.user
    form = FollowForm(request.POST)

    if form.is_valid():
        user_to_follow = User.objects.get(pk=user_id)

        if current_user != user_to_follow:
            current_user.following.add(user_to_follow)
            user_to_follow.followers.add(current_user)

        return HttpResponseRedirect(reverse("profile_page", args=[user_to_follow.username]))

    return HttpResponseRedirect(reverse("profile_page", args=[current_user.username]))


@login_required
def unfollow(request, user_id):
    current_user = request.user
    form = FollowForm(request.POST)
    if form.is_valid():
        user_to_follow = User.objects.get(pk=user_id)

        if current_user != user_to_follow:
            current_user.following.remove(user_to_follow)
            user_to_follow.followers.remove(current_user)

        return HttpResponseRedirect(reverse("profile_page", args=[user_to_follow.username]))

    return HttpResponseRedirect(reverse("profile_page", args=[current_user.username]))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
