from django.urls import path

from .views import (
    CreateBookView,
    BookView
)

app_name = "Book"

urlpatterns = [
    path('', CreateBookView.as_view(), name="CreateBook"),
    path('<int:book_id>/', BookView.as_view(), name="Book")
]
