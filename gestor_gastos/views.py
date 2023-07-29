from django.shortcuts import render, redirect
from .models import Category, Movements
from .forms import MovementsPaymentForm, CategoryForm, MovementsFundsForm, SavingsDepositForm, SavingsWithdrawForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Sum
from decimal import Decimal
from django.db import IntegrityError, Error

class InsufficientFundsError(Exception):
    pass

class MovementNotCreated(Exception):
    pass

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
        form = MovementsPaymentForm()
        context = {
            'form': form,
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
            
            try:
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
            except:
                messages.error(request, "Ocurrio un error al realizar el pago")
                return redirect('movementsIndex')

        else:
            messages.error(request, "Ocurrio un error relacionado al formulario")
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
            try:
                check_already_exist = Category.objects.get(name=categoryName)
            except ObjectDoesNotExist:
                check_already_exist = None
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
            
            try:
                new_movement.amount = amount
                new_movement.total_amount = amount
                new_movement.salary_funds_before = funds_last_movement
                new_movement.salary_funds_after = current_funds
                new_movement.avings_funds_before = categoryCurrentFunds
                new_movement.savings_funds_after = categoryCurrentFunds
                new_movement.save()
                messages.success(request, f"Has agregado $ {amount} pesos")
                return redirect('fundsIndex')
            except:
                messages.error(request, "Ocurrio un error al ingresar dinero")
                return redirect('fundsIndex')

        else:
            messages.error(request, "Ocurrio un error relacionado al formulario")
            return redirect('fundsIndex')


def savingDepositLogic(request, id, savings, detail):
    form = SavingsDepositForm()
    savings = float(savings)
    #Get info and do math to update funds
    category = Category.objects.get(id=id)
    categoryCurrentFunds = float(category.current_funds)
    categoryNewFunds = categoryCurrentFunds + savings

    try:
        last_movement = Movements.objects.latest('id')
        funds_last_movement = float(last_movement.salary_funds_after)
    except:
        funds_last_movement = 0
        
    current_funds = funds_last_movement - savings

    if savings > funds_last_movement:
        raise InsufficientFundsError

    try:
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
        new_movement.detail = detail
        new_movement.save()
        #Update category data
        category.last_funds = categoryCurrentFunds
        category.current_funds = categoryNewFunds
        category.save()
    except:
        raise MovementNotCreated


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
            
            savings = form.cleaned_data['savings']
            detail = form.cleaned_data['detail']
            try:
                savingDepositLogic(request, id, savings, detail)
                messages.success(request, f"Has agregado $ {savings} pesos a la categoria {category}")
                return redirect('categoriesIndex')
            except InsufficientFundsError or MovementNotCreated:
                if InsufficientFundsError:
                    messages.error(request, "Saldo insuficiente")
                    return redirect('categoriesIndex')
                if MovementNotCreated:
                    messages.error(request, "Ocurrio un error al ingresar dinero")
                    return redirect('categoriesIndex')
        else:
            messages.error(request, "Ocurrio un error relacionado al formulario")
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
            
            try:
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

            except:
                messages.error(request, "Ocurrio un error al ingresar dinero")
                return redirect('categoriesIndex')
        else:
            messages.error(request, "Ocurrio un error relacionado al formulario")
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
            
            category_total_details.append((category, total_payments_category, total_transfer_incomes_category, 
                                        total_savings_deposit_category, total_savings_withdraw_category))
        
        total_savings_withdraw_month = 0
        total_savings_deposit_month = 0
        total_payments_month = 0
        total_transfer_incomes_month = 0
        
        for data in category_total_details:
            total_payments_month += data[1]
            total_transfer_incomes_month += data[2]
            total_savings_deposit_month += data[3]
            total_savings_withdraw_month += data[4]
        
        total_spends_month = total_savings_deposit_month + total_payments_month
        total_incomes_month = total_transfer_incomes_month + total_savings_withdraw_month
        total_month = total_incomes_month - total_spends_month
        category_total_details.sort(key=lambda x: x[1],reverse=True)

    if total_payments_month != 0:
        total_payments_category_percentaje = ["{:.2f}".format((x[1] / total_payments_month) * 100) for x in category_total_details]
    else:
        total_payments_category_percentaje = [(0) for x in category_total_details]
    fusion = list(zip(category_total_details, total_payments_category_percentaje))
    proccessed_data = [(tuple[0], tuple[1], data, tuple[2], tuple[3], tuple[4]) for tuple, data in fusion]
    
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
    }
    return render(request, '../templates/movements/month_detail.html', context)


