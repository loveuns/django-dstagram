from django.shortcuts import render, redirect, reverse
from .models import Photo
from .forms import PhotoForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from tagging.views import TaggedObjectList


@login_required
def list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/list.html', {'object_list': photos})


class TagListView(LoginRequiredMixin, TaggedObjectList):
    model = Photo
    template_name = 'photo/list.html'


class UploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'text', 'tag']
    template_name = 'photo/upload.html'  # photo_form.html

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.save()
            return redirect('photo:list')
        else:
            return self.render_to_response({'form': form})


@login_required
def upload(request):
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('photo:list')
    else:
        form = PhotoForm()
    return render_to_response({'form': form})


class DetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/detail.html'


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete_confirm.html'  # photo_confirm_delete.html

    # 작성자 본인 체크
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user == self.object.author:
            return redirect('/')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)


class UpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text', 'tag']
    template_name = 'photo/update.html'  # photo_form.html

    def get_success_url(self):
        return reverse('photo:detail', args=[self.object.id])

    # 작성자 본인 체크
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user == self.object.author:
            return redirect('/')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
