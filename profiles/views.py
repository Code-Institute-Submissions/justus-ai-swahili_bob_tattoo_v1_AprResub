from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.http import JsonResponse
import re
from .models import SubscribedUsers
from django.core.mail import send_mail
from django.conf import settings
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    def index(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email
        subscribedUsers.name = name
        subscribedUsers.save()
        # send a confirmation mail
        subject = 'NewsLetter Subscription'
        message = 'Hello ' + name + ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
        return res
    return render(request, 'index.html')

def validate_email(request): 
    email = request.POST.get("email", None)   
    if email is None:
        res = JsonResponse({'msg': 'Email is required.'})
    elif SubscribedUsers.objects.get(email = email):
        res = JsonResponse({'msg': 'Email Address already exists'})
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Invalid Email Address'})
    else:
        res = JsonResponse({'msg': ''})
    return res

    return render(request, template, context)