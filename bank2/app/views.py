from django.shortcuts import render,redirect,HttpResponse
from .models import BankAccount
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Max
from django.contrib import messages 


def home(request):
    return render(request,'home.html')

def account_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        photo = request.FILES.get('photo')  # Get the uploaded file
        max_account_no = BankAccount.objects.aggregate(Max('account_no'))['account_no__max']
        
        if max_account_no is None:
            # If no accounts exist, start with a default value (e.g., 100000000000)
            account_no = 100000000000
        else:
            account_no = max_account_no + 1 
        # Create a new bank account instance
        BankAccount.objects.create(
            name=name,
            phone=phone,
            email=email,
            account_no=account_no,
            photo=photo  # Save the uploaded photo

        )
        try:
            send_mail(
                subject="Account Created Successfully",
                message=f"Dear {name},\n\nYour account has been created successfully! Your account number is {account_no}.\n\nThank you for choosing Dochay Bank!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],  # Use the email provided by the user
                fail_silently=False,
            )
            return redirect('home') 
        except Exception as e:
            return HttpResponse(f"Error sending email: {str(e)}")
    return render(request,'account_create.html')

def pin_generation(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        pin = request.POST['pin']
        confirm_pin = request.POST['confirm_pin']

        # Validate PIN
        if pin != confirm_pin:
            return render(request, 'pin_generation.html', {'error': 'PINs do not match.'})

        # Find or create bank account entry
        account, created = BankAccount.objects.get_or_create(name=name, phone=phone)

        # Update or set the PIN
        account.pin = pin
        account.save()

        # Send email notification
        send_mail(
            'Your PIN has been generated',
            f'Hello {name},\n\nYour PIN is: {pin}\n\nPlease keep it safe!',
            'from@example.com',  # Replace with your sender email
            [account.email],  # Ensure the email field is populated in your model
            fail_silently=False,
        ) 
        messages.success(request, 'Your PIN has been generated successfully!')
        # return redirect()

    return render(request,'pin_generation.html')

def deposite(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pin = request.POST.get('pin')
        amount = request.POST.get('amount')

        try:
            # Retrieve the bank account based on name, phone, and pin
            account = BankAccount.objects.get(name=name, phone=phone, pin=pin)

            if account.balance is None:
                account.balance = 0  # Initialize balance if it's None

            # Ensure amount is an integer before adding it to balance
            amount_int = int(amount)
            account.balance += amount_int  
            account.save()

            # Send an email notification
            send_mail(
                'Deposit Confirmation',
                f'Dear {name},\n\nYour account has been credited with {amount}. Your new balance is {account.balance}.',
                'from@example.com',  # Replace with your email address
                [account.email],
                fail_silently=False,
            )

            messages.success(request, 'Deposit successful! A confirmation email has been sent.')
            return redirect('deposite')  # Redirect to the deposit page or any other page

        except BankAccount.DoesNotExist:
            messages.error(request, 'Account not found. Please check your details.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        print(f"Name: {name}, Phone: {phone}, Pin: {pin}, Amount: {amount}")
    return render(request,'deposite_money.html')

def withdraw(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pin = request.POST.get('pin')
        amount = float(request.POST.get('amount'))

        try:
            # Assuming you have a way to identify the account, e.g., by phone or name
            account = BankAccount.objects.get(phone=phone, pin=pin)

            if account.balance >= amount:
                account.balance -= amount
                account.save()
                send_mail(
                'Deposit Confirmation',
                f'Dear {name},\n\nYour account has been debited with {amount}. Your new balance is {account.balance}.',
                'from@example.com',  # Replace with your email address
                [account.email],
                fail_silently=False,
            )
                messages.success(request, f'Withdrawal of {amount} successful! Your new balance is {account.balance}.')
            else:
                messages.error(request, 'Insufficient funds.')

        except BankAccount.DoesNotExist:
            messages.error(request, 'Invalid account details.')
    return render(request,'withdraw_money.html')

def transfer_money(request):
    if request.method == 'POST':
        s_name = request.POST.get('s_name')
        s_phone = request.POST.get('s_phone')
        r_name = request.POST.get('r_name')
        r_phone = request.POST.get('r_phone')
        transfer_amount = float(request.POST.get('transfer_amount'))

        try:
            # Retrieve sender's account
            sender_account = BankAccount.objects.get(name=s_name, phone=s_phone)
            sender_balance = sender_account.balance

            if sender_balance < transfer_amount:
                messages.error(request, "Oops! Your current balance is less than the transfer amount.")
            else:
                # Deduct amount from sender's account
                sender_account.balance -= transfer_amount
                sender_account.save()
                # Retrieve recipient's account
                recipient_account = BankAccount.objects.get(name=r_name, phone=r_phone)
                recipient_account.balance += transfer_amount
                recipient_account.save()

                messages.success(request, f'Transfer of {transfer_amount} successful! New balance: {sender_account.balance}.')
        except BankAccount.DoesNotExist:
            messages.error(request, "Invalid account details provided.")
    return render(request,'transfer_money.html')

def account_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        try:
            # Retrieve account details based on name and phone number
            account = BankAccount.objects.get(name=name, phone=phone)
            context = {
                'account': account
            }
            return render(request, 'account_details.html', context)
        except BankAccount.DoesNotExist:
            messages.error(request, "Account not found. Please check your details.")
    return render(request,'account_details.html')