from django.contrib import admin
from .models import Profile,PatientTest

# Register your models here.

# admin.site.register(Profile)
# admin.site.register(PatientTest)
@admin.register(PatientTest)
class PatientTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'age', 'blood_pressure', 'prediction')
    search_fields = ('profile__user__username', 'prediction')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')