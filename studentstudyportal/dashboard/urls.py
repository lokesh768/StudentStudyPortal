from django.urls import path
from dashboard.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   # Notes Section URLs   
   path('',home,name='home'),
   path('notes/',notes,name='notes'),
   path('delete_note/<int:pk>/',delete_note,name='delete-note'),
   path('notes_detail/<int:pk>/',NotesDetailView.as_view(),name='notes-detail'),

   #Homework Section URLs
   path('homework/',homework,name='homework'),
   path('update_homework/<int:pk>',update_homework,name='update-homework'),
   path('delete_homework/<int:pk>',delete_homwork,name='delete-homework'),

   # Youtube Section URLs
   path('youtube/',youtube,name='youtube'),

   # Todo Section URLs
   path('todo/',todo,name='todo'),
   path('update_todo/<int:pk>',update_todo,name='update-todo'),
   path('delete_todo/<int:pk>',delete_todo,name='delete-todo'),

   # Books Section URLs
   path('books/',books,name='books'),

   # Dictionary Section URLs
   path('dictionary/',dictionary,name='dictionary'),

   # Wikipedia Section URLs
   path('wiki/',wiki,name='wiki'),

   # Conversions Section URLs
   path('conversion/',conversion,name='conversion'),

   # Registration URL
   path('register/',register,name='register'),

   # Login URL
   path('login/',auth_views.LoginView.as_view(template_name="dashboard/login.html"),name='login'),

   # Profile URL
   path('profile/',profile,name='profile'),
 
   # Logout URL
   path('logout/',logout_page,name='logout'),

]