from django.shortcuts import render
from django.http import HttpResponse

from django.contrib import messages

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from .forms import UploadJson
import json

# Create your views here.
def home(request):
    if request.method == "POST":
        email = request.POST.get('mail')
        body = request.POST.get('body')
        mail_subject = request.POST.get('mail_subject')
        from_email = request.POST.get('from_mail')
        validate_email(email)
        try:
            send_mail(mail_subject, body,from_email,[email],  fail_silently=False)
            messages.success(request, "Email has been sent successfully!")
        except:
            messages.error(request, "Failed to send message, Please try again!")

        return render(request, 'home.html')
    return render(request, 'home.html')

def uploadfiles(request):
    if request.method == "POST":
        form = UploadJson(request.POST, request.FILES)
        if form.is_valid(): 
            file = form.cleaned_data['file']
            if not file.name.endswith('.json'):
                messages.error(request, 'You can only upload JSON files!')
                return render(request, 'uploadfile.html', {'uploadjson':UploadJson})
            file_content = file.read().decode('utf-8')
            json_string = json.loads(file_content)
            global emails 
            emails = []
            invalid_email = []
            invalid_num = 0
            for data in json_string:
                invalid_num +=1
                emails.append(data['email'])
                if validate_email(data['email']) == False:
                    invalid_email.append(data['email'])
                    emails.remove(data['email'])
            valid_email = emails[:6]
            invalid_email = invalid_email[:6]
            valid_num = len(emails)
            total = invalid_num
            invalid_num = invalid_num - valid_num
            context = {
                'valid_email' : valid_email,
                'invalid_email' : invalid_email,
                'valid_num': valid_num,
                'invalid_num': invalid_num,
                'total': total,
            }
            return render(request, 'uploadfile.html',context)
        else:
            print("File is not valid")
    else:
        form = UploadJson()
    return render(request, 'uploadfile.html', {'uploadjson':UploadJson})

def sendmail(request):
    email = emails
    print(email)
    if request.method == "POST":
        subject = request.POST.get('mail_subject')
        message = request.POST.get('message')
        from_mail = request.POST.get('from_mail')

        #getting emails from the uploadfiles function using global variable
        send_mail(subject, message,from_mail ,email,  fail_silently=False)
    return render(request, 'sendMassmail.html')

def About(request):
    return render(request, 'About.html')