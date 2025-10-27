from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="books.index"),                # /books/
    path("index.html", views.index),                          # /books/index.html (اختياري)
    path("list_books/", views.list_books, name="books.list_books"),
    path("list_books.html", views.list_books),                # اختياري
    path("aboutus/", views.aboutus, name="books.aboutus"),
    path("aboutus.html", views.aboutus),                      # اختياري
    path("<int:bookId>/", views.viewbook, name="books.view_one_book"),
    path("list_books/one_book.html", views.viewbook),  # you’d also need to handle bookId
    path('html5/links', views.links_page_view, name='links_page'),
    # ... (داخل urlpatterns)
path('html5/text/formatting', views.text_formatting_view, name='text_formatting_page'),
# ... (داخل urlpatterns)
path('html5/listing', views.listing_page_view, name='listing_page'),
# ... (داخل urlpatterns)
path('html5/tables', views.tables_page_view, name='tables_page'),
    path('search/', views.search_view, name='books-search'),
    path('simple/query', views.simple_query, name='books-simple_query'),
    path('lookup/query', views.lookup_query, name='books-lookup_query'),
    
]