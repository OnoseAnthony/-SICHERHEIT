from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from manager.models import User, Passwords
from manager.forms import RegisterForm
from manager.password_generator import generate_secure_password
from manager.qr_generator import generate_qrcode





# Create your views here.


@method_decorator([login_required,], name='dispatch')
class IndexListView(ListView):
    model = Passwords
    ordering = ('user', )
    context_object_name = 'user_profile'
    template_name = 'manager/dashboard.html'

    def get_context_data(self, **kwargs):
        return super(IndexListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        queryset = self.request.user.user_profile.all()
        return queryset


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'manager/register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('manager:index')


    def form_invalid(self, form):
        messages.error(self.request, 'Please check form fields.', extra_tags = 'esignup')
        return redirect('manager:register')


def user_login(request):
    context = {}
    if request.method == 'POST' and check_user(request.POST['login_passphrase']):
        user_obj = User.objects.get(login_passphrase = request.POST['login_passphrase'])
        username = user_obj.username
        cleaned_password = request.POST['password']
        user = authenticate(request, username=username, password=cleaned_password)
        if user:
            # correct username and password login the user
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            context['error'] = "Provide Valid Credentials !!"
            return render(request, 'manager/login.html', context)

    else:
        return render(request, 'manager/login.html', context)



def check_user(passphrase):
    if(User.objects.filter(login_passphrase = passphrase).first()):
        return True
    else:
        return False


@login_required
def user_logout(request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


@method_decorator([login_required,], name='dispatch')
class PasswordsListView(ListView):
    model = Passwords
    ordering = ('application_service_name', )
    context_object_name = 'user_profile'
    template_name = 'manager/password_list.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = self.request.user.user_profile.all()
        return queryset


@method_decorator([login_required,], name='dispatch')
class PasswordCreateView(CreateView):
    model = Passwords
    fields = ('application_service_name', 'application_service_url', 'registered_username', 'registered_email_address',)
    template_name = 'manager/create_password.html'

    def form_valid(self, form):
        passwords = form.save(commit=False)
        passwords.user = self.request.user
        passwords.password = generate_secure_password(form.cleaned_data["application_service_name"], 18)
        qrcode_image = generate_qrcode(passwords.password)
        canvas = Image.new('RGB', (200, 200), 'white')
        draw = ImageDraw.Draw(canvas)
        position = (left, top)
        canvas.paste(qrcode_image, position)
        blob = BytesIO()
        canvas.save(blob, 'JPEG')
        passwords.qrcode_image.save('qrcode-{}-{}.jpg'.format(form.cleaned_data["application_service_name"], passwords.password[:4]), File(blob), save=False)
        passwords.save()
        messages.success(self.request, 'Password created successfully', extra_tags= 'addmemsuccess')
        return redirect('manager:password_change', passwords.pk)

    def form_invalid(self, form):
        messages.error(self.request, 'Please check form fields.', extra_tags = 'esignup')
        return redirect('manager:password_add')


@method_decorator([login_required,], name='dispatch')
class PasswordUpdateView(UpdateView):
    model = Passwords
    fields = ('application_service_name', 'application_service_url', 'registered_username', 'registered_email_address',)
    context_object_name = 'passwords'
    template_name = 'manager/change_password.html'



    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing passwords that belongs
        to the logged in user.
        '''
        return self.request.user.user_profile.all()

    def get_success_url(self):
        return reverse('manager:password_change_list')


@method_decorator([login_required,], name='dispatch')
class PasswordDeleteView(DeleteView):
    model = Passwords
    context_object_name = 'password'
    template_name = 'manager/delete_password.html'
    success_url = reverse_lazy('manager:password_change_list')

    def delete(self, request, *args, **kwargs):
        password = self.get_object()
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.user_profile.all()
