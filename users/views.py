from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterModelForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views import View


def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)  # Email orqali autentifikatsiya

            if user is not None:
                login(request, user)
                return redirect('shop:index')
            else:
                messages.error(request, "Email yoki parol noto‘g‘ri!")

    return render(request, 'users/login.html', {'form': form})


def register_page(request):
    form = RegisterModelForm()
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            try:
                send_mail(
                    'Xush kelibsiz!',
                    'Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!',
                    'solihapahridinova@gmail.com',
                    [user.email],
                    fail_silently=True
                )
            except Exception as e:
                print("Email jo‘natishda xatolik:", e)

            authenticated_user = authenticate(request, email=user.email, password=form.cleaned_data['password'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('shop:index')
            else:
                messages.error(request, "Autentifikatsiya muvaffaqiyatsiz yakunlandi!")

    return render(request, 'users/register.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('shop:index')


class RegisterPage(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = RegisterModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            self.send_welcome_email(user)  # Email yuborish

            authenticated_user = authenticate(request, email=user.email, password=form.cleaned_data['password'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('shop:index')
            else:
                messages.error(request, "Autentifikatsiya muvaffaqiyatsiz yakunlandi!")
                return redirect('users:register')

        return render(request, self.template_name, {'form': form})

    def send_welcome_email(self, user):
        subject = "Xush kelibsiz!"
        html_message = render_to_string('users/email_welcome.html', {'user': user})
        plain_message = strip_tags(html_message)
        from_email = 'solihapahridinova@gmail.com'
        recipient_list = [user.email]

        email = EmailMultiAlternatives(subject, plain_message, from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")
        email.send()