# Method client ask me to redistribute all the left money she has at the end of the month
def redistributeLeftoverMoney(request, current_funds = None):
    payment_categories = Category.objects.filter(is_payment=True).order_by('-percentage')
    if request.method == 'GET':

        current_funds = float(current_funds)
        if current_funds < 100:
            messages.error(request, "Tienes muy poco saldo para hacer esta operacion. Tu saldo debe ser mayor a $100")
            return redirect ('categoriesIndex')
        
        # 100% of the current funds are going to be redistribute 
        # There are some categories that have some percentage fixed.
        # Will sum all the fixed percentage to see how much have left to get 100% and redistribute in the remaining categories
        total_percentage_fixed = Category.objects.filter(is_payment=True, percentage__gt=0).aggregate(total_percentage=Sum('percentage'))
        
        # will get the remaining percentage to be divided into the remaining categories.
        total_percentage_left = - total_percentage_fixed["total_percentage"] + 100

        # Getting the quantity of categories that have 0% percentage
        total_payment_categoryes_no_percentage = Category.objects.filter(is_payment=True, percentage=0)
        
        # if total percentage fixed is grater than 100% redirect
        if total_percentage_fixed["total_percentage"] > 100:
            messages.error(request, "La suma de porcentajes fijos de las categorias ha superado el 100%\n Modifica alguans categorias para llegar a un valor de 100% o menos.")
            return redirect('categoriesIndex')
        # checking if percentage fixed is == 100 and there are no more categories to redistribute funds to avoid ZeroDivisionError
        elif total_percentage_fixed["total_percentage"] <= 100 and not total_payment_categoryes_no_percentage:
            context = {
                'payment_categories': payment_categories,
                'current_funds': current_funds,
                }
            return render(request, '../templates/categories/redistribute_leftover_money.html', context)
        else:
            # Calculating the percentage for each remaining category.
            remaining_categories_percentage = (total_percentage_left / ((len(total_payment_categoryes_no_percentage))))
            context = {
                'payment_categories': payment_categories,
                'remaining_categories_percentage': remaining_categories_percentage,
                'current_funds': current_funds,
            }
            return render(request, '../templates/categories/redistribute_leftover_money.html', context)

    if request.method == 'POST':
        
        current_funds = float(request.POST.get("current_funds"))
        
        # Getting the items and it's values from HTML form
        amount_and_id_data = []

        for key in request.POST.keys():
            if key == "amount_and_category_id":
                formData = request.POST.getlist(key)
                
                for item in formData: # Itering and creating new list with correct data values
                    data = item.split("_")
                    listData = float(data[0]), int(data[1])
                    amount_and_id_data.append(listData)
        
        if len(amount_and_id_data) == len(payment_categories): #Checking if user selected all categories

            total = 0
            for data in amount_and_id_data:
                total += data[0]
            
            for data in amount_and_id_data:
                category = Category.objects.get(id=data[1])
                break
            
            total = round(total, 2)
            verification = round(total - current_funds, 2)
            if verification > 0:
                for data in amount_and_id_data:
                    data[0] -=verification
                    break
            elif verification < 0:
                for data in amount_and_id_data:
                    data[0] += (-verification)
                    break
            amount_and_id_data_rounded = [[round(value[0], 2), int(value[1])] for value in amount_and_id_data]
            # Calling method to create 1 movement for each id and put amounts into saving of each category and substract the amount from current_funds
            for amount, id in amount_and_id_data_rounded:
                detail = "ingreso atraves de distribucion automatica de fin de mes"
                try:
                    savingDepositLogic(request, id, amount, detail)
                except InsufficientFundsError:
                    messages.error(request, "Saldo insuficiente")
                    return redirect('categoriesIndex')
                            
            if verification == 0:
                messages.success(request, f"Depositos realizados correctamente\nNo hubieron sobrantes")
                return redirect('categoriesIndex')
            elif verification < 0:
                messages.success(request, f"Depositos realizados correctamente\nSe sumaron $ {verification} a la categoria {category.name} que era un sobrante de redondeo")
                return redirect('categoriesIndex')
            else:
                messages.success(request, f"Depositos realizados correctamente\nSe restaron $ {verification} a la categoria {category.name} que era un sobrante de redondeo")
                return redirect('categoriesIndex')
        
        # verifying if all the categories has been selected or not for future Flow control
        elif len(amount_and_id_data) < len(payment_categories):
            amount_and_id_data_rounded = [[round(value[0], 2), int(value[1])] for value in amount_and_id_data_rounded]

            for amount, id in amount_and_id_data_rounded:
                try:
                    savingDepositLogic(request, id, amount)
                except InsufficientFundsError or MovementNotCreated:
                    if InsufficientFundsError:
                        messages.error(request, "Saldo insuficiente")
                        return redirect('categoriesIndex')
                    if MovementNotCreated:
                        messages.error(request, "Ocurrio un error al generar el movimiento")
                        return redirect('categoriesIndex')
            messages.success(request, f"Depositos realizados correctamente\nHa sobrado dinero ya que no seleccionaste todas las categorias")
            return redirect('categoriesIndex')
        
        else:
            messages.error(request, "Se han seleccionado mas categorias de las existentes")
            return redirect('categoriesIndex')
            
    return render(request, '../templates/categories/redistribute_leftover_money.html')