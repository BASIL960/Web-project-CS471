from django.urls import path
from . import views

urlpatterns = [
    # --- الصفحات العامة ---
    path("", views.index, name="books.index"),
    path("index.html", views.index),
    path("list_books/", views.list_books, name="books.list_books"),
    path("list_books.html", views.list_books),
    path("aboutus/", views.aboutus, name="books.aboutus"),
    path("aboutus.html", views.aboutus),
    path("<int:bookId>/", views.viewbook, name="books.view_one_book"),
    path("list_books/one_book.html", views.viewbook),
    
    # --- HTML5 Pages ---
    path('html5/links', views.links_page_view, name='links_page'),
    path('html5/text/formatting', views.text_formatting_view, name='text_formatting_page'),
    path('html5/listing', views.listing_page_view, name='listing_page'),
    path('html5/tables', views.tables_page_view, name='tables_page'),

    # --- Search & Query ---
    path('search/', views.search_view, name='books-search'),
    path('simple/query', views.simple_query, name='books-simple_query'),
    path('lookup/query', views.lookup_query, name='books-lookup_query'),
    
    # --- Lab 8 URLs ---
    path('lab8/task1/', views.lab8_task1, name="lab8.task1"),
    path('lab8/task2/', views.lab8_task2, name="lab8.task2"),
    path('lab8/task3/', views.lab8_task3, name="lab8.task3"),
    path('lab8/task4/', views.lab8_task4, name="lab8.task4"),
    path('lab8/task5/', views.lab8_task5, name="lab8.task5"),
    path('lab8/task7/', views.lab8_task7, name="lab8.task7"),

    # --- Lab 9 URLs ---
    path('lab9/task1/', views.lab9_task1, name='lab9_task1'),
    path('lab9/task2/', views.lab9_task2, name='lab9_task2'),
    path('lab9/task3/', views.lab9_task3, name='lab9_task3'),
    path('lab9/task4/', views.lab9_task4, name='lab9_task4'),
    path('lab9/task5/', views.lab9_task5, name='lab9_task5'),
    path('lab9/task6/', views.lab9_task6, name='lab9_task6'),

    # --- Lab 10: Task 1 URLs ---
    path('lab10/students/', views.list_students, name='list_students'),
    path('lab10/students/add/', views.create_student, name='add_student'),
    path('lab10/students/update/<int:pk>/', views.update_student, name='update_student'),
    path('lab10/students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # --- Lab 10: Task 2 URLs ---
    path('lab10/students2/', views.list_students2, name='list_students2'),
    path('lab10/students2/add/', views.create_student2, name='add_student2'),
    path('lab10/students2/update/<int:pk>/', views.update_student2, name='update_student2'),
    path('lab10/students2/delete/<int:pk>/', views.delete_student2, name='delete_student2'),

    # --- Lab 10: Task 3 URLs (Images) ---
    path('lab10/images/', views.list_images, name='list_images'),
    path('lab10/images/upload/', views.upload_image, name='upload_image'),
    path('lab10/images/delete/<int:pk>/', views.delete_image, name='delete_image'),
]