from .serializers import UserSerializer
from .models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
# from django.contrib.auth.mixins import RoleBasedLoginRequiredMixin
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth.views import LogoutView
from datetime import datetime, timedelta
from orders.models import Order

class AdminDashboardView(View):
    def get(self, request):
        # Get today's date
        today = datetime.today().date()

        # Calculate the start of this week (Monday)
        start_of_week = today - timedelta(days=today.weekday())

        # Get orders for the current week (from Monday to today)
        current_week_orders = Order.objects.filter(date__gte=start_of_week)

        # Get orders for the previous week (same days as this week, but last week)
        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_week - timedelta(days=1)
        last_week_orders = Order.objects.filter(date__gte=start_of_last_week, date__lte=end_of_last_week)

        # Calculate the total orders for the current and last week
        current_week_order_count = current_week_orders.count()
        last_week_order_count = last_week_orders.count()

        # Calculate the percentage change since last week (if last week's count is not zero)
        if last_week_order_count > 0:
            percentage_change = ((current_week_order_count - last_week_order_count) / last_week_order_count) * 100
        else:
            percentage_change = 0  # Avoid division by zero

        # Prepare context to pass to template
        context = {
            'current_week_order_count': current_week_order_count,
            'percentage_change': round(percentage_change, 2),
        }

        # Render the template with the context
        return render(request, "adminDashboard.html", context)

        # return redirect('adminLogin')  # Redirect if not authenticated or incorrect role


class AdminLoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.role == "admin":
            return redirect("adminDashboard")
        return render(request, "adminLogin.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user:
            # Redirect based on role
            if user.role == "admin":
                login(request, user)
                return redirect("adminDashboard")
            messages.error(request, "Unauthorized user role.")
            return render(request, "adminLogin.html")
        messages.error(request, "Invalid username or password.")
        return render(request, "adminLogin.html")


class AdminLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if 'user_role' in request.session and request.session['user_role'] == 'admin':
            del request.session['user_role']  # Remove session role for admin
        return super().dispatch(request, *args, **kwargs)


from django.http import JsonResponse


class GetAvenza(View):  # Changed to inherit from View
    def get(self, request):
        data = why_avenza.objects.all().first()
        if data is None:
            return JsonResponse({"error": "No data found"}, status=404)
        
        response_data = {
            "id": data.id,
            "description": data.description,
        }
        return JsonResponse({"data": response_data}, status=200)

from .models import *

def why_avenza_add(request):
    
    if request.method == "POST":

        why_avenza_data = request.POST.get('description')

        print(why_avenza_data)

        instance = why_avenza.objects.get(id = 1)
        instance.description = why_avenza_data
        instance.save()

        return render(request, 'why_avenza.html', {"data" : instance})
    
    else:

        # create first row using admin then editing only

        data = why_avenza.objects.get(id = 1)
        print(data)

        return render(request, 'why_avenza.html', {"data" : data})



class Gettestimonials(View):
    def get(self, request):
        data = testimonials.objects.all()  # Assuming Testimonials is the model name

        if not data.exists():
            return JsonResponse({"error": "No data found"}, status=404)

        response_data = []
        for testimonial in data:
            temp = {
                "id": testimonial.id,
                "name": testimonial.name,
                "description": testimonial.description,
            }
            response_data.append(temp)

        return JsonResponse({"data": response_data}, status=200)

from .models import *

def add_testimonials(request):
    
    if request.method == "POST":

        description = request.POST.get('description')
        name = request.POST.get('name')

        print(description)
        print(name)

        instance = testimonials.objects.create(description = description, name = name)
        instance.save()

        return redirect('list_testimonials')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html')

def update_testimonials(request, testimonials_id):
    
    instance = testimonials.objects.get(id = testimonials_id)

    if request.method == "POST":

        description = request.POST.get('description')
        name = request.POST.get('name')

        print(description)
        print(name)

        instance.description = description
        instance.name = name
        instance.save()

        return redirect('list_testimonials')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_testimonials.html', {'data' : instance})


def list_testimonials(request):

    data = testimonials.objects.all()

    return render(request, 'list_testimonials.html', {'data' : data})


def delete_testimonials(request, testimonials_id):

    data = testimonials.objects.get(id = testimonials_id).delete()

    return redirect('list_testimonials')





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class Getcancelation_policy(View):  # Changed to inherit from View


    @method_decorator(csrf_exempt)
    def post(self, request):
        data = cancelation_policy.objects.all()  # Assuming Testimonials is the model name

        if not data.exists():
            return JsonResponse({"error": "No data found"}, status=404)

        response_data = []
        for i in data:
            temp = {
                "id": i.id,
                "description": i.description,
            }
            response_data.append(temp)

        return JsonResponse({"data": response_data}, status=200)

from .models import *

def add_cancelation_policy(request):
    
    if request.method == "POST":

        description = request.POST.get('description')

        print(description)

        instance = cancelation_policy.objects.create(description = description)
        instance.save()

        return redirect('list_cancelation_policy')
    
    else:

        return render(request, 'add_cancelation_policy.html')


def update_cancelation_policy(request, cancelation_policy_id):

    instance = cancelation_policy.objects.get(id = cancelation_policy_id)
    
    if request.method == "POST":

        description = request.POST.get('description')

        print(description)

       
        instance.description = description
        instance.save()


        return redirect('list_cancelation_policy')
    
    else:

        return render(request, 'add_cancelation_policy.html', {"data" : instance})




def list_cancelation_policy(request):

    data = cancelation_policy.objects.all()

    return render(request, 'list_cancelation_policy.html', {'data' : data})



def delete_cancelation_policy(request, cancelation_policy_id):

    data = cancelation_policy.objects.get(id = cancelation_policy_id).delete()

    return redirect('list_cancelation_policy')



# create admin and get all the admins
class AdminListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role="admin").all()
    serializer_class = UserSerializer


# update, delete and retrieve admin
class AdminRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




from customers.models import *

def delete_customer(request, customer_id):

    customer_insance = Customer.objects.get(id = customer_id)





def update_customer(request, customer_id):

    customer_insance = Customer.objects.get(id = customer_id)

    return render(request, '')



