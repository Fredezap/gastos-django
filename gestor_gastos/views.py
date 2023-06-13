from django.shortcuts import render, redirect
from .models import Category, Movements
from .forms import MovementsPaymentForm, CategoryForm, MovementsFundsForm, SavingsDepositForm, SavingsWithdrawForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Sum


def index(request):
    return render(request, '../templates/index.html')

def movementsIndex(request):
    try:
        last_movement = Movements.objects.latest('id')
        current_funds = last_movement.salary_funds_after
    except:
        last_movement = {}
        current_funds = 0
    if request.method == "GET":
        movements = Movements.objects.all().order_by('-id')
        context = {
            'current_funds': current_funds,
            'movements': movements,
            'is_get': True
        }
        return render(request, '../templates/movements/index.html', context)
    if request.method == "POST":
        year = request.POST['year']
        month = request.POST['month']
        month = int(month)
        movements = Movements.objects.filter(date__year=year, date__month=month).order_by('-id')
        context = {
                    'month': month,
                    'year': year,
                    'movements': movements,
                    'current_funds': current_funds,
                }
        return render(request, '../templates/movements/index.html', context)
    
def movementsCreate(request):
    if request.method == "GET":
        categories = Category.objects.filter(is_payment=True).order_by('name')
        form = MovementsPaymentForm()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, '../templates/movements/create.html', context)
    
    if request.method == "POST":
        form = MovementsPaymentForm(request.POST)
        
        if form.is_valid():
            
            #Get info and do math to update funds - checks
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            savings = form.cleaned_data['savings']
            total_amount = amount + savings
            
            if amount <= 0:
                messages.error(request, "No puedes realizar un pago de valor $0 o menor")
                return redirect('movementsIndex')
            
            try:
                last_movement = Movements.objects.latest('id')
                current_funds_last_movement = last_movement.salary_funds_after
            except:
                current_funds_last_movement = 0

            new_current_funds = current_funds_last_movement - total_amount
            
            if total_amount > current_funds_last_movement:
                messages.error(request, "Saldo insuficiente")
                return redirect('movementsIndex')

            categoryCurrentFunds = category.current_funds
            categoryNewFunds = categoryCurrentFunds + savings
            
            #Update category data
            if savings > 0:
                category.last_funds = categoryCurrentFunds
                category.current_funds = categoryNewFunds
                category.save()
            

            #Instance new info to save it
            new_movement = form.save(commit=False)
            new_movement.category = category
            new_movement.amount = amount
            new_movement.savings = savings
            new_movement.total_amount = total_amount
            new_movement.salary_funds_before = current_funds_last_movement
            new_movement.salary_funds_after = new_current_funds
            new_movement.savings_funds_before = categoryCurrentFunds
            new_movement.savings_funds_after = categoryNewFunds
            new_movement.save()

            messages.success(request, f"Has agregado un pago en concepto de {category}")
            return redirect('movementsIndex')
        else:
            messages.error(request, "Ocurrio un error")
            return redirect('movementsIndex')

def categoriesIndex(request, letter = None):
    if request.method == "GET":
        try:
            last_movement = Movements.objects.latest('id')
            current_funds = last_movement.salary_funds_after
        except:
            current_funds = 0
        if letter != None:
            categories = Category.objects.filter(name__istartswith=letter).order_by('-current_funds')
        else:
            name = request.GET.get('search', '').capitalize()
            categories = Category.objects.filter(name__contains=name).order_by('-current_funds')
        context = {
            'categories': categories,
            'current_funds': current_funds
        }
        return render(request, '../templates/categories/index.html', context)

def categoriesCreate(request):
    if request.method == "GET":
        form = CategoryForm() 
        context = {
            'form': form
        }
        return render(request, '../templates/categories/create.html', context)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            categoryName = form.cleaned_data['name'].capitalize()
            print(categoryName)
            print(type(categoryName))
            try:
                check_already_exist = Category.objects.get(name=categoryName)
                print(check_already_exist)
            except ObjectDoesNotExist:
                check_already_exist = None
            print(check_already_exist)
            if check_already_exist == None:
                new_category.name = categoryName
                new_category.save()
                messages.success(request, "Has agregado una nueva categoria")
                return redirect('categoriesIndex')
            else:
                messages.error(request, "ERROR<br><br>Categoría existente")
                return redirect('categoriesIndex')

def fundsIndex(request):
    if request.method == "GET":
        try:
            last_movement = Movements.objects.latest('id')
            current_funds = last_movement.salary_funds_after
        except:
            current_funds = 0
        context = {
            'current_funds': current_funds
        }
        return render(request, '../templates/funds/index.html', context)

