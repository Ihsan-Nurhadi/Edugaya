from django.contrib import admin
from .models import LearningCharacteristic, Student

admin.site.register(LearningCharacteristic)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'result', 'submitted_at')
    
    def result(self, obj):
        # Mengganti None dengan teks yang lebih informatif
        return obj.result if obj.result else 'Belum dipilih'
    
    result.admin_order_field = 'result'  # Agar bisa diurutkan berdasarkan result
admin.site.register(Student)
