from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .models import Book
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.management import call_command

@login_required
def send_due_reminder_view(request):
    # 👉 nếu bạn có role thủ thư thì check thêm ở đây
    # ví dụ:
    # if request.user.role != "librarian": ...

    if request.method == "POST":
        call_command("send_due_reminder")
        return JsonResponse({
            "success": True,
            "message": "📧 sent a reminder email about the book return deadline (one day in advance)."
        })

    return JsonResponse({"success": False}, status=400)
@login_required
def send_overdue_reminder_api(request):
    try:
        call_command("send_overdue_reminder")
        return JsonResponse({"success": True, "message": "📧 Sent reminder email to overdue users."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
@login_required
def librarian_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)

    # ✅ Chỉ cho phép thủ thư truy cập
    if profile.role != 'librarian':
        return redirect('library:home')

    # ======================================================
    # 👉 Xử lý khi nhấn "Thêm người dùng"
    # ======================================================
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        name = request.POST.get("name")
        occupation = request.POST.get("occupation")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")

        # 1️⃣ Tạo tài khoản User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # 2️⃣ Tạo UserProfile tương ứng
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            role='user'
        )

        return redirect(reverse("librarian:managebook") + "?section=quanLyNguoiDung")

    # ======================================================
    # 👉 Load dữ liệu hiển thị
    # ======================================================
    users_only = UserProfile.objects.filter(role='user').order_by("id")

    # --- Phân trang người dùng ---
    paginator = Paginator(users_only, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    books = Book.objects.all()
    categories = Book.objects.values_list('category', flat=True).distinct()
    librarian_name = profile.name or profile.user.username

    # ======================================================
    # 👉 Lấy danh sách mượn trả
    # ======================================================
    records_all = BorrowRecord.objects.select_related("user", "book").all()

    # --- Tự động cập nhật trạng thái "overdue" ---
    today = now().date()
    for record in records_all:
        if record.due_date and record.due_date < today and record.status == 'borrowed':
            record.status = 'overdue'
            record.save()

    # --- Phân loại ---
    records_borrowed = records_all.filter(status__in=['borrowed', 'overdue'])
    records_ovedue = records_all.filter(status= 'overdue')
    records_history = records_all.filter(status='returned')

    # --- Tổng số bản ghi ---
    total_borrowed = records_borrowed.count()
    total_history = records_history.count()
    total_books = Book.objects.count()
    # ======================================================
    # 👉 Truyền dữ liệu sang template
    # ======================================================
    context = {
        'users': page_obj.object_list,
        'page_obj': page_obj,
        'books': books,
        'categories': categories,
        'librarian_name': librarian_name,
        'profile': profile,
        'records_borrowed': records_borrowed,
        'records_history': records_history,
        'total_borrowed': total_borrowed,
        'total_history': total_history,
        'total_books': total_books,
        'records_ovedue':records_ovedue,
    }

    return render(request, 'managebook.html', context)

from django.contrib.auth.models import Group


def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "account/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


# views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import UserProfile


def danh_sach_nguoi_dung(request):
    users = UserProfile.objects.select_related('user').all()  # lấy tất cả UserProfile kèm User
    return render(request, 'users_list.html', {'users': users})


from django.core.paginator import Paginator

def catalog(request):
    books = Book.objects.all().order_by("-book_id")   # lấy danh sách sách
    paginator = Paginator(books, 8)  # 8 sách / trang

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "/catalog.html", {"page_obj": page_obj})
@login_required
def payment_done(request):
    return render(request, "account/payment_done.html")  
from django.shortcuts import get_object_or_404, render, redirect
from .models import UserProfile  # model chứa phone, address, gender,...

