from django.shortcuts import render

from django.http import HttpResponse
from .models import Book, Address, Student  # Import models for Lab 8
from django.db.models import Q, Count, Sum, Avg, Max, Min # Needed for Lab 8
# def index(request):
#  name = request.GET.get("name") or "world!" #add this line
#  return HttpResponse("Helloa, "+name) #replace the word “world!”
# apps/bookmodule/views.py
from django.shortcuts import render
# استيرادات Aggregations و الدوال الرياضية
from django.db.models import Sum, F, FloatField, Min, Max, Avg, Count, Q
from django.db.models.functions import Cast
# استيراد النماذج
from .models import Book, Publisher 
# الاستيرادات من المسار الرئيسي
from django.db.models import Sum, F
# في apps/bookmodule/views.py

# تأكد من إضافة StudentImageForm إلى هذا السطر
from .forms import StudentForm, Student2Form, StudentImageForm
# الاستيرادات الخاصة بدوال قاعدة البيانات (يجب عليك إضافة هذا السطر)
from django.db.models.functions import Cast 
from django.db.models import FloatField # FloatField غالباً موجودة في models مباشرة
def index2(request, val1 = 0): #add the view function (index2)
  return HttpResponse("value1 = "+str(val1))

# def index(request):
#  name = request.GET.get("name") or "world!"
#  return render(request, "bookmodule/index.html") #Change HttpResponse to render function

def index(request):
 name = request.GET.get("name") or "world!"
 return render(request, "bookmodule/index.html" , {"name": name}) #y


def viewbook(request, bookId):
 # assume that we have the following books somewhere (e.g. database)
 book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
 book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
 targetBook = None
 if book1['id'] == bookId: targetBook = book1
 if book2['id'] == bookId: targetBook = book2
 context = {'book':targetBook} # book is the variable name accessible by the template
 return render(request, 'bookmodule/show.html', context)

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")


def links_page_view(request):
    return render(request, 'bookmodule/links.html')

def text_formatting_view(request):
    return render(request, 'bookmodule/text_formatting.html')

def listing_page_view(request):
    return render(request, 'bookmodule/listing.html')

def tables_page_view(request):
    return render(request, 'bookmodule/tables.html')


def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]
def search_view(request):
    if request.method == "POST":
        string = request.POST.get('keyword','').strip().lower()
        # checkbox غير المؤشر يعيد None، فإذا كان موجوداً يعود 'on'
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

def simple_query(request):
    # Retrieve multiple objects: books where the title contains 'and' (case-insensitive) [cite: 413]
    mybooks = Book.objects.filter(title__icontains='and')
    
    # Render the results using the bookList.html template [cite: 413]
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def lookup_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/bookList.html', {'books': []})
    

def lab8_task1(request):
    # List books that have price less than or equal 50 using Q operator
    books = Book.objects.filter(Q(price__lte=50))
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task2(request):
    # List books with editions > 2 AND (title OR author contains 'qu')
    query = Q(edition__gt=2) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task3(request):
    # Opposite of Task 2: editions <= 2 AND (neither title nor author contains 'qu')
    query = Q(edition__lte=2) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    books = Book.objects.filter(query)
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task4(request):
    # List books and order by their titles
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/bookList.html', {'books': books})

