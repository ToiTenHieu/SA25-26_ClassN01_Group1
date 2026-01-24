# ebook_reader/views.py
from django.shortcuts import render, get_object_or_404
from .models import Ebook

def read_ebook_view(request, ebook_id):
    ebook = get_object_or_404(Ebook, id=ebook_id)
    ebook_url = ebook.file.url
    context = {
        'ebook_url': ebook_url,
        'book_title': ebook.book.title,
    }
    return render(request, 'ebook_reader/read_ebook.html', context)
# ebook_reader/views.py
from django.shortcuts import render
from .models import Ebook

def digital(request):
    category = request.GET.get('category', '')  # lấy thể loại từ query string
    if category:
        ebooks = Ebook.objects.filter(book__category=category)
    else:
        ebooks = Ebook.objects.all()
    return render(request, 'ebook_reader/digital.html', {'ebooks': ebooks, 'selected_category': category})
