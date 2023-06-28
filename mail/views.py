from django.shortcuts import render
from django.http import HttpResponse

from django.contrib import messages

from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from .forms import UploadJson
import json

#for email extraction 
import re
from bs4 import BeautifulSoup
import requests

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



def EmailExtractor(request):
    allLinks = [];mails=[]
    if request.method == "POST":
        url = request.POST.get('link')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.attrs.get('href') for a in soup.select('a[href]') ]
        for i in links:
            if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i)or('Support' in i or 'support' in i):
                allLinks.append(i)
        allLinks = set(allLinks)
        def findMails(soup):
            for name in soup.find_all('a'):
                    if(name is not None):
                        emailText=name.text
                        match=bool(re.match('''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',emailText))
                        if('@' in emailText and match==True):
                            emailText=emailText.replace(" ",'').replace('\r','')
                            emailText=emailText.replace('\n','').replace('\t','')
                            if(len(mails)==0)or(emailText not in mails):
                                print(emailText)
                            mails.append(emailText)
        for link in allLinks:
            if(link.startswith("http") or link.startswith("www") or link.startswith("https")):
                r=requests.get(link)
                data=r.text
                soup=BeautifulSoup(data,'html.parser')
                findMails(soup)

            else:
                newurl=url+link
                r=requests.get(newurl)
                data=r.text
                soup=BeautifulSoup(data,'html.parser')
                findMails(soup)
        global emails
        emails = set(mails)
        total = len(mails)
        print(mails)
        if(len(mails)==0):
            print("No Mails Found")
        
        context = {
            'emails':mails,
            'total': total,
        }
        return render(request, 'emailExtractor.html', context)
    return render(request, 'emailExtractor.html')

def sendmail(request):
    try:
        email = emails
    except:
        messages.error(request,"Failed to get Emails!")
    if request.method == "POST":
        subject = request.POST.get('mail_subject')
        message = request.POST.get('message')
        from_mail = request.POST.get('from_mail')

        #getting emails from the uploadfiles function using global variable
        try:
            send_mail(subject, message,from_mail,email,fail_silently=False)
            messages.success(request, 'Email sent successfull.')
        except:
            messages.error(request, 'Failed to send Mail.')
    return render(request, 'sendMassmail.html')

def About(request):
    return render(request, 'About.html')