def lab8_task5(request):
    # Display count, total, average, max, and min price
    aggs = Book.objects.aggregate(
        book_count=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/aggregates.html', {'aggs': aggs})

def lab8_task7(request):
    # Show the number of students in each city 
    # We use annotate() to group by Address and add a 'student_count' field
    cities = Address.objects.annotate(student_count=Count('student'))
    return render(request, 'bookmodule/city_counts.html', {'cities': cities})

# ------------------------------------
def lab9_task1(request):
    # 1. نحسب إجمالي مخزون جميع الكتب
    total_stock_data = Book.objects.aggregate(total=Sum('quantity'))
    total_stock = total_stock_data['total'] or 0

    books = Book.objects.all()

    if total_stock > 0:
        # 2. نستخدم annotate لإضافة حقل 'percentage'
        # نستخدم Cast لتحويل الكمية إلى Float لضمان دقة عملية القسمة.
        books = books.annotate(
            percentage=(Cast(F('quantity'), FloatField()) * 100.0) / total_stock
        )

    context = {
        'books': books,
        'total_stock': total_stock,
        'task_title': 'Task 1: Percentage Availability'
    }
    return render(request, 'bookmodule/lab9_results.html', context)


# ------------------------------------
# Task 2: الناشرين وإجمالي مخزون كتبهم
# (تم التصحيح لاستخدام 'books__quantity')
# ------------------------------------
def lab9_task2(request):
    # نستخدم annotate على نموذج Publisher لحساب مجموع الكميات (quantity) للكتب المرتبطة (books)
    publishers = Publisher.objects.annotate(
        total_book_stock=Sum('books__quantity')
    )

    context = {
        'publishers': publishers,
        'task_title': 'Task 2: Publisher Total Book Stock'
    }
    return render(request, 'bookmodule/lab9_results.html', context)


# ------------------------------------
# Task 3: أقدم كتاب لكل ناشر
# (تم التصحيح لاستخدام 'books__pubdate')
# ------------------------------------
def lab9_task3(request):
    # نستخدم annotate على نموذج Publisher لإيجاد أقل (Min) تاريخ نشر (pubdate)
    publishers = Publisher.objects.annotate(
        oldest_book_date=Min('books__pubdate')
    )
    
    context = {
        'publishers': publishers,
        'task_title': 'Task 3: Oldest Book Date Per Publisher'
    }
    return render(request, 'bookmodule/lab9_results.html', context)


# ------------------------------------
# Task 4: حساب متوسط، أدنى، وأقصى سعر لكل ناشر
# (تم التصحيح لاستخدام 'books__price')
# ------------------------------------
def lab9_task4(request):
    # نستخدم annotate لحساب ثلاثة تجميعات (Avg, Min, Max) على حقل السعر (price)
    publishers = Publisher.objects.annotate(
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price')
    )
    
    context = {
        'publishers': publishers,
        'task_title': 'Task 4: Min, Max, and Average Price Per Publisher'
    }
    return render(request, 'bookmodule/lab9_results.html', context)


# ------------------------------------
# Task 5: الناشرين وعدد الكتب ذات التقييم العالي (Rating >= 4)
# (تم التصحيح لاستخدام 'books')
# ------------------------------------
def lab9_task5(request):
    # نستخدم filter مع Count لإيجاد عدد الكتب ذات التقييم >= 4 لكل ناشر
    publishers = Publisher.objects.annotate(
        high_rated_count=Count('books', filter=Q(books__rating__gte=4))
    ).filter(high_rated_count__gt=0) 

    context = {
        'publishers': publishers,
        'task_title': 'Task 5: Count of Highly Rated Books Per Publisher (Rating >= 4)'
    }
    return render(request, 'bookmodule/lab9_results.html', context)


# ------------------------------------
# Task 6: عدد الكتب المفلترة لكل ناشر
# (تم التصحيح لاستخدام 'books')
# ------------------------------------
def lab9_task6(request):
    # شروط التصفية: (price > 50) AND (1 <= quantity < 5)
    filter_condition = Q(books__price__gt=50) & Q(books__quantity__gte=1) & Q(books__quantity__lt=5)

    # نستخدم Count مع التصفية داخل دالة annotate
    publishers = Publisher.objects.annotate(
        filtered_book_count=Count('books', filter=filter_condition)
    ).filter(filtered_book_count__gt=0)

    context = {
        'publishers': publishers,
        'task_title': 'Task 6: Count of Filtered Books Per Publisher'
    }
    return render(request, 'bookmodule/lab9_results.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # ضروري لـ Task 3
# استيراد النماذج
from .models import Student, Student2, StudentImage
# استيراد الفورمات
from .forms import StudentForm, Student2Form, StudentImageForm

# --- دوال Lab 9 (يمكن تركها بدون حماية أو حمايتها حسب الرغبة) ---
# ... (يمكنك ترك دوال lab9_task1 إلخ كما هي، التركيز في Lab 11 على Lab 10) ...
# سأضع هنا فقط دوال Lab 10 مع الحماية المطلوبة

# =========================================
#  Lab 10: Task 1 (Student One-to-Many)
# =========================================

@login_required # حماية صفحة العرض
def list_students(request):
    students = Student.objects.all()
    context = {
        'students': students,
        'view_type': 'list',
        'task_type': 'task1',
        'page_title': 'Task 1: Students List',
        'user': request.user # لتظهر في القالب
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required # حماية صفحة الإضافة
def create_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_students')
    context = {
        'form': form,
        'view_type': 'form',
        'task_type': 'task1',
        'page_title': 'Add Student (Task 1)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required # حماية صفحة التعديل
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('list_students')
    context = {
        'form': form,
        'view_type': 'form',
        'task_type': 'task1',
        'page_title': 'Edit Student (Task 1)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required # حماية صفحة الحذف
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students')
    context = {
        'obj_name': student.name,
        'view_type': 'delete',
        'task_type': 'task1',
        'page_title': 'Delete Student (Task 1)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

# =========================================
#  Lab 10: Task 2 (Student Many-to-Many)
# =========================================

@login_required
def list_students2(request):
    students = Student2.objects.all()
    context = {
        'students': students,
        'view_type': 'list',
        'task_type': 'task2',
        'page_title': 'Task 2: Students List',
        'user': request.user
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required
def create_student2(request):
    form = Student2Form(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_students2')
    context = {
        'form': form,
        'view_type': 'form',
        'task_type': 'task2',
        'page_title': 'Add Student (Task 2)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required
def update_student2(request, pk):
    student = get_object_or_404(Student2, pk=pk)
    form = Student2Form(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('list_students2')
    context = {
        'form': form,
        'view_type': 'form',
        'task_type': 'task2',
        'page_title': 'Edit Student (Task 2)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required
def delete_student2(request, pk):
    student = get_object_or_404(Student2, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students2')
    context = {
        'obj_name': student.name,
        'view_type': 'delete',
        'task_type': 'task2',
        'page_title': 'Delete Student (Task 2)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

# =========================================
#  Lab 10: Task 3 (Image Upload)
# =========================================

@login_required
def list_images(request):
    try:
        images = StudentImage.objects.all()
    except NameError:
        images = []
    context = {
        'images': images,
        'view_type': 'list',
        'task_type': 'task3',
        'page_title': 'Task 3: Image Gallery',
        'user': request.user
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = StudentImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_images')
    else:
        form = StudentImageForm()
    context = {
        'form': form,
        'view_type': 'form',
        'task_type': 'task3',
        'page_title': 'Upload Image (Task 3)'
    }
    return render(request, 'bookmodule/lab10_master.html', context)

@login_required
def delete_image(request, pk):
    image = get_object_or_404(StudentImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        return redirect('list_images')
    context = {
        'obj_name': image.title,
        'view_type': 'delete',
        'task_type': 'task3',
        'page_title': 'Delete Image'
    }
    return render(request, 'bookmodule/lab10_master.html', context)
