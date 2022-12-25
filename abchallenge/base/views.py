from django.shortcuts import render, redirect
from .models import Account, Transaction, Repayment
from datetime import timedelta, datetime
from django.db.models import Max
from .forms import AdvanceForm
from django.db import IntegrityError

def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def profile(request):
    context = {}
    return render(request, 'base/profile.html', context)


def accounts(request):
    # authentication statement
    redir = check_superUser(request)
    if  redir != None:
        return redir
        
    accounts = Account.objects.all()
    context = {'accounts': accounts}
    return render(request, 'base/accounts.html', context)


def transactions(request):
    # authentication statement
    redir = check_superUser(request)
    if  redir != None:
        return redir
        
    transactions = Transaction.objects.all()
    context = {"transactions": transactions}
    return render(request, "base/transactions.html", context)

def repayments(request):
    # authentication statement
    redir = check_superUser(request)
    if  redir != None:
        return redir

    repayments = Repayment.objects.all()
    context = {"repayments": repayments}
    return render(request, "base/repayments.html", context)

def reports(request):
    # authentication statement
    redir = check_superUser(request)
    if  redir != None:
        return redir

    last_5_days = Transaction.objects.filter(attempt_at__gte=datetime.now()-timedelta(days=5))
    context = {"last_5": last_5_days}
    return render(request, 'base/reports.html', context)

def performAdvance(request):
    # authentication statement
    redir = check_superUser(request)
    if  redir != None:
        return redir        

    context= {}
    
    # after the form has been submitted
    if request.method == "POST":
        form = AdvanceForm(request.POST)
        if form.is_valid():
            # good to go
            context['acct'] = form.cleaned_data['acct']
            context['amt'] = form.cleaned_data['amt']
            context['is_credit'] = form.cleaned_data['is_credit']
            form = AdvanceForm() 
            context['form'] = form

            # figure out if its a credit or debit here.
            if context['is_credit'] == True:
                src_acct = 0
                dst_acct = context['acct']
            else:
                src_acct = context['acct']
                dst_acct = 0
                
            crdt = _getCrdt(context['is_credit'])
            amt = context['amt']

            # call to performTransaction
            t_no = performTransaction(src_acct, dst_acct, amt, crdt)
            context['t_no'] = t_no
            print(t_no)            
            
            return render(request, 'base/perform_advance_form.html', context) # change to appropriate
    else:
        # blank form
        form = AdvanceForm()    

    # set the context with the form
    context['form'] = form

    return render(request, 'base/perform_advance_form.html', context)


def myaccount(request):
    context = {}
    return render(request, 'base/myaccount.html', context)

#checks to see if specific user is the user of the reqest
def check_superUser(request):
    print(request.user.is_superuser)
    if not request.user.is_superuser:
        return redirect("/")
    return None


# this isn't a request function
def performTransaction(src, dst, amt, direction):
    print("in performTransaction")
    context = {}
    t_no = -1
    
    # creating a line of credit or taking weekly payment?
    if direction == "credit":
        ### src = 0, check balance in src
        if not _enough_in_account(src, amt):
            ### theres not enough money in the account
            print("1Not enough money in root account")

            # create transaction with fail
            print("2creating failed transaction")
            t = Transaction(in_acct_id=dst,
                            out_acct_id=src,
                            amt=amt,
                            is_success=False)
            t.save()
        else:
            ### there is enough in account
            print("3there is enough money in root account")

            # create repayment entry
            print("5 Attempting repayment entry with non-root")
            r = Repayment(acct_id=dst,
                        total_amt=amt)
            try:
                r.save()
            except IntegrityError:
                return -1
            except Repayment.DoesNotExist:
                return -1

            # create transaction with success
            print("4 creating transaction with success")
            t = Transaction(in_acct_id=dst,
                            out_acct_id=src,
                            amt=amt,
                            is_success=True)
            t.save()

            # todo get accounts and adjust balances
            _adjust_balance(src, -amt)
            _adjust_balance(dst, amt)
    else:
        ### src != 0, check balance in dst, this is accepting payments

        if not _enough_in_account(src, amt):
            ### theres not enough money in the account
            print("6 there is not enough money in non-root account")

            # create transaction with fail
            print("7 creating failed transaction")
            t = Transaction(in_acct_id=dst,
                            out_acct_id=src,
                            amt=amt,
                            is_success=False)
            t.save()

            # find repayment r via acct_no
            print("8 getting Repayment with non-root acct_no", src)
            r = Repayment.objects.get(acct_id=src)

            # add 7 days to end_at
            print("9 adding a week to repayment plan for non-root account")
            r.end_at = r.end_at + timedelta(days=7)

            print("11 increasing num_defaults by 1")
            r.num_defaults = r.num_defaults + 1

            # save r
            r.save()
        else:
            # there is enough money in the account
            print("10 there is enough money in the non-root account")

            # todo get accounts via acct_no and adjust balances
            _adjust_balance(src, -amt)
            _adjust_balance(dst, amt)

            # if today is the end_at then remove repayment
            print("src:", src)
            end_at = Repayment.objects.get(acct=src)
            print(end_at.end_at)
            print(datetime.today().date())
            if end_at.end_at == datetime.today().date():
                print("date is today")
                end_at.delete()
            else:
                print("didn't work")

 
    qs = Transaction.objects.aggregate(Max('trans_no'))
    t_no = qs['trans_no__max']
    return t_no


def _adjust_balance(acct, amt):
    # get account
    a = Account.objects.get(acct_no=acct)
    a.principle = a.principle + amt
    a.save()
    return
    # 


# Checks to see if theres enough money in the account
def _enough_in_account(acct_no, amt):
    account = Account.objects.get(acct_no=acct_no)
    balance = account.principle
    print("checking amount in account", acct_no, "with balance", balance, "against amt", amt)
    return balance >= amt


def _getCrdt(b):
    if b:
        return "credit"
    else:
        return "debit"
    
# one time change
# id_4 = Transaction.objects.get(trans_no=4)
# id_4.attempt_at = datetime.now()-timedelta(days=6)
# id_4.save()
###