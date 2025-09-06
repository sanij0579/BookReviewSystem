from django.views import View
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render, redirect
from django.contrib import messages
from book.forms import BookForm
from book.models import Book

class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'book/book_form.html', {'form': form})
    
    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book-create')
        return render(request, 'book/book_form.html', {'form': form})

class BookListView(TemplateView):
    template_name = 'book/book_list.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        genre = self.request.GET.get('genre')
        if genre:
            context['books'] = Book.objects.filter(genre=genre).order_by('-created_at')
        else:
            context['books'] = Book.objects.all().order_by('-created_at')
        return context

class BookDetailView(TemplateView):
    template_name = 'book/book_detail.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        context['book'] = Book.objects.get(pk=pk)
        return context

class BookUpdateView(View):
    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        form = BookForm(instance=book)
        return render(request, 'book/book_form.html', {'form': form})
    
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book-update', pk=pk)
        return render(request, 'book/book_form.html', {'form': form})


class BookDeleteView(RedirectView):
    pattern_name = 'book-list'

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs.get('pk')
        book = Book.objects.get(pk=pk)
        book.delete()
        messages.success(self.request, 'Book deleted successfully!')
        # Return URL for book-list without passing any kwargs
        return super().get_redirect_url()
