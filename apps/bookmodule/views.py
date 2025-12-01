from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, Count, Sum, Avg, Max, Min, F, FloatField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required

# استيراد النماذج (يجب عليك التأكد من استيراد كل ما تحتاجه)
from .models import Book, Address, Student, Publisher, Student2, StudentImage

# استيراد نماذج النماذج (Forms)
from .forms import StudentForm, Student2Form, StudentImageForm, BookForm # BookForm مضافة لمهام Lab 10


# الدوال الأولية لتمهيد المشروع
def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))

def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})

def viewbook(request, bookId):
    # Lab 6: Simple viewbook logic
    book1 = {'id': 123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
    book2 = {'id': 456, 'title': 'Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId:
        targetBook = book1
    if book2['id'] == bookId:
        targetBook = book2
    context = {'book': targetBook}
    return render(request, 'bookmodule/show.html', context)

def aboutus(request):
    # Lab 6
    return render(request, "bookmodule/aboutus.html")

def links_page_view(request):
    # Lab 6
    return render(request, 'bookmodule/links.html')

def text_formatting_view(request):
    # Lab 6
    return render(request, 'bookmodule/text_formatting.html')

def listing_page_view(request):
    # Lab 6
    return render(request, 'bookmodule/listing.html')

def tables_page_view(request):
    # Lab 6
    return render(request, 'bookmodule/tables.html')

def __getBooksList():
    # Helper for search_view (Lab 7)
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]

def search_view(request):
    # Lab 7: Search logic
    if request.method == "POST":
        string = request.POST.get('keyword', '').strip().lower()
        isTitle = request.POST.get('option1') is not None
        isAuthor = request.POST.get('option2') is not None

        books = __getBooksList()
        new_books = []
        for item in books:
            contained = False
            if isTitle and string and string in item['title'].lower():
                contained = True
            if (not contained) and isAuthor and string and string in item['author'].lower():
                contained = True
            if contained:
                new_books.append(item)
        return render(request, 'bookmodule/bookList.html', {'books': new_books})
    return render(request, 'bookmodule/search.html')


# =========================================
# Lab 8: Django Models (Part 2)
# =========================================

def simple_query(request):
    # Lab 8: Simple query (Example)
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def lookup_query(request):
    # Lab 8: Advanced lookup (Example)
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def lab8_task1(request):
    # Lab 8: Task 1 (Q operator: price <= 80)
    # [cite_start]التصحيح: تم تعديل القيمة من 50 إلى 80 لتتوافق مع متطلب المختبر [cite: 25]
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task2(request):
    # [cite_start]Lab 8: Task 2 (editions > 3 AND (title OR author contains 'qu')) [cite: 26]
    query = Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task3(request):
    # [cite_start]Lab 8: Task 3 (editions <= 3 AND (NOT (title OR author contains 'qu'))) [cite: 27]
    query = Q(edition__lte=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task4(request):
    # [cite_start]Lab 8: Task 4 (Ordering by title) [cite: 28]
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task5(request):
    # [cite_start]Lab 8: Task 5 (Aggregation functions) [cite: 29]
    aggs = Book.objects.aggregate(
        book_count=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/aggregates.html', {'aggs': aggs})

def lab8_task7(request):
    # [cite_start]Lab 8: Task 7 (Count students per city) [cite: 45]
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/city_counts.html', {'cities': cities})


# =========================================
# Lab 9: Django Models (Part 3)
# =========================================

def lab9_task1(request):
    # [cite_start]Lab 9: Task 1 (Percentage Availability) [cite: 83]
    total_stock_data = Book.objects.aggregate(total=Sum('quantity'))
    total_stock = total_stock_data['total'] or 0
    books = Book.objects.all()
    if total_stock > 0:
        books = books.annotate(
            percentage=(Cast(F('quantity'), FloatField()) * 100.0) / total_stock
        )
    context = {'books': books, 'total_stock': total_stock, 'task_title': 'Task 1: Percentage Availability'}
    return render(request, 'bookmodule/lab9_results.html', context)

def lab9_task2(request):
    # [cite_start]Lab 9: Task 2 (Publisher Total Book Stock) [cite: 86]
    publishers = Publisher.objects.annotate(
        total_book_stock=Sum('books__quantity')
    )
    context = {'publishers': publishers, 'task_title': 'Task 2: Publisher Total Book Stock'}
    return render(request, 'bookmodule/lab9_results.html', context)

def lab9_task3(request):
    # [cite_start]Lab 9: Task 3 (Oldest Book Date Per Publisher) [cite: 87]
    publishers = Publisher.objects.annotate(
        oldest_book_date=Min('books__pubdate')
    )
    context = {'publishers': publishers, 'task_title': 'Task 3: Oldest Book Date Per Publisher'}
    return render(request, 'bookmodule/lab9_results.html', context)

def lab9_task4(request):
    # [cite_start]Lab 9: Task 4 (Min, Max, and Average Price Per Publisher) [cite: 88]
    publishers = Publisher.objects.annotate(
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price')
    )
    context = {'publishers': publishers, 'task_title': 'Task 4: Min, Max, and Average Price Per Publisher'}
    return render(request, 'bookmodule/lab9_results.html', context)

def lab9_task5(request):
    # [cite_start]Lab 9: Task 5 (Count of Highly Rated Books Per Publisher) [cite: 93]
    publishers = Publisher.objects.annotate(
        high_rated_count=Count('books', filter=Q(books__rating__gte=4))
    ).filter(high_rated_count__gt=0)
    context = {'publishers': publishers, 'task_title': 'Task 5: Count of Highly Rated Books Per Publisher (Rating >= 4)'}
    return render(request, 'bookmodule/lab9_results.html', context)

def lab9_task6(request):
    # [cite_start]Lab 9: Task 6 (Count of Filtered Books Per Publisher) [cite: 94]
    filter_condition = Q(books__price__gt=50) & Q(books__quantity__gte=1) & Q(books__quantity__lt=5)
    publishers = Publisher.objects.annotate(
        filtered_book_count=Count('books', filter=filter_condition)
    ).filter(filtered_book_count__gt=0)
    context = {'publishers': publishers, 'task_title': 'Task 6: Count of Filtered Books Per Publisher'}
    return render(request, 'bookmodule/lab9_results.html', context)

def list_books(request):
    return render(request, 'bookmodule/list_books.html')
# =========================================
# Lab 10: Django Forms (Part 1) - CRUD for Book
# =========================================

# Lab 10: Part 1 - CRUD بدون استخدام نماذج جانقو (Book Model)
# هذه الدوال كانت مفقودة، وقد تم إضافتها.

def list_books_no_form(request):
    # [cite_start]Lab 10: Task 1 (Part 1: List books without form) [cite: 55]
    books = Book.objects.all()
    context = {'books': books, 'task_title': 'Lab 10: Part 1 - List Books (No Forms)'}
    return render(request, 'bookmodule/lab10_book_list_no_form.html', context)

def add_book_no_form(request):
    # Lab 10: Task 2 (Part 1: Add book without form)
    if request.method == 'POST':
        # نستقبل البيانات من الطلب
        title = request.POST.get('title')
        price = request.POST.get('price')
        author = request.POST.get('author') # حقل ضروري حسب المودل الخاص بك
        
        # إنشاء الكتاب وحفظه
        Book.objects.create(
            title=title,
            price=price,
            author=author,
            # الحقول الأخرى (quantity, rating, etc) ستأخذ القيم الافتراضية (Default)
        )
        return redirect('list_books_no_form')
    return render(request, 'bookmodule/lab10_add_book_no_form.html')

def edit_book_no_form(request, pk):
    # [cite_start]Lab 10: Task 3 (Part 1: Edit book without form) [cite: 58]
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.price = request.POST.get('price')
        # ... تحديث باقي الحقول
        book.save()
        return redirect('list_books_no_form')
    return render(request, 'bookmodule/lab10_edit_book_no_form.html', {'book': book})

def delete_book_no_form(request, pk):
    # [cite_start]Lab 10: Task 4 (Part 1: Delete book without form) [cite: 59]
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books_no_form')
    return render(request, 'bookmodule/lab10_delete_book_confirm.html', {'obj_name': book.title})

# Lab 10: Part 2 - CRUD باستخدام نماذج جانقو (Book Model)
# هذه الدوال كانت مفقودة، وقد تم إضافتها.

def list_books_with_form(request):
    # [cite_start]Lab 10: Task 1 (Part 2: List books with form) [cite: 61]
    books = Book.objects.all()
    context = {'books': books, 'task_title': 'Lab 10: Part 2 - List Books (With Forms)'}
    return render(request, 'bookmodule/lab10_book_list_with_form.html', context)

def add_book_with_form(request):
    # [cite_start]Lab 10: Task 2 (Part 2: Add book with form) [cite: 61]
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_books_with_form')
    return render(request, 'bookmodule/lab10_book_form.html', {'form': form, 'page_title': 'Add Book'})

def edit_book_with_form(request, pk):
    # [cite_start]Lab 10: Task 3 (Part 2: Edit book with form) [cite: 61]
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books_with_form')
    return render(request, 'bookmodule/lab10_book_form.html', {'form': form, 'page_title': 'Edit Book'})

def delete_book_with_form(request, pk):
    # [cite_start]Lab 10: Task 4 (Part 2: Delete book with form) [cite: 61]
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books_with_form')
    return render(request, 'bookmodule/lab10_delete_book_confirm.html', {'obj_name': book.title})


# =========================================
# Lab 11: Django Forms (Part 2) - Relations & File Handling
# =========================================

# @login_required
def list_students(request):
    # [cite_start]Lab 11: Task 1 (One-to-One/Many List) [cite: 11]
    students = Student.objects.all()
    context = {'students': students, 'view_type': 'list', 'task_type': 'task1', 'page_title': 'Task 1: Students List'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def create_student(request):
    # [cite_start]Lab 11: Task 1 (One-to-One/Many Create) [cite: 11]
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_students')
    context = {'form': form, 'view_type': 'form', 'task_type': 'task1', 'page_title': 'Add Student (Task 1)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def update_student(request, pk):
    # [cite_start]Lab 11: Task 1 (One-to-One/Many Update) [cite: 11]
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('list_students')
    context = {'form': form, 'view_type': 'form', 'task_type': 'task1', 'page_title': 'Edit Student (Task 1)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def delete_student(request, pk):
    # [cite_start]Lab 11: Task 1 (One-to-One/Many Delete) [cite: 11]
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students')
    context = {'obj_name': student.name, 'view_type': 'delete', 'task_type': 'task1', 'page_title': 'Delete Student (Task 1)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def list_students2(request):
    # [cite_start]Lab 11: Task 2 (Many-to-Many List) [cite: 12]
    students = Student2.objects.all()
    context = {'students': students, 'view_type': 'list', 'task_type': 'task2', 'page_title': 'Task 2: Students List'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def create_student2(request):
    # [cite_start]Lab 11: Task 2 (Many-to-Many Create) [cite: 12]
    form = Student2Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_students2')
    context = {'form': form, 'view_type': 'form', 'task_type': 'task2', 'page_title': 'Add Student (Task 2)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def update_student2(request, pk):
    # [cite_start]Lab 11: Task 2 (Many-to-Many Update) [cite: 12]
    student = get_object_or_404(Student2, pk=pk)
    form = Student2Form(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('list_students2')
    context = {'form': form, 'view_type': 'form', 'task_type': 'task2', 'page_title': 'Edit Student (Task 2)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def delete_student2(request, pk):
    # [cite_start]Lab 11: Task 2 (Many-to-Many Delete) [cite: 12]
    student = get_object_or_404(Student2, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students2')
    context = {'obj_name': student.name, 'view_type': 'delete', 'task_type': 'task2', 'page_title': 'Delete Student (Task 2)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def list_images(request):
    # [cite_start]Lab 11: Task 3 (Image List) [cite: 15]
    try:
        images = StudentImage.objects.all()
    except NameError:
        images = []
    context = {'images': images, 'view_type': 'list', 'task_type': 'task3', 'page_title': 'Task 3: Image Gallery'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def upload_image(request):
    # [cite_start]Lab 11: Task 3 (Image Upload) [cite: 15]
    if request.method == 'POST':
        form = StudentImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_images')
    else:
        form = StudentImageForm()
    context = {'form': form, 'view_type': 'form', 'task_type': 'task3', 'page_title': 'Upload Image (Task 3)'}
    return render(request, 'bookmodule/lab10_master.html', context)

# @login_required
def delete_image(request, pk):
    # [cite_start]Lab 11: Task 3 (Image Delete) [cite: 15]
    image = get_object_or_404(StudentImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('list_images')
    context = {'obj_name': image.title, 'view_type': 'delete', 'task_type': 'task3', 'page_title': 'Delete Image'}
    return render(request, 'bookmodule/lab10_master.html', context)