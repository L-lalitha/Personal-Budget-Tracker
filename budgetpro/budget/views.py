from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'budget/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = sum(t.amount for t in transactions if t.category == 'Income')
    total_expense = sum(t.amount for t in transactions if t.category == 'Expense')
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    }
    return render(request, 'budget/dashboard.html', context)

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    
    return render(request, 'budget/add_transaction.html', {'form': form})

def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    if transaction.user == request.user:
        transaction.delete()
    return redirect('dashboard')

from django.http import JsonResponse
from .models import Transaction
from django.utils.timezone import localtime

def transaction_chart_data(request):
    transactions = Transaction.objects.order_by('-date')[:10]  # Last 10 transactions
    data = {
        "labels": [localtime(t.date).strftime("%Y-%m-%d") for t in transactions],
        "amounts": [t.amount for t in transactions],
    }
    return JsonResponse(data)
from django.shortcuts import render
from django.http import JsonResponse
from .models import Transaction
from django.db.models import Sum
from django.utils.timezone import localtime

def dashboard(request):
    transactions = Transaction.objects.order_by('-date')[:5]  # Last 5 transactions
    total_income = Transaction.objects.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = abs(Transaction.objects.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)

    return render(request, 'budget/dashboard.html', {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
    })
def expense_chart_data(request):
    transactions = Transaction.objects.order_by('date')
    categories = transactions.values_list('description', flat=True).distinct()

    data = {
        "labels": [t.date.strftime("%Y-%m-%d") for t in transactions],  # ✅ FIXED
        "amounts": [
            abs(Transaction.objects.filter(description=cat).aggregate(Sum('amount'))['amount__sum'] or 0)
            for cat in categories
        ],
    }
    return JsonResponse(data)