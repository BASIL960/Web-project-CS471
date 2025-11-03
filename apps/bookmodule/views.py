from django.shortcuts import render

from django.http import HttpResponse
from .models import Book, Address, Student  # Import models for Lab 8
from django.db.models import Q, Count, Sum, Avg, Max, Min # Needed for Lab 8
# def index(request):
#  name = request.GET.get("name") or "world!" #add this line
#  return HttpResponse("Helloa, "+name) #replace the word “world!”

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