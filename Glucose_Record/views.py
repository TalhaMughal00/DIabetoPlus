from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GRecords
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

@login_required
def record(request):
    user_records = GRecords.objects.filter(user=request.user).order_by('-date')
    return render(request, 'glucose_record.html', {'Glucose_Record': user_records})

@login_required
def add_record(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        mor_fast = request.POST.get('mor_fast', '')
        mor_after = request.POST.get('mor_after', '')
        evening = request.POST.get('evening', '')
        night_fast = request.POST.get('night_fast', '')
        night_after = request.POST.get('night_after', '')

        # Check if date is provided
        if not date:
            messages.error(request, 'Date is required.')
            return render(request, 'glucose_record.html')

        # Check if a record with the same date already exists for the user
        if GRecords.objects.filter(user=request.user, date=date).exists():
            messages.error(request, 'A record with this date already exists.')
        else:
            try:
                record = GRecords(
                    user=request.user,
                    date=date,
                    mor_fast=int(mor_fast) if mor_fast.strip() else None,
                    mor_after=int(mor_after) if mor_after.strip() else None,
                    evening=int(evening) if evening.strip() else None,
                    night_fast=int(night_fast) if night_fast.strip() else None,
                    night_after=int(night_after) if night_after.strip() else None
                )
                record.save()
                messages.success(request, 'New Record has been added successfully')
            except Exception as e:
                messages.error(request, 'An error occurred while saving the record.')
        return redirect('record')
    return render(request, 'glucose_record.html')


@login_required
def clear_records(request):
    if request.method == 'POST':
        if GRecords.objects.filter(user=request.user).exists():
            GRecords.objects.filter(user=request.user).delete()
            messages.info(request, 'All Records Have been Cleared')
        else:
            messages.info(request, 'No Records to clear.')
    return redirect('record')

def delete_record(request, pk):
    if request.method == 'POST':
        record = get_object_or_404(GRecords, id=pk, user=request.user)
        record.delete()
        messages.success(request, 'Record deleted successfully.')
    return redirect('record')

@login_required
def update_record(request, pk):
    record = get_object_or_404(GRecords, id=pk, user=request.user)

    if request.method == 'POST':
        date = request.POST.get('date')
        mor_fast = request.POST.get('mor_fast', '')
        mor_after = request.POST.get('mor_after', '')
        evening = request.POST.get('evening', '')
        night_fast = request.POST.get('night_fast', '')
        night_after = request.POST.get('night_after', '')

        # Validate data and update record
        if not date:
            messages.error(request, 'Date is required.')
        else:
            try:
                record.date = date
                record.mor_fast = int(mor_fast) if mor_fast.strip() else None
                record.mor_after = int(mor_after) if mor_after.strip() else None
                record.evening = int(evening) if evening.strip() else None
                record.night_fast = int(night_fast) if night_fast.strip() else None
                record.night_after = int(night_after) if night_after.strip() else None
                record.save()
                messages.success(request, 'Record has been updated successfully.')
            except Exception as e:
                messages.error(request, 'An error occurred while updating the record.')
        return redirect('record')

    return render(request, 'glucose_record.html', {'record': record})

@login_required
def gen_pdf(request):
    # Fetch user records
    user_records = GRecords.objects.filter(user=request.user).order_by('date')

    # Define the template and context
    template_path = 'PDF.html'  # Name of your HTML template
    context = {
        'Glucose_Record': user_records,  # Context key for records
        'request': request  # Passing request to access request.user in the template
    }
    response = BytesIO()

    # Generate the PDF
    try:
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        # Create the HttpResponse with the correct content type and headers
        pdf_response = HttpResponse(response.getvalue(), content_type='application/pdf')
        pdf_response['Content-Disposition'] = 'attachment; filename="glucose_records.pdf"'
        return pdf_response
    except Exception as e:
        return HttpResponse(f'An error occurred: {e}')

