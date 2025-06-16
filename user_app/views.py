from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm , StudentForm
from django.shortcuts import render, redirect
from django.urls import reverse
from courses_app.models import Post
from learning_style.models import Student

# Create your views here.
def index(request):
    return render(request, "user_app/index.html")
def about(request):
    return render(request,'user_app/aboutus.html')
def student(request):
    return render(request,'user_app/student.html')
def teacher(request):
    return render(request,'user_app/teacher.html')
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST ,request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Anda Berhasil Mendaftar. Silahkan Masuk dengan Akun yang terdaftar")
        else:
            msg = 'form is not valid'  
    else:
        form = SignUpForm()
    return render(request,'user_app/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Arahkan sesuai kebutuhan, contoh:
                return redirect('user_app:dashboard')  # bisa ganti sesuai route yang diinginkan
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'user_app/login.html', {'form': form, 'msg': msg})



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
@login_required
def teacherdashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_date')

    # Menangani pengiriman form untuk menambah murid
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Menyimpan murid baru
            return redirect('user_app:dashboard')  # Redirect untuk refresh halaman

    else:
        form = StudentForm()

    # Ambil daftar murid yang ada
    students = Student.objects.all()

    return render(request, 'dashboard_app/teachers_dashboard.html', {
        'posts': posts,
        'form': form,
        'students': students,  # Kirimkan daftar murid ke template
    })
@login_required
def teacherprofile(request):
    # Check if the user is a teacher
    if not request.user.is_teacher:
        messages.warning(request, "You are not authorized to access this page.")
        return redirect('index')  # Redirect to a safe page
    user_profile = request.user
    return render(request, 'dashboard_app/teacher_profile.html', {'user_profile': user_profile })