def fundsMovementCreate(request):
    if request.method == "GET":    
        form = MovementsFundsForm()
        context = {
            'form': form,
        }
        return render(request, '../templates/funds/createMovement.html', context)
    if request.method == "POST":
        form = MovementsFundsForm(request.POST)
        if form.is_valid():
            
            new_movement = form.save(commit=False)
            amount = form.cleaned_data['amount']
            categoryName = form.cleaned_data['category']
            
            category= Category.objects.get(name=categoryName)
            categoryCurrentFunds =  category.current_funds
            
            try:
                last_movement = Movements.objects.latest('id')
                funds_last_movement = last_movement.salary_funds_after
            except:
                funds_last_movement = 0

            current_funds = funds_last_movement + amount
            
            new_movement.amount = amount
            new_movement.total_amount = amount
            new_movement.salary_funds_before = funds_last_movement
            new_movement.salary_funds_after = current_funds
            new_movement.avings_funds_before = categoryCurrentFunds
            new_movement.savings_funds_after = categoryCurrentFunds
            new_movement.save()
            messages.success(request, f"Has agregado $ {amount} pesos")
            return redirect('fundsIndex')
        else:
            messages.error(request, "Ocurrio un error")
            return redirect('fundsIndex')
        
def savingsDeposit(request, id):
    category = Category.objects.get(id=id)
    
    if request.method == "GET":    
        form = SavingsDepositForm()
        context = {
            'form': form,
            'category': category,
        }
        return render(request, '../templates/savings/savingsDeposit.html', context)
    
    if request.method == "POST":
        form = SavingsDepositForm(request.POST)
        if form.is_valid():
            
            #Get info and do math to update funds
            savings = form.cleaned_data['savings']
            categoryCurrentFunds =  category.current_funds
            categoryNewFunds = categoryCurrentFunds + savings
            
            try:
                last_movement = Movements.objects.latest('id')
                funds_last_movement = last_movement.salary_funds_after
            except:
                funds_last_movement = 0

            current_funds = funds_last_movement - savings
            
            if savings > funds_last_movement:
                messages.error(request, "Saldo insuficiente")
                return redirect('categoriesIndex')
            
            #Instance new info to save it
            new_movement = form.save(commit=False)
            new_movement.category = category
            new_movement.amount = 0
            new_movement.savings = savings
            new_movement.total_amount = savings
            new_movement.salary_funds_before = funds_last_movement
            new_movement.salary_funds_after = current_funds
            new_movement.savings_funds_before = categoryCurrentFunds
            new_movement.savings_funds_after = categoryNewFunds
            new_movement.payment_method = f"Ingreso ahorros a categoria {category}"
            new_movement.save()
            
            #Update category data
            category.last_funds = categoryCurrentFunds
            category.current_funds = categoryNewFunds
            category.save()
                        
            messages.success(request, f"Has agregado $ {savings} pesos a la categoria {category}")
            return redirect('categoriesIndex')
        else:
            messages.error(request, "Ocurrio un error")
            return redirect('categoriesIndex')

def savingsWithdraw(request, id):
    category = Category.objects.get(id=id)
    
    if request.method == "GET":    
        form = SavingsWithdrawForm()
        context = {
            'form': form,
            'category': category,
        }
        return render(request, '../templates/savings/savingsWithdraw.html', context)
    
    if request.method == "POST":
        form = SavingsWithdrawForm(request.POST)
        if form.is_valid():
            
            #Get info and do math to update funds
            amount = form.cleaned_data['amount']
            categoryCurrentFunds =  category.current_funds
            categoryNewFunds = categoryCurrentFunds - amount
            
            try:
                last_movement = Movements.objects.latest('id')
                funds_last_movement = last_movement.salary_funds_after
            except:
                funds_last_movement = 0

            current_funds = funds_last_movement + amount
            
            if amount > categoryCurrentFunds:
                messages.error(request, "Saldo insuficiente")
                return redirect('categoriesIndex')
            
            #Instance new info to save it
            new_movement = form.save(commit=False)
            new_movement.category = category
            new_movement.amount = amount
            new_movement.savings = 0
            new_movement.total_amount = amount
            new_movement.salary_funds_before = funds_last_movement
            new_movement.salary_funds_after = current_funds
            new_movement.savings_funds_before = categoryCurrentFunds
            new_movement.savings_funds_after = categoryNewFunds
            new_movement.payment_method = f"Extraccion ahorros de la categoria {category}"
            new_movement.is_savings_withdraw = True
            new_movement.save()
            
            #Update category data
            category.last_funds = categoryCurrentFunds
            category.current_funds = categoryNewFunds
            category.save()
                        
            messages.success(request, f"Has extraido $ {amount} pesos de la categoria {category}")
            return redirect('categoriesIndex')
        else:
            messages.error(request, "Ocurrio un error")
            return redirect('categoriesIndex')

