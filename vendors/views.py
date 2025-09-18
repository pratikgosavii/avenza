from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from location.models import Location
from .serializers import VendorSerializer,VendorSerializerData
from .models import Vendor
from admins.models import User
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from orders.models import Order
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# from django.contrib.auth.mixins import RoleBasedLoginRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from packages.models import Package, PackageLocationPrice
from category.models import Category
from packages.models import Package

from .decorators import *


@vendor_or_admin_login_required
class VendorDashboardView(View):
    def get(self, request):

        return render(request, "vendorDashboard.html")
       


from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

class VendorLoginView(View):

    def get(self, request):
        # Redirect to vendor dashboard if the user is already authenticated and is a vendor
        if request.user.is_authenticated and hasattr(request.user, 'vendor'):
            return redirect("vendorDashboard")
        return render(request, "vendorLogin.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate user
        print("Attempting to authenticate:", username)
        user = authenticate(request, username=username, password=password)

        if user:
            print("User found:", user)

            # Check if the user has a vendor profile
            if hasattr(user, 'vendor'):
                print("User is a vendor with role:", user.vendor.is_approved)

                # Check if the vendor is approved
                if user.vendor.is_approved:
                    login(request, user)
                    request.session['vendor_id'] = user.vendor.id
                    print(request.user)
                    return redirect("vendorDashboard")
                else:
                    messages.error(request, "Vendor is not approved by the admin.")
                    print("Vendor is not approved.")
                    return render(request, "vendorLogin.html")

            # If the user is not a vendor
            messages.error(request, "Unauthorized vendor role.")
            print("User is not a vendor. Role:", user.role)
            return render(request, "vendorLogin.html")

        # If no user is found
        messages.error(request, "Invalid username or password.")
        print("No user found, invalid credentials.")
        return render(request, "vendorLogin.html")




class VendorLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if 'user_role' in request.session and request.session['user_role'] == 'vendor':
            del request.session['user_role']  # Remove session role for vendor
        return super().dispatch(request, *args, **kwargs)



from rest_framework.permissions import AllowAny

class VendorRegisterView(APIView):

    permission_classes = [AllowAny]  # This allows unauthenticated access to this view

    def get(self, request):
        locations = Location.objects.all()
        categories = Category.objects.all()
        return render(request, "vendorRegister.html", {
            "locations": locations,
            "Categories": categories,
        })

    def post(self, request):
        print(request.data)
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            # Notify admins
            admins = User.objects.filter(role=User.ADMIN)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    vendor=vendor,
                    message=f"Vendor {vendor.vendorname} has registered. Please approve or reject.",
                )

            messages.success(request, "Vendor registered successfully! Awaiting admin approval.")
            return render(request, "vendorLogin.html")

        # Collect errors from serializer and pass them to the template
        error_messages = {field: " ".join(errors) for field, errors in serializer.errors.items()}
        messages.error(request, "There were errors in your registration. Please check the form.")
        return render(request, "vendorRegister.html", {
            'errors': error_messages,  # Pass errors to the template
            "locations": Location.objects.all(),
            "Categories": Category.objects.all(),
        })



@admin_login_required
class AdminVendorRegisterView(APIView):

    def get(self, request):
        locations = Location.objects.all()
        return render(request, "adminVendorRegister.html", {"locations": locations})

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            # Create the vendor
            vendor = serializer.save()

            # Notify admins
            admins = User.objects.filter(role=User.ADMIN)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    vendor=vendor,
                    message=f"Vendor {vendor.business_name} has registered. Please approve or reject.",
                )

            # Success message
            messages.success(request, "Vendor registered successfully! Awaiting admin approval.")
            return render(request, "adminVendorRegister.html")

        # Error message
        error_messages = {field: " ".join(errors) for field, errors in serializer.errors.items()}
        messages.error(request, error_messages)
        return render(request, "adminVendorRegister.html", {'errors': serializer.errors})



class VendorListView(APIView):
    def get(self, request):
        vendors = Vendor.objects.select_related('user', 'location').prefetch_related('category').filter(is_approved=1)  # Optimize query
        serializer = VendorSerializerData(vendors, many=True)  
        print(serializer.data)

        # Pass serialized data to the template
        return render(request, 'vendorsList.html', {'vendors': serializer.data})




