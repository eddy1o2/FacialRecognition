import base64

import cv2
import os, errno

from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, NewPostForm

from .models import Post


# Create your views here.

def home(request):
    return render(request, 'home.html')


def list_blog(request):
    data = {'Posts': Post.objects.all().order_by('-created_at')}
    return render(request, 'blog.html', data)


class PostListView(ListView):
    queryset = Post.objects.all().order_by('-created_at')
    template_name = 'blog.html'
    context_object_name = 'Posts'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'


def about(request):
    return render(request, 'about.html')


def stream():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('static/images/img_demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               open('static/images/img_demo.jpg', 'rb').read() + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def detected_face(request):
    return render(request, 'streaming.html')


def error(request):
    return render(request, 'error.html')


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():

            # Getting static folder path from project settings
            static_dir = settings.STATICFILES_DIRS[0]

            # Creating a folder in static directory
            new_dir_path = os.path.join(static_dir, "images/" + form.clean_username())
            try:
                os.mkdir(new_dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    # directory already exists
                    pass
                else:
                    print(e)
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'register.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


def new_post(request):
    user = User.objects.first()
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = user
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('blogs')
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})


def get_data(request):
    return render(request, 'get_data.html')


# TODO: Handle user log in first
# @login_required
def resource(request):
    return render(request, 'resource.html')


def save_img(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = request.POST.get('imgBase64')
            # get base64 raw string
            base64_str = data[22:]
            # print(len(data))
            # print(base64_str)
            # print(base64_str[-10:len(base64_str)])
            # pic = io.BytesIO()
            # img_string = io.BytesIO(base64.b64decode(base64_str))
            # image = Image.open(img_string)
            # image.save(pic, image.format, quality=100)
            # pic.seek(0)
            # return HttpResponse(pic, content_type='image/png')
            img_data = base64.b64decode(base64_str)
            with open('static/images/output.png', 'wb') as f:
                f.write(img_data)
            return HttpResponse('')
    else:
        print('nothing')
