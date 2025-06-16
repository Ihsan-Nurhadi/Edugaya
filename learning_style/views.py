from django.shortcuts import render, redirect
from .forms import LearningStyleForm
from .naive_bayes import naive_bayes_predict
from .models import LearningCharacteristic # Gunakan model Student

def questionnaire_view(request):
    result = None
    category_posterior = None  # Untuk menampung perhitungan posterior

    # Mengambil dan mengurutkan data LearningCharacteristic berdasarkan code
    characteristics = LearningCharacteristic.objects.all().order_by('code')

    if request.method == 'POST':
        form = LearningStyleForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']  # Ambil data student yang dipilih
            selected = form.cleaned_data['selected']
            
            # Mendapatkan prediksi dan posterior
            result, category_posterior = naive_bayes_predict(selected)

            # Menyimpan hasil prediksi ke objek Student
            student.selected_choices = ",".join(selected)  # Simpan pilihan yang dipilih
            student.result = result  # Simpan gaya belajar yang diprediksi
            student.save()  # Simpan perubahan ke database

            # Redirect ke halaman hasil (agar form kosong lagi)
            return render(request, 'learning_style/result.html', {
                'result': result, 
                'name': student.name,  # Kirimkan nama student untuk ditampilkan
                'category_posterior': category_posterior  # Kirimkan perhitungan posterior
            })
    else:
        form = LearningStyleForm()

    # Mengurutkan pilihan berdasarkan code
    form.fields['selected'].choices = [(char.id, f"{char.code}. {char.question}") for char in characteristics]

    return render(request, 'learning_style/questionnaire.html', {'form': form})