@vendor_or_admin_login_required
class VendorRequestView(APIView):
    def get(self, request):
        vendors = Vendor.objects.select_related('user', 'location').filter(is_pending=1)  # Optimize query
        return render(request, 'vendorRequest.html', {'vendors': vendors})
    

@vendor_or_admin_login_required
class VendorProfileView(APIView):
    def get(self, request, vendor_id=None):
        # Fetch vendor details
        vendors = Vendor.objects.select_related('user', 'location').prefetch_related('category').filter(id=vendor_id)
        # if not vendors.exists():
        #     return HttpResponse("Vendor not found.", status=404)

        vendor = vendors.first()
        vendor_serializer = VendorSerializerData(vendor)
        
        # Fetch orders associated with the vendor
        orders = Order.objects.filter(vendor=vendor).select_related('packageId', 'locationId')
        orders_data = [
            {
                "id": order.id,
                "package_name": order.packageId.title,
                "category": ", ".join([cat.title for cat in order.packageId.categories.all()]),
                "date": order.date,
                "location": order.locationId.title,
                "status": "Completed" if order.updated_at.date() <= order.date else "Pending",
                "total_amount": order.total_amount,
                "rating": 4.5,  # Assuming a placeholder rating
            }
            for order in orders
        ]

        # Pass vendor and order data to the template
        return render(request, 'vendorProfile.html', {
            'vendor': vendor_serializer.data,
            'orders': orders_data,
            
        })





class VendorDetailView(APIView):

    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)