def movementsMonthly(request):
    if request.method == "GET":
        date_movements = Movements.objects.values('date__year', 'date__month').annotate(year=Count('date__year')).order_by('date__year', '-date__month')
        context = {
            'date_movements': date_movements
        }
        return render(request, '../templates/movements/monthly.html', context)
    if request.method == "POST":
        year = request.POST['year']
        month = request.POST['month']
        month = int(month)
        
        first_movement_month = Movements.objects.filter(date__year=year, date__month=month)[:1]
        for data in first_movement_month:
            salary_amount_start_month = data.salary_funds_before

        total_savings_month = 0
        
        categories = Category.objects.all()
        category_total_details = []
        for category in categories:

            total_savings_withdraw_category = Movements.objects.filter(Q(category=category), Q(date__year=year, date__month=month), Q(is_savings_withdraw=True)).aggregate(total=Sum('amount'))['total']
            if total_savings_withdraw_category == None:
                total_savings_withdraw_category = 0
            total_savings_deposit_category1 = Movements.objects.filter(Q(category=category), Q(date__year=year, date__month=month), Q(amount=0)).aggregate(total=Sum('savings'))['total']
            if total_savings_deposit_category1 == None:
                total_savings_deposit_category1 = 0
            total_savings_deposit_category2 = Movements.objects.filter(Q(category=category), Q(date__year=year, date__month=month),Q(category__is_payment=True), Q(amount__gt=0), Q(is_savings_withdraw=False)).aggregate(total=Sum('savings'))['total']
            if total_savings_deposit_category2 == None:
                total_savings_deposit_category2 = 0
            total_payments_category = Movements.objects.filter(Q(category=category), Q(date__year=year, date__month=month), Q(category__is_payment=True), Q(is_savings_withdraw=False), Q(amount__gt=0)).aggregate(total=Sum('amount'))['total']
            if total_payments_category == None:
                total_payments_category = 0
            total_transfer_incomes_category= Movements.objects.filter(Q(category=category), Q(date__year=year, date__month=month), Q(savings=0), Q(category__is_payment=False)).aggregate(total=Sum('amount'))['total']
            if total_transfer_incomes_category == None:
                total_transfer_incomes_category = 0
            
            total_savings_deposit_category = total_savings_deposit_category1 + total_savings_deposit_category2
            
            total_savings_category = category.current_funds
            total_savings_month += total_savings_category
            
            category_total_details.append((category, total_savings_withdraw_category, total_savings_deposit_category, total_payments_category, total_transfer_incomes_category, total_savings_category))
        
        total_savings_withdraw_month = 0
        total_savings_deposit_month = 0
        total_payments_month = 0
        total_transfer_incomes_month = 0
        
        for data in category_total_details:
            total_savings_withdraw_month += data[1]
            total_savings_deposit_month += data[2]
            total_payments_month += data[3]
            total_transfer_incomes_month += data[4]
        
        total_spends_month = total_savings_deposit_month + total_payments_month
        total_incomes_month = total_transfer_incomes_month + total_savings_withdraw_month
        total_month = total_incomes_month - total_spends_month
        category_total_details.sort(key=lambda x: x[3],reverse=True)

    total_payments_category_percentaje = ["{:.2f}".format((x[3] / total_payments_month) * 100) for x in category_total_details]
    fusion = list(zip(category_total_details, total_payments_category_percentaje))
    proccessed_data = [(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], data) for tuple, data in fusion]
    
    context = {
        'proccessed_data': proccessed_data,
        'category_total_details': category_total_details,
        'total_savings_deposit_month': total_savings_deposit_month,
        'total_savings_withdraw_month': total_savings_withdraw_month,
        'total_transfer_incomes_month': total_transfer_incomes_month,
        'total_incomes_month': total_incomes_month,
        'total_payments_month': total_payments_month,
        'total_transfer_incomes_month': total_transfer_incomes_month,
        'total_spends_month': total_spends_month,
        'total_month': total_month,
        'month': month,
        'salary_amount_start_month': salary_amount_start_month,
        'total_savings_month': total_savings_month,
    }
    return render(request, '../templates/movements/month_detail.html', context)