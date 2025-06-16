from typing import Any
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.query import QuerySet
from django.views.generic import (ListView, 
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from courses_app.models import Post , Class, Lesson
from courses_app.forms import PostForm , ClassForm , LearningCharacteristicForm
from user_app.models import User  # Ganti Teacher dengan User
from learning_style.models import LearningCharacteristic
# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'courses_app/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        # Ambil parameter pencarian dari URL
        search_query = self.request.GET.get('search', '')
        learning_style_filter = self.request.GET.get('learning_style', '')  # Ambil filter gaya belajar

        # Query default: hanya post yang sudah dipublikasikan
        queryset = Post.objects.filter(published_date__lte=timezone.now())

        # Jika ada parameter pencarian, filter berdasarkan title atau text
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )

        # Jika ada parameter filter gaya belajar, filter post berdasarkan gaya belajar
        if learning_style_filter:
            queryset = queryset.filter(learning_style=learning_style_filter)

        # Urutkan berdasarkan tanggal publikasi terbaru
        return queryset.order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')

        # Menambahkan pilihan gaya belajar ke dalam context untuk ditampilkan di template
        context['learning_style_choices'] = Post.LEARNING_STYLE_CHOICES
        context['selected_learning_style'] = self.request.GET.get('learning_style', '')  # Menambahkan gaya belajar yang dipilih ke context

        return context
    
class ClassListView(ListView):
    model = Class
    template_name = 'courses_app/class_list.html'
    context_object_name = 'classes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mendapatkan post berdasarkan pk yang diteruskan di URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Menambahkan post ke dalam konteks
        context['post'] = post
        return context

    def get_queryset(self):
        # Mendapatkan post berdasarkan pk yang diteruskan
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Mengambil kelas yang terkait dengan post tersebut
        return Class.objects.filter(post=post)

class ClassDetailView(DetailView):
    model = Class
    template_name = 'courses_app/class_detail.html'
    context_object_name = 'class_instance'

    
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Ambil semua kelas terkait dengan post ini
        context['classes'] = post.classes.all()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post
    template_name = 'courses_app/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # langsung pakai request.user
        context['posts'] = Post.objects.filter(author=user).order_by('-created_date')
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user  # langsung pakai request.user
        # Pastikan published_date tidak diset supaya post masuk draft
        post.published_date = None
        post.save()
        return redirect('post_draft_list')

class ClassCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = ClassForm
    model = Class
    template_name = 'courses_app/create_class.html'

    def get_form_kwargs(self):
        """
        Override method ini untuk mengirimkan user ke ClassForm.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Kirim user yang sedang login
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Tambahkan informasi tambahan ke context.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Ambil semua post yang dibuat oleh user
        context['posts'] = Post.objects.filter(author=user)
        return context

    def form_valid(self, form):
        """
        Validasi form sebelum menyimpan.
        """
        class_instance = form.save(commit=False)
        # Pastikan post milik user yang sedang login
        if class_instance.post.author != self.request.user:
            form.add_error('post', "Anda tidak memiliki izin untuk menggunakan post ini.")
            return self.form_invalid(form)
        class_instance.save()
        return redirect('user_app:dashboard')  # Arahkan ke halaman post_detail setelah menyimpan kelas


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Simpan post terlebih dahulu
        post = form.save(commit=False)
        post.save()  # Save post ke database
        # Redirect ke halaman draft list
        return redirect('post_draft_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Post
    template_name = 'courses_app/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        # Ambil semua post draft milik user (published_date null)
        return Post.objects.filter(author=user, published_date__isnull=True).order_by('created_date')
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_new')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('user_app:dashboard')

@login_required
def post_(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

class LessonListView(ListView):
    model = Lesson
    template_name = 'courses_app/lesson_list.html'
    context_object_name = 'lessons' 

class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'courses_app/lesson_detail.html' 
    context_object_name = 'lesson' 

    # Menambahkan produk dan subchapter yang terkait ke dalam konteks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()  # Mendapatkan objek lesson berdasarkan pk
        
        # Menambahkan produk terkait lesson ke dalam konteks
        context['products'] = lesson.products.all()  # Mengambil semua produk terkait dengan lesson
        
        # Menambahkan subchapter terkait lesson ke dalam konteks
        return context
    
@login_required
def kuisoner_view(request):
    # Jika metode POST untuk menambah atau mengedit data
    if request.method == 'POST':
        # Menangani data untuk menambah atau mengedit
        if 'add' in request.POST:
            form = LearningCharacteristicForm(request.POST)
            if form.is_valid():
                form.save()  # Menyimpan data baru
                return redirect('kuisoner')  # Redirect ke halaman kuisoner setelah menyimpan

        elif 'edit' in request.POST:
            # Menangani update data
            characteristic_id = request.POST.get('characteristic_id')
            characteristic = get_object_or_404(LearningCharacteristic, id=characteristic_id)
            form = LearningCharacteristicForm(request.POST, instance=characteristic)
            if form.is_valid():
                form.save()  # Menyimpan data yang telah diubah
                return redirect('kuisoner')

        elif 'delete' in request.POST:
            # Menangani penghapusan data
            characteristic_id = request.POST.get('characteristic_id')
            characteristic = get_object_or_404(LearningCharacteristic, id=characteristic_id)
            characteristic.delete()  # Menghapus data
            return redirect('kuisoner')

    else:
        form = LearningCharacteristicForm()

    # Ambil semua data LearningCharacteristic dan urutkan berdasarkan 'code'
    characteristics = LearningCharacteristic.objects.all().order_by('code')  # Mengurutkan berdasarkan 'code'

    return render(request, 'courses_app/kuisoner.html', {
        'form': form,
        'characteristics': characteristics  # Kirimkan daftar data ke template
    })