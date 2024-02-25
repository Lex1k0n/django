from django.shortcuts import render, redirect
from .forms import MailForm
from .models import Mail, Blueprint
from django.core.mail import send_mail
import smtplib


def index(request):
    bps = Blueprint.objects.all()
    names = []
    dict_bp = {}
    txt_fill = ''
    for sample in bps:
        names.append(sample.name)
        dict_bp[sample.name] = sample.text
    mails = Mail.objects.all()
    mail_lst = []
    for mail in mails:
        mail_lst.append(mail.email)
    if request.method == 'POST' and 'change' in request.POST:
        current = Blueprint.objects.get(name=request.POST.get('change_bp'))
        txt_fill = dict_bp[str(current)]
    elif request.method == 'POST' and 'spam' in request.POST:
        for mail in mail_lst:
            try:
                send_mail(
                    'name here',
                    request.POST.get('mail_text'),
                    'your address here',
                    [mail]
                )
            except smtplib.SMTPDataError:
                txt_fill = 'Oops, it seems that your address doesnt have permissions to send email through smtp ' \
                           'provider! Try to check that you can do this with IT support.'
    return render(request, 'main/index.html', {'names': names, 'fill': txt_fill})


def add(request):
    err = ''
    mails = Mail.objects.all()
    mail_lst = []
    for mail in mails:
        mail_lst.append(mail.email)
    if request.method == 'POST':
        if 'addbtn' in request.POST:
            form = MailForm(request.POST)
            if form.is_valid():
                current = form.cleaned_data.get('email')
                for mail in mails:
                    if mail.email == current:
                        err = 'This email is already added!'
                        return render(request, 'main/add.html', {'form': form, 'error': err, 'mails': mail_lst})
                form.save()
                return redirect('add_mail')
            else:
                err = 'Incorrect input!'
        elif 'dltbtn' in request.POST:
            Mail.objects.get(email=request.POST.get('delete_mail')).delete()
            return redirect('add_mail')
    form = MailForm()
    return render(request, 'main/add.html', {'form': form, 'error': err, 'mails': mail_lst})


def bp(request):
    err = ''
    bps = Blueprint.objects.all()
    names = []
    for sample in bps:
        names.append(sample.name)
    if request.method == 'POST':
        if request.POST.get('bptxt') == '':
            err = 'BP text cannot be empty!'
        elif request.POST.get('bpname') == '':
            err = 'BP name cannot be empty!'
        elif request.POST.get('bpname') in names:
            err = 'This name already exists.'
        else:
            Blueprint.create(request.POST.get('bpname'), request.POST.get('bptxt')).save()

    return render(request, 'main/bp.html', {'error': err})