def edit_user(request, user_id):
    profile = get_object_or_404(UserProfile, pk=user_id)
    if request.method == "POST":
        profile.name = request.POST.get('name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.date_of_birth = request.POST.get('date_of_birth')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect(reverse("librarian:managebook") + "?section=quanLyNguoiDung")
    return render(request, 'edit_user.html', {'user': profile})
@csrf_exempt  # hoặc dùng csrf token header trong fetch
def delete_user_api(request, user_id):
    if request.method == "DELETE":
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        user_profile.delete()
        return JsonResponse({"message": "User deleted successfully."})
    
    return JsonResponse({"error": "Invalid request method."}, status=400)
from django.template.defaultfilters import slugify

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def add_book(request):
    if request.method == "POST":
        # Kiểm tra xem có phải FormData (file upload) hay JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Xử lý FormData (có file upload)
            name = request.POST.get("bookName") or request.POST.get("name")
            author = request.POST.get("author")
            category = request.POST.get("category")
            quantity = request.POST.get("quantity")
            publish_year = request.POST.get("publishYear") or request.POST.get("year")
            description = request.POST.get("description")
            cover_image = request.FILES.get("cover_image")
            
            # Lưu vào DB
            book = Book.objects.create(
                title=name,
                author=author,
                category=category,
                quantity=quantity,
                year=publish_year,
                description=description
            )
            
            # Lưu ảnh bìa nếu có
            if cover_image:
                book.cover_image = cover_image
                book.save()
        else:
            # Xử lý JSON (backward compatibility)
            data = json.loads(request.body)
            name = data.get("name")
            author = data.get("author")
            category = data.get("category")
            quantity = data.get("quantity")
            publish_year = data.get("publishYear")
            description = data.get("description")

            # Lưu vào DB
            book = Book.objects.create(
                title=name,
                author=author,
                category=category,
                quantity=quantity,
                year=publish_year,
                description=description
            )

        return JsonResponse({"message": "Book added successfully", "id": book.book_id}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def update_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "GET":
        # Trả về dữ liệu sách để load vào form
        return JsonResponse({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "description": book.description,
            "status": book.status,
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.year = data.get("year", book.year)
            book.category = data.get("category", book.category)
            book.quantity = data.get("quantity", book.quantity)
            book.description = data.get("description", book.description)
            book.status = data.get("status", book.status)
            book.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Book
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Book
import json

# GET all books
def book_list(request):
    if request.method == "GET":
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

# GET or PUT a single book
@csrf_exempt
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "GET":
        response_data = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "status": book.status,
            "description": book.description,
        }
        # Thêm URL ảnh bìa nếu có
        if book.cover_image:
            response_data["cover_image_url"] = book.cover_image.url
        return JsonResponse(response_data)

    elif request.method == "POST":  # Đổi từ PUT sang POST để hỗ trợ FormData
        # Kiểm tra xem có phải FormData (file upload) hay JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Xử lý FormData (có file upload)
            book.title = request.POST.get("title", book.title)
            book.author = request.POST.get("author", book.author)
            book.year = request.POST.get("year", book.year)
            book.category = request.POST.get("category", book.category)
            book.quantity = request.POST.get("quantity", book.quantity)
            book.status = request.POST.get("status", book.status)
            book.description = request.POST.get("description", book.description)
            
            # Xử lý ảnh bìa nếu có
            cover_image = request.FILES.get("cover_image")
            if cover_image:
                book.cover_image = cover_image
            
            book.save()
        else:
            # Xử lý JSON (backward compatibility)
            data = json.loads(request.body.decode("utf-8"))

            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.year = data.get("year", book.year)
            book.category = data.get("category", book.category)
            book.quantity = data.get("quantity", book.quantity)
            book.status = data.get("status", book.status)
            book.description = data.get("description", book.description)
            book.save()

        return JsonResponse({"message": "Book updated successfully"})

    elif request.method == "PUT":
        # Backward compatibility với PUT
        data = json.loads(request.body.decode("utf-8"))

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.year = data.get("year", book.year)
        book.category = data.get("category", book.category)
        book.quantity = data.get("quantity", book.quantity)
        book.status = data.get("status", book.status)
        book.description = data.get("description", book.description)
        book.save()

        return JsonResponse({"message": "Book updated successfully"})

    elif request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"}, status=200)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
from django.shortcuts import render
from .models import BorrowRecord

from django.shortcuts import render
from .models import BorrowRecord
# app_name/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import BorrowRecord # Thay bằng tên model thực tế của bạn

@require_POST
def return_book_api(request, record_id):
    try:
        borrow_record = get_object_or_404(BorrowRecord, pk=record_id)
        
        # 1. Cập nhật ngày trả và trạng thái
        borrow_record.return_date = timezone.now().date()
        borrow_record.status = 'RETURNED' # Thay 'RETURNED' bằng trạng thái hợp lệ
        borrow_record.save()
        
        # 2. Tăng số lượng sách có sẵn (Nếu cần)
        # book = borrow_record.book # Giả sử có field 'book' Foreign Key
        # book.quantity += 1
        # book.save()

        return JsonResponse({'message': 'Book returned and status updated successfully.'}, status=200)

    except BorrowRecord.DoesNotExist:
        return JsonResponse({'error': 'Borrow record not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import BorrowRecord
def get_book_count(request):
    count = Book.objects.count()
    return JsonResponse({"count": count})
