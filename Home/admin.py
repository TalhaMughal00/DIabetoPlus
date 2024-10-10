from django.contrib import admin
from Home.models import feedback
from django.urls import path
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import NewsletterSubscriber

class feedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback', 'created_at')
admin.site.register(feedback, feedbackAdmin)

# View For Sending NewsLetter
class NewsletterAdmin(admin.ModelAdmin):
    change_list_template = "admin/send_newsletter.html"  # Custom template path

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter_view), name='send_newsletter'),
        ]
        return custom_urls + urls

    def send_newsletter_view(self, request):
        if request.method == "POST":
            subject = request.POST.get('subject', None)
            message = request.POST.get('message', None)

            if subject and message:
                # Fetch all subscriber emails
                subscribers = NewsletterSubscriber.objects.values_list('email', flat=True)
                
                if subscribers:  # Ensure there are subscribers
                    # Send the email to all subscribers
                    send_mail(subject, message, 'diabetoplus@gmail.com', list(subscribers), fail_silently=False)
                    self.message_user(request, "Newsletter sent successfully!")
                else:
                    self.message_user(request, "No subscribers found.")
                return redirect('admin:index')  # Redirect to the same page
            else:
                self.message_user(request, "Please fill in both the subject and message.")

        # Render the newsletter form template
        return render(request, 'admin/send_newsletter.html')

# Register the NewsletterSubscriber model with the custom admin class
admin.site.register(NewsletterSubscriber, NewsletterAdmin)