@admin_login_required
class VendorUpdateView(APIView):

    def put(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Vendor updated successfully!",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@admin_login_required
class VendorDeleteView(APIView):

    def delete(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        vendor.user.delete()  # Delete associated User object
        vendor.delete()
        return Response({"message": "Vendor deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


@admin_login_required
class VendorApprovalView(APIView):
    """
    Handle vendor approval or rejection with feedback for the admin dashboard.
    """

    def post(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)

        # Ensure the 'action' is present in the request
        action = request.data.get("action", "").strip().lower()
        if not action:
            messages.error(request, "Action parameter is required.")
            return redirect('vendorList')  # Replace with the actual name of your URL for vendor list

        # Approve action
        if action == "approve":
            if vendor.is_pending:
                vendor.is_approved = True
                vendor.is_pending = False
                vendor.save()

                # Send notification email for approval
                # try:
                #     send_mail(
                #         "Vendor Registration Approved",
                #         f"Congratulations {vendor.business_name}, your registration has been approved.",
                #         settings.DEFAULT_FROM_EMAIL,
                #         [vendor.user.email],
                #     )
                #     messages.success(request, f"Vendor '{vendor.business_name}' approved successfully!")
                # except Exception as e:
                #     messages.warning(
                #         request,
                #         f"Vendor '{vendor.business_name}' approved, but email notification failed: {str(e)}"
                #     )
                return redirect('vendorList')

            messages.warning(request, f"Vendor '{vendor.business_name}' is already approved.")
            return redirect('vendorList')

        # Reject action
        elif action == "reject":
            if vendor.is_pending:
                vendor.user.delete()
                vendor.delete()
                # try:
                #     # Delete the vendor and associated user
                #     vendor.user.delete()
                #     vendor.delete()
                #
                #     # Send notification email for rejection
                #     send_mail(
                #         "Vendor Registration Rejected",
                #         f"Sorry {vendor.business_name}, your registration has been rejected.",
                #         settings.DEFAULT_FROM_EMAIL,
                #         [vendor.user.email],
                #     )
                #     messages.success(request, f"Vendor '{vendor.business_name}' rejected successfully!")
                # except Exception as e:
                #     messages.warning(
                #         request,
                #         f"Vendor '{vendor.business_name}' rejected, but email notification failed: {str(e)}"
                #     )
                return redirect('vendorList')

            messages.warning(request, f"Vendor '{vendor.business_name}' is already approved or rejected.")
            return redirect('vendorList')

        # Invalid action case
        else:
            messages.error(request, f"Invalid action '{action}'. Use 'approve' or 'reject'.")
            return redirect('vendor_list')





from customers.models import Ticket

@vendor_or_admin_login_required
class VendorTicket(APIView):
    def get(self, request):
        # Filter tickets with specified statuses
        allowed_statuses = ["open", "in_progress", "resolved", "closed"]
        tickets = Ticket.objects.filter(status__in=allowed_statuses)  # Fetch only tickets with these statuses

        # Count tickets by status
        total_tickets = tickets.count()
        approved_tickets = tickets.filter(status='approved').count()  # Adjust if 'approved' isn't needed
        pending_tickets = tickets.filter(status='in_progress').count()
        not_approved_tickets = tickets.filter(status='not_approved').count()  # Adjust if 'not_approved' isn't needed

        # Prepare ticket data to send to the template
        ticket_data = []
        for ticket in tickets:
            ticket_data.append({
                'id': ticket.id,
                'order_id': ticket.order.id,
                'customer': ticket.customer.user.username,
                'vendor': ticket.vendor.username,
                'issue_description': ticket.issue_description,
                'status': ticket.get_status_display(),
                'created_at': ticket.created_at,
            })

        # Pass the dynamic data to the template
        return render(request, "vendor_ticket.html", {
            "data": ticket_data,
            "total_tickets": total_tickets,
            "approved_tickets": approved_tickets,
            "pending_tickets": pending_tickets,
            "not_approved_tickets": not_approved_tickets
        })

    def post(self, request):
        action = request.POST.get('action')  # Action: approve, deny, delete, or update status
        ticket_ids = request.POST.getlist('ticket_ids')  # Selected ticket IDs
        new_status = request.POST.get('new_status')  # Get the new status to apply

        if not ticket_ids:
            return Response({'error': 'No tickets selected'}, status=400)

        # Fetch the tickets that need to be updated
        tickets = Ticket.objects.filter(id__in=ticket_ids)

        if action == 'approve':
            tickets.update(status='approved')
        elif action == 'deny':
            tickets.update(status='not_approved')
        elif action == 'delete':
            tickets.delete()
            return Response({'message': f'{len(ticket_ids)} tickets deleted successfully'}, status=200)
        elif action == 'update_status' and new_status:
            tickets.update(status=new_status)
        else:
            return Response({'error': 'Invalid action'}, status=400)

        return redirect('VendorTicket')
        # return Response({'message': f'{len(ticket_ids)} tickets updated successfully'}, status=200)


@vendor_or_admin_login_required
class VendorTicketFilter(APIView):
    def get(self, request):
        tag = request.GET.get('tag', 'all')  # Default to 'all' if no tag is passed

        # Filter tickets based on the 'tag' parameter
        if tag == 'in_progress':
            tickets = Ticket.objects.filter(status='in_progress')
        elif tag == 'approved':
            tickets = Ticket.objects.filter(status='approved')
        elif tag == 'closed':
            tickets = Ticket.objects.filter(status='closed')
        else:
            tickets = Ticket.objects.all()  # Default to all tickets if tag is 'all' or invalid
        
        # Prepare ticket data to send in response
        ticket_data = []
        for ticket in tickets:
            ticket_data.append({
                'id': ticket.id,
                'order_id': ticket.order.id,
                'customer': ticket.customer.user.username,
                'vendor': ticket.vendor.username,
                'issue_description': ticket.issue_description,
                'status': ticket.get_status_display(),  # Get the display value of status
                'created_at': ticket.created_at,
            })
        
        # Return the filtered ticket data in the response
        return Response({'data': ticket_data}, status=200)



from .models import *
from django.contrib.auth.decorators import login_required

@vendor_or_admin_login_required
def vendor_calendar(request):
    if request.method == 'POST':

        selected_dates = request.POST.getlist('available_dates')

       

        
        # Clear existing dates for the vendor
        VendorAvailability.objects.filter(vendor=request.user).delete()
        
        # Save each selected date
        for date in selected_dates:
            VendorAvailability.objects.create(vendor=request.user, date=date)
    
        return JsonResponse({'message': 'Dates saved successfully'})

    available_dates = VendorAvailability.objects.filter(vendor=request.user).values_list('date', flat=True)
    

    print('------------------------')
    print(request.user)
    print('------------------------')


    # Convert available_dates to a list and ensure it's in the correct format
    available_dates_list = list(available_dates)
    formatted_dates = [date.strftime('%Y-%m-%d') for date in available_dates_list] if available_dates_list else []

    print(available_dates_list)  # This will print an empty list if no dates are available
    return render(request, 'vendor_calendar.html', {'available_dates': formatted_dates})

from rest_framework.permissions import AllowAny

@vendor_or_admin_login_required
class VendorOders(APIView):
    def get(self, request):
        # Get the vendor_id from session
        vendor_id = request.session['vendor_id']
        user_id = Vendor.objects.get(id=vendor_id)
        try:
            vendor_name = user_id.vendorname  # Fetch the vendor using the vendor_id
        except:
            vendor_name = ""
        if vendor_id:
            # Get all orders associated with the current vendor
            orders = Order.objects.filter(vendor_id=user_id)
            # print(orders)
        else:
            orders = Order.objects.none()  # Return an empty queryset if no vendor_id in session

        # You can also get the count of orders placed by this vendor
        total_orders = orders.count()

        # Pass orders and total_orders to the template
        return render(request, "vendorOrders.html", {
            'orders': orders,
            'total_orders': total_orders,
            "vendor_name":vendor_name,
            "ses":request.session['vendor_id']
        })
    
    permission_classes = [AllowAny]  # This allows unauthenticated access to this view
    authentication_classes = []  # This disables any authentication for this view

    def post(self, request):
        """
        Handle the update of the order status (e.g., accepted or rejected)
        """

        print(request.data)
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')

        # Validate the order_id and new_status
        if not order_id or new_status not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        print('-------------2-------------------')

        # Retrieve the order object
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        print('-------------3-------------------')

        print(order.vendor_id)
        print(request.session.get('vendor_id'))
        # Check if the current user is the vendor for this order
        if order.vendor_id != request.session.get('vendor_id'):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        print('-------------5-------------------')

        # Update the order status
        order.status = new_status
        order.save()

        print('-------------4-------------------')

        # Return a response with updated order data
        return JsonResponse({
            'order_id': order.id,
            'status': order.status,
            'message': 'Order status updated successfully'
        })
    

from .serializers import *


@vendor_or_admin_login_required
class VendorOrderCompleted(APIView):

    def get(self, request, pk):
        order_instance = Order.objects.get(id=pk)
        return render(request, "order_completed.html", {'order_instance': order_instance})

    def post(self, request, pk):
        
        order_instance = get_object_or_404(Order, id=pk)
        
        images = request.FILES.getlist('completion_images')
        
        if not images:
            messages.error(request, f"No images uploaded.")
            return redirect('VendorOders')

        # Create multiple VendorOrderCompleted instances for each image
        for image in images:
            OrderCompletionImage.objects.create(
                vendor=order_instance.vendor,
                completion_images=image
            )

        order_instance.status = 'completed'
        order_instance.save()


        messages.success(request, f"Order marked as completed")
        return redirect('VendorOders')
    
            
       

@vendor_or_admin_login_required    
class VendorPayments(APIView):

    def get(self, request):
        # data = Vendor.objects.all()
        return render(request, "vendorPayments.html")
    
# from .serializers import PackageSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import render
# from .serializers import PackageSerializer

# class CreateServices(APIView):
#     def get(self, request):
#         return render(request, "vendorServices.html")

#     def post(self, request):
#         """
#         Create a new Package and its associated PackageLocationPrice
#         """
#         serializer = PackageSerializer(data=request.data)

#         try:
#             if serializer.is_valid():
#                 package = serializer.save()  # This will also save associated PackageLocationPrice objects
                
#                 # Return a success response with the created package data
#                 return render(request, "vendorServices.html", {'package': package})
#             else:
#                 # If the serializer is not valid, return errors
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             # Print the error message for debugging purposes
#             print(f"Error occurred: {str(e)}")
#             # Return a generic error response
#             return Response({"error": "An error occurred while creating the package."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
# class ServicesList(APIView):
#     def get(self, request):
#         # Fetch data from the database (e.g., all the packages) and pass it to the template
#         services = Package.objects.all()  # Retrieve all packages

#         # Render the 'vendorListServices.html' template with the services data
#         return render(request, "vendorListServices.html", {"services": services})


@vendor_or_admin_login_required
class VendorDetails(APIView):
    
    def get(self, request):
        try:
            vendor_id = request.session['vendor_id']
        except KeyError:
            return redirect('/api/vendors/login/')
        
        # Fetch the vendor associated with the logged-in user
        vendor = get_object_or_404(Vendor, id=vendor_id)

        categories = Category.objects.all()

        # Render the 'vendorDetails.html' template with the vendor data
        return render(request, "vendorDetails.html", {"vendor": vendor, "Categories": categories})
    
    def post(self, request):
        vendor_id = request.session['vendor_id']

        print(request.POST)
        
        # Fetch the vendor associated with the logged-in user using vendor_id from session
        vendor = get_object_or_404(Vendor, id=vendor_id)

        try:
            # Update vendorname
            vendorname = request.POST.get("vendorname", None)
            if vendorname:
                vendor.vendorname = vendorname

            # Update vendorPhoneNumber
            vendorPhoneNumber = request.POST.get("vendorPhoneNumber", None)
            if vendorPhoneNumber:
                if len(vendorPhoneNumber) != 10 or not vendorPhoneNumber.isdigit():
                    return Response({"error": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)
                vendor.vendorPhoneNumber = vendorPhoneNumber

            # Update portfolio link
            portfolio_link = request.POST.get("portfolio_link", None)
            if portfolio_link:
                vendor.portfolio_link = portfolio_link

            # Handle image upload
            if 'image' in request.FILES:
                vendor.image = request.FILES['image']

            # Save the vendor instance
            vendor.save()

            return render(request, "vendorDetails.html", {"vendor": vendor, "success": "Profile updated successfully!"})

        except Exception as e:
            return render(request, "vendorDetails.html", {"vendor": vendor, "error": f"An error occurred: {str(e)}"})

# from .models import Review
# from .serializers import ReviewSerializer

@vendor_or_admin_login_required
class VendorFeedbacks(APIView):

    def get(self, request):
        # user_id = request.session.get('vendor_id')
        
        # if user_id is None:
        #     return render(request, "vendorfeedback.html", {"review": []})  # or redirect to login

        # reviews = Review.objects.filter(user=user_id)

        # serializer = ReviewSerializer(reviews, many=True)  # Pass queryset and set many=True
        
        # Render template with serialized data
        static_reviews = [
            {
                "id": 1,
                "package": "Package A",
                "user": "Vendor 1",
                "rating": 5,
                "comment": "Excellent service!",
                "created_at": "2024-12-01T10:00:00Z"
            },
            {
                "id": 2,
                "package": "Package B",
                "user": "Vendor 2",
                "rating": 4,
                "comment": "Very good experience.",
                "created_at": "2024-12-02T11:30:00Z"
            },
            {
                "id": 3,
                "package": "Package C",
                "user": "Vendor 3",
                "rating": 3,
                "comment": "Average service.",
                "created_at": "2024-12-03T14:15:00Z"
            }
        ]

        return render(request, "vendorfeedback.html", {"review": static_reviews})

    def post(self, request):
        order = request.get('order')
        get_user = Order.objects.filter(id=order)
        # serializer = ReviewSerializer(data=request.data)

        # if serializer.is_valid():
        #     serializer.save()  # Set the user field before saving
        return Response("serializer.data", status=status.HTTP_201_CREATED)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@vendor_or_admin_login_required
class UpdateVendorAvailability(APIView):
    """
    A class-based view to handle vendor availability update.
    """

    def post(self, request, *args, **kwargs):
        try:
            print(request.user)
            vendor = Vendor.objects.get(user = request.user)  # You can adjust this to update a specific vendor.
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        available = request.data.get('available')

        if available is None:
            return Response({"error": "Availability status is required"}, status=status.HTTP_400_BAD_REQUEST)

        vendor.is_available = available
        vendor.save()

        return Response({"message": "Vendor availability updated successfully", "vendor": VendorSerializer(vendor).data}, status=status.HTTP_200_OK)