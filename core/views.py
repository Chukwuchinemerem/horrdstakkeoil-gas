from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.db import transaction as db_transaction
from django.utils import timezone
from datetime import date
from decimal import Decimal, InvalidOperation
from .models import (
    UserProfile, KYCVerification, Equipment, EquipmentListing,
    Rental, WalletAddress, Transaction, Notification, PasswordResetToken, WithdrawalRequest
)


def is_admin(user):
    return user.is_staff or user.is_superuser


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


# ─── PUBLIC ─────────────────────────────────────────────────────────────────

def home(request):
    equipment = Equipment.objects.filter(status='available')[:9]
    services = [
        {'title':'Equipment Rental',      'desc':'Access our premium fleet of oil tankers, trucks, offshore platforms, and underground safe tanks.','icon':'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4'},
        {'title':'Oil & Gas Investment',  'desc':'Earn 8–24% annual ROI by investing in professionally managed oil and gas operations.','icon':'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'},
        {'title':'Sell Your Equipment',   'desc':'List your oil and gas equipment for sale on our platform and reach global buyers instantly.','icon':'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z'},
        {'title':'Crypto & Bank Payments','desc':'Pay via BTC, ETH, USDT TRC20, SOL or wire transfer through 6 major US banks.','icon':'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'},
        {'title':'KYC Verification',      'desc':'Fully verified accounts unlock higher deposit limits and investment tiers.','icon':'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z'},
        {'title':'24/7 Expert Support',   'desc':'Dedicated account managers and round-the-clock technical support for all rentals.','icon':'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z'},
    ]
    steps = [
        {'title':'Create Account',  'desc':'Register free in 2 minutes with basic company information.'},
        {'title':'Fund Wallet',     'desc':'Deposit via crypto or bank wire transfer instantly.'},
        {'title':'Choose Equipment','desc':'Browse and select from 200+ premium equipment options.'},
        {'title':'Start Operations','desc':'Receive documentation, keys, and full technical support.'},
    ]
    languages  = ['English','Français','Español','Deutsch','Nederlands','Português','العربية','中文','日本語']
    footer_links = ['Equipment Rental','Oil & Gas Investment','Fleet Management','Offshore Operations','Pipeline Services']
    partners = [
        {'name':'Halliburton',    'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Halliburton_logo.svg/250px-Halliburton_logo.svg.png', 'bg':'#FFF0F3', 'border':'#D4002A', 'text':'#D4002A'},
        {'name':'SLB',            'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/SLB_Logo_2022.svg/250px-SLB_Logo_2022.svg.png', 'bg':'#E6F6FF', 'border':'#009DDC', 'text':'#009DDC'},
        {'name':'CONO',           'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/ConocoPhillips_logo_2.svg/250px-ConocoPhillips_logo_2.svg.png', 'bg':'#FFF5F5', 'border':'#B20000', 'text':'#B20000'},
        {'name':'ConocoPhillips', 'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/ConocoPhillips_logo_2.svg/250px-ConocoPhillips_logo_2.svg.png', 'bg':'#FFF5F5', 'border':'#B20000', 'text':'#B20000'},
        {'name':'SAUD',           'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Saudi_Aramco_Logo.svg/200px-Saudi_Aramco_Logo.svg.png', 'bg':'#F0FFF7', 'border':'#00843D', 'text':'#00843D'},
        {'name':'Saudi Aramco',   'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Saudi_Aramco_Logo.svg/200px-Saudi_Aramco_Logo.svg.png', 'bg':'#F0FFF7', 'border':'#00843D', 'text':'#00843D'},
        {'name':'BAKE',           'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Baker_Hughes_logo.svg/200px-Baker_Hughes_logo.svg.png', 'bg':'#F0F4FF', 'border':'#003087', 'text':'#003087'},
        {'name':'Baker Hughes',   'logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Baker_Hughes_logo.svg/200px-Baker_Hughes_logo.svg.png', 'bg':'#F0F4FF', 'border':'#003087', 'text':'#003087'},
    ]
    return render(request, 'core/home.html', {
        'equipment': equipment, 'services': services, 'steps': steps,
        'languages': languages, 'footer_links': footer_links, 'partners': partners,
    })


# FIXED: register_view - proper indentation and no broken if/else
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    ref_code = request.GET.get('ref', '')
    reg_features = ['Free account — no setup fees','Crypto & bank wire payments','Invest in oil & gas markets','Earn $50 per referral','24/7 live support']
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm  = request.POST.get('confirm_password', '')
        referral = request.POST.get('referral_code', '').strip()
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = get_or_create_profile(user)
            if referral:
                try:
                    rp = UserProfile.objects.get(referral_code=referral)
                    profile.referred_by = rp
                    rp.balance += Decimal('50'); rp.referral_bonus += Decimal('50'); rp.save()
                    Notification.objects.create(user=rp.user, title='Referral Bonus!',
                        message=f'{username} joined using your referral link. You earned $50.00!')
                except UserProfile.DoesNotExist:
                    pass
            profile.save()
            login(request, user)
            messages.success(request, f'Welcome to Hordstake, {username}!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Registration error: {str(e)}')
            return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})
    return render(request, 'core/register.html', {'ref_code': ref_code, 'reg_features': reg_features})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            nxt = request.GET.get('next', '')
            if nxt:
                return redirect(nxt)
            return redirect('admin_dashboard' if (user.is_staff or user.is_superuser) else 'dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def equipment_list(request):
    category = request.GET.get('category', '')
    equipment = Equipment.objects.filter(status='available')
    if category:
        equipment = equipment.filter(category=category)
    invest_plans = [
        {'name':'Starter', 'roi':8,  'min':'500',    'max':'4,999',     'lock':30, 'payout':'Monthly', 'featured':False},
        {'name':'Growth',  'roi':16, 'min':'5,000',  'max':'24,999',    'lock':60, 'payout':'Monthly', 'featured':True},
        {'name':'Premium', 'roi':24, 'min':'25,000', 'max':'Unlimited', 'lock':90, 'payout':'Monthly', 'featured':False},
    ]
    invest_steps = ['Choose a Plan','Deposit Funds','We Operate','Earn Returns']
    return render(request, 'core/equipment_list.html', {
        'equipment': equipment, 'selected_category': category,
        'invest_plans': invest_plans, 'invest_steps': invest_steps,
    })


def equipment_detail(request, pk):
    item = get_object_or_404(Equipment, pk=pk)
    return render(request, 'core/equipment_detail.html', {'item': item})


# ─── USER DASHBOARD ─────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    profile  = get_or_create_profile(request.user)
    rentals  = Rental.objects.filter(user=request.user).order_by('-created_at')[:5]
    txns     = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    unread   = Notification.objects.filter(user=request.user, is_read=False).count()
    active_r = Rental.objects.filter(user=request.user, status='active').count() + profile.manual_active_rentals
    total_sp = (Transaction.objects.filter(user=request.user, transaction_type='rental', status='confirmed').aggregate(Sum('amount'))['amount__sum'] or 0) + profile.manual_total_spent
    my_listings = EquipmentListing.objects.filter(user=request.user).order_by('-created_at')[:3]
    try:
        kyc = request.user.kyc
    except KYCVerification.DoesNotExist:
        kyc = None
    popup_txn = Transaction.objects.filter(user=request.user, transaction_type='deposit', status='confirmed', popup_shown=False).first()
    quick_actions = [
        {'title':'Deposit Funds',      'sub':'Add via crypto or bank wire',   'url':'/deposit/',              'icon':'M12 4v16m8-8H4',                   'bg':'rgba(37,99,235,0.12)', 'color':'#3B82F6'},
        {'title':'Browse Equipment',   'sub':'Rent from our full fleet',       'url':'/equipment/',            'icon':'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4','bg':'rgba(34,197,94,0.12)','color':'#22C55E'},
        {'title':'Sell Equipment',     'sub':'List your gear for sale',        'url':'/sell/',                 'icon':'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z','bg':'rgba(168,85,247,0.12)','color':'#A855F7'},
        {'title':'Invest in Oil & Gas','sub':'Earn up to 24% annual ROI',      'url':'/equipment/?type=invest','icon':'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',  'bg':'rgba(234,179,8,0.12)','color':'#EAB308'},
        {'title':'Invest in Gold',    'sub':'Earn up to 22% annual ROI',      'url':'/gold-invest/',          'icon':'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 8v1m0-9a9 9 0 110 18A9 9 0 0112 3z','bg':'rgba(251,191,36,0.15)','color':'#F59E0B'},
        {'title':'KYC Verification',   'sub':'Verify your identity',           'url':'/kyc/',                  'icon':'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z','bg':'rgba(37,99,235,0.12)','color':'#60A5FA'},
        {'title':'Withdraw Funds',     'sub':'Cash out your balance',          'url':'/withdraw/',             'icon':'M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z','bg':'rgba(239,68,68,0.10)','color':'#EF4444'},
    ]
    return render(request, 'core/dashboard.html', {
        'profile':profile,'rentals':rentals,'transactions':txns,
        'unread_notifications':unread,'active_rentals':active_r,'total_spent':total_sp,
        'quick_actions':quick_actions,'kyc':kyc,'popup_txn':popup_txn,'my_listings':my_listings,
    })


@login_required
def rent_equipment(request, pk):
    item    = get_object_or_404(Equipment, pk=pk, status='available')
    profile = get_or_create_profile(request.user)
    today   = date.today().isoformat()
    if request.method == 'POST':
        start_str = request.POST.get('start_date')
        end_str   = request.POST.get('end_date')
        notes     = request.POST.get('notes', '')
        try:
            start = date.fromisoformat(start_str)
            end   = date.fromisoformat(end_str)
            if end <= start:
                messages.error(request, 'End date must be after start date.')
                return render(request, 'core/rent_equipment.html', {'item':item,'profile':profile,'today':today})
            duration   = (end - start).days
            total_cost = item.daily_rate * duration
            if profile.balance < total_cost:
                messages.error(request, f'Insufficient balance. Need ${total_cost:.2f}, have ${profile.balance:.2f}.')
                return render(request, 'core/rent_equipment.html', {'item':item,'profile':profile,'today':today})
            with db_transaction.atomic():
                rental = Rental.objects.create(user=request.user,equipment=item,start_date=start,end_date=end,duration_days=duration,total_cost=total_cost,status='active',notes=notes)
                profile.balance -= total_cost; profile.save()
                item.status = 'rented'; item.save()
                Transaction.objects.create(user=request.user,transaction_type='rental',amount=total_cost,status='confirmed',description=f'Rental: {item.name} for {duration} days',rental=rental,receipt_generated=True)
                Notification.objects.create(user=request.user,title='Rental Confirmed!',message=f'Your rental for {item.name} has been confirmed for {duration} days at ${total_cost:.2f}.')
            messages.success(request, f'Successfully rented {item.name}!')
            return redirect('my_rentals')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'core/rent_equipment.html', {'item':item,'profile':profile,'today':today})


@login_required
def my_rentals(request):
    profile = get_or_create_profile(request.user)
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_rentals.html', {'rentals':rentals,'profile':profile})


GOLD_PLANS = [
    {'name':'Silver Gold', 'roi':10, 'min':'500',    'max':'9,999',     'lock':30, 'payout':'Monthly', 'featured':False,
     'perks':['Gold-backed asset pool','Monthly interest payments','Dedicated account manager','Secure vault storage']},
    {'name':'Gold Elite',  'roi':16, 'min':'10,000', 'max':'49,999',    'lock':60, 'payout':'Monthly', 'featured':True,
     'perks':['Priority gold allocation','Real-time portfolio dashboard','Bi-weekly performance reports','Premium account manager']},
    {'name':'Platinum',    'roi':22, 'min':'50,000', 'max':'Unlimited', 'lock':90, 'payout':'Monthly', 'featured':False,
     'perks':['Exclusive gold reserve access','Custom investment strategy','Weekly portfolio review','Direct CEO access']},
]

@login_required
def gold_invest_view(request):
    profile = get_or_create_profile(request.user)
    return render(request, 'core/gold_invest.html', {
        'profile': profile,
        'gold_plans': GOLD_PLANS,
    })

@login_required
def gold_deposit_view(request):
    profile = get_or_create_profile(request.user)
    wallets = WalletAddress.objects.filter(is_active=True)
    plan_name = request.GET.get('plan', '')
    selected_plan = next((p for p in GOLD_PLANS if p['name'].lower().replace(' ','_') == plan_name), None)
    if request.method == 'POST':
        amount  = request.POST.get('amount', '')
        crypto  = request.POST.get('crypto', '')
        tx_hash = request.POST.get('tx_hash', '')
        plan    = request.POST.get('plan_name', '')
        try:
            amount_val = Decimal(str(amount))
            if amount_val <= 0: raise ValueError
            Transaction.objects.create(
                user=request.user, transaction_type='deposit',
                amount=amount_val, status='pending',
                crypto_type=crypto, tx_hash=tx_hash,
                description=f'Gold Investment – {plan} Plan via {crypto}'
            )
            Notification.objects.create(
                user=request.user,
                title='Gold Investment Submitted',
                message=f'Your gold investment of ${amount_val:.2f} ({plan} Plan) via {crypto} is awaiting admin confirmation.'
            )
            messages.success(request, 'Gold investment submitted! Awaiting admin confirmation.')
            return redirect('gold_deposit')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid amount.')
    return render(request, 'core/gold_deposit.html', {
        'profile': profile, 'wallets': wallets,
        'plan_name': plan_name, 'selected_plan': selected_plan,
        'gold_plans': GOLD_PLANS,
    })


def deposit_view(request):
    profile = get_or_create_profile(request.user)
    wallets = WalletAddress.objects.filter(is_active=True)
    if request.method == 'POST':
        amount  = request.POST.get('amount','')
        crypto  = request.POST.get('crypto','')
        tx_hash = request.POST.get('tx_hash','')
        try:
            amount_val = Decimal(str(amount))
            if amount_val <= 0: raise ValueError
            Transaction.objects.create(user=request.user,transaction_type='deposit',amount=amount_val,status='pending',crypto_type=crypto,tx_hash=tx_hash,description=f'Deposit via {crypto}')
            Notification.objects.create(user=request.user,title='Deposit Submitted',message=f'Your deposit of ${amount_val:.2f} via {crypto} is awaiting admin confirmation.')
            messages.success(request, 'Deposit submitted! Awaiting admin confirmation.')
            return redirect('deposit')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid amount.')
    return render(request, 'core/deposit.html', {'profile':profile,'wallets':wallets})


@login_required
def withdraw_view(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount','')
        crypto = request.POST.get('crypto','')
        wallet_address = request.POST.get('wallet_address','')
        try:
            amount_val = Decimal(str(amount))
            if amount_val <= 0 or amount_val > profile.balance:
                messages.error(request, 'Invalid amount or insufficient balance.')
                return render(request, 'core/withdraw.html', {'profile':profile})
            WithdrawalRequest.objects.create(user=request.user,amount=amount_val,crypto_type=crypto,wallet_address=wallet_address)
            profile.balance -= amount_val; profile.save()
            Transaction.objects.create(user=request.user,transaction_type='withdrawal',amount=amount_val,status='pending',crypto_type=crypto,description=f'Withdrawal via {crypto}')
            Notification.objects.create(user=request.user,title='Withdrawal Requested',message=f'Your withdrawal of ${amount_val:.2f} via {crypto} has been submitted.')
            messages.success(request, 'Withdrawal request submitted!')
            return redirect('withdraw')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid amount.')
    return render(request, 'core/withdraw.html', {'profile':profile})


@login_required
def transactions_view(request):
    profile = get_or_create_profile(request.user)
    txns    = Transaction.objects.filter(user=request.user)
    return render(request, 'core/transactions.html', {'profile':profile,'transactions':txns})


@login_required
def notifications_view(request):
    profile = get_or_create_profile(request.user)
    notifs  = Notification.objects.filter(user=request.user)
    notifs.update(is_read=True)
    return render(request, 'core/notifications.html', {'profile':profile,'notifications':notifs})


@login_required
def referral_view(request):
    profile       = get_or_create_profile(request.user)
    referred_users = UserProfile.objects.filter(referred_by=profile)
    return render(request, 'core/referral.html', {'profile':profile,'referred_users':referred_users})


# ─── SELL / EQUIPMENT LISTINGS ───────────────────────────────────────────────

@login_required
def sell_equipment(request):
    profile = get_or_create_profile(request.user)
    my_listings = EquipmentListing.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        try:
            listing = EquipmentListing.objects.create(
                user           = request.user,
                title          = request.POST.get('title','').strip(),
                category       = request.POST.get('category',''),
                description    = request.POST.get('description','').strip(),
                asking_price   = float(request.POST.get('asking_price',0)),
                year_of_make   = request.POST.get('year_of_make','').strip(),
                condition      = request.POST.get('condition','').strip(),
                location       = request.POST.get('location','').strip(),
                payment_method = request.POST.get('payment_method','both'),
                bank_name      = request.POST.get('bank_name','').strip(),
                account_name   = request.POST.get('account_name','').strip(),
                account_number = request.POST.get('account_number','').strip(),
                routing_number = request.POST.get('routing_number','').strip(),
                crypto_wallet  = request.POST.get('crypto_wallet','').strip(),
                crypto_type    = request.POST.get('crypto_type','').strip(),
                image          = request.FILES.get('image'),
            )
            Notification.objects.create(
                user=request.user, title='Listing Submitted',
                message=f'Your listing "{listing.title}" has been submitted and is under review. You will be notified once approved.'
            )
            messages.success(request, 'Your equipment listing has been submitted for review!')
            return redirect('my_listings')
        except Exception as e:
            messages.error(request, f'Error submitting listing: {str(e)}')
    return render(request, 'core/sell_equipment.html', {'profile':profile,'my_listings':my_listings})


@login_required
def my_listings(request):
    profile = get_or_create_profile(request.user)
    listings = EquipmentListing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_listings.html', {'profile':profile,'listings':listings})


# ─── KYC ────────────────────────────────────────────────────────────────────

@login_required
def kyc_submit(request):
    profile = get_or_create_profile(request.user)
    try:
        kyc = request.user.kyc
    except KYCVerification.DoesNotExist:
        kyc = None
    if request.method == 'POST' and (not kyc or kyc.status == 'rejected'):
        full_name = request.POST.get('full_name','').strip()
        dob       = request.POST.get('date_of_birth','')
        address   = request.POST.get('address','').strip()
        ssn       = request.POST.get('ssn','').strip()
        id_doc    = request.FILES.get('id_document')
        selfie    = request.FILES.get('selfie')
        if not all([full_name, dob, address, id_doc, selfie]):
            messages.error(request, 'All fields except SSN are required.')
            return render(request, 'core/kyc_submit.html', {'profile':profile,'kyc':kyc})
        if kyc and kyc.status == 'rejected':
            kyc.full_name=full_name; kyc.date_of_birth=dob; kyc.address=address
            kyc.ssn=ssn; kyc.id_document=id_doc; kyc.selfie=selfie
            kyc.status='pending'; kyc.admin_note=''; kyc.save()
        else:
            KYCVerification.objects.create(user=request.user,full_name=full_name,date_of_birth=dob,address=address,ssn=ssn,id_document=id_doc,selfie=selfie)
        Notification.objects.create(user=request.user,title='KYC Submitted',message='Your KYC documents are under review. We will notify you within 24 hours.')
        messages.success(request, 'KYC submitted successfully! Under review.')
        return redirect('kyc_status')
    return render(request, 'core/kyc_submit.html', {'profile':profile,'kyc':kyc})


@login_required
def kyc_status(request):
    profile = get_or_create_profile(request.user)
    try:
        kyc = request.user.kyc
    except KYCVerification.DoesNotExist:
        kyc = None
    return render(request, 'core/kyc_status.html', {'profile':profile,'kyc':kyc})


# ─── RECEIPT ────────────────────────────────────────────────────────────────

@login_required
def view_receipt(request, pk):
    txn     = get_object_or_404(Transaction, pk=pk, user=request.user, status='confirmed', receipt_generated=True)
    profile = get_or_create_profile(request.user)
    ref_short = str(txn.reference)[:8].upper()
    details = [
        ('Receipt No.',      f'HSK-{ref_short}'),
        ('Transaction Type', txn.get_transaction_type_display()),
        ('Amount',           f'${txn.amount:,.2f} USD'),
        ('Payment Method',   f'{txn.crypto_type or "N/A"} Cryptocurrency'),
        ('Transaction Hash', txn.tx_hash or 'N/A'),
        ('Reference ID',     str(txn.reference)),
        ('Status',           'CONFIRMED'),
        ('Date & Time',      txn.created_at.strftime('%B %d, %Y at %H:%M UTC')),
    ]
    return render(request, 'core/receipt.html', {'txn':txn,'profile':profile,'details':details})


@login_required
def download_receipt(request, pk):
    txn     = get_object_or_404(Transaction, pk=pk, user=request.user, status='confirmed', receipt_generated=True)
    ref_short = str(txn.reference)[:8].upper()
    content = f"""HORDSTAKE ENERGY SOLUTIONS
Official Payment Receipt
{'='*50}

Receipt No:     HSK-{ref_short}
Date & Time:    {txn.created_at.strftime('%B %d, %Y at %H:%M UTC')}
Status:         CONFIRMED

{'─'*50}
PAYER DETAILS
Name:           {txn.user.get_full_name() or txn.user.username}
Username:       {txn.user.username}
Email:          {txn.user.email}

{'─'*50}
TRANSACTION DETAILS
Type:           {txn.get_transaction_type_display()}
Amount:         ${txn.amount:,.2f} USD
Payment Method: {txn.crypto_type or 'N/A'}
TX Hash:        {txn.tx_hash or 'N/A'}
Reference ID:   {str(txn.reference)}

{'='*50}
Hordstake Energy Solutions
hordstake.com  |  +2349121304245
ISO Certified | Licensed & Insured
"""
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="Hordstake-Receipt-HSK-{ref_short}.txt"'
    return response


# ─── API ────────────────────────────────────────────────────────────────────

@login_required
def api_popup_check(request):
    txn = Transaction.objects.filter(user=request.user, transaction_type='deposit', status='confirmed', popup_shown=False).first()
    if txn:
        txn.popup_shown = True; txn.save()
        return JsonResponse({'show':True,'amount':str(txn.amount),'crypto':txn.crypto_type,'ref':str(txn.reference)[:8].upper(),'receipt_url':f'/receipt/{txn.pk}/'})
    return JsonResponse({'show':False})


@login_required
def api_notifications(request):
    notifs = Notification.objects.filter(user=request.user, is_read=False)[:5]
    return JsonResponse({'count':notifs.count(),'notifications':[{'title':n.title,'message':n.message,'created_at':n.created_at.isoformat()} for n in notifs]})


# ─── ADMIN ──────────────────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users      = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_revenue    = Transaction.objects.filter(status='confirmed', transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
    active_rentals   = Rental.objects.filter(status='active').count()
    pending_deposits = Transaction.objects.filter(transaction_type='deposit', status='pending').count()
    pending_kyc      = KYCVerification.objects.filter(status='pending').count()
    pending_listings = EquipmentListing.objects.filter(status='pending').count()
    recent_txns      = Transaction.objects.all().order_by('-created_at')[:10]
    recent_users     = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    for u in recent_users: get_or_create_profile(u)
    recent_users = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')[:5]
    admin_actions = [
        {'title':'Confirm Deposits',    'sub':'Review pending payments',       'url':'/admin_dashboard/transactions/','icon':'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',                                                                                           'bg':'rgba(34,197,94,0.12)', 'color':'#22C55E'},
        {'title':'KYC Management',      'sub':f'{pending_kyc} pending',         'url':'/admin_dashboard/kyc/',         'icon':'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z','bg':'rgba(168,85,247,0.12)','color':'#A855F7'},
        {'title':'Sale Listings',       'sub':f'{pending_listings} pending',    'url':'/admin_dashboard/listings/',    'icon':'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z','bg':'rgba(234,179,8,0.12)', 'color':'#EAB308'},
        {'title':'Add Funds',           'sub':'Credit user accounts',           'url':'/admin_dashboard/add-funds/',   'icon':'M12 4v16m8-8H4',                                                                                                                          'bg':'rgba(37,99,235,0.12)', 'color':'#3B82F6'},
        {'title':'Wallet Settings',     'sub':'Update crypto addresses',        'url':'/admin_dashboard/wallet-settings/','icon':'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z',                                            'bg':'rgba(239,68,68,0.10)', 'color':'#EF4444'},
    ]
    return render(request, 'core/admin/dashboard.html', {
        'total_users':total_users,'total_revenue':total_revenue,'active_rentals':active_rentals,
        'pending_deposits':pending_deposits,'pending_kyc':pending_kyc,'pending_listings':pending_listings,
        'recent_transactions':recent_txns,'recent_users':recent_users,'admin_actions':admin_actions,
    })


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    for u in users: get_or_create_profile(u)
    users = User.objects.filter(is_superuser=False).select_related('profile').order_by('-date_joined')
    return render(request, 'core/admin/users.html', {'users':users})


@login_required
@user_passes_test(is_admin)
def admin_user_detail(request, pk):
    viewed_user = get_object_or_404(User, pk=pk)
    profile     = get_or_create_profile(viewed_user)
    txns        = Transaction.objects.filter(user=viewed_user).order_by('-created_at')
    rentals     = Rental.objects.filter(user=viewed_user).order_by('-created_at')
    try:
        kyc = viewed_user.kyc
    except KYCVerification.DoesNotExist:
        kyc = None
    return render(request, 'core/admin/user_detail.html', {'viewed_user':viewed_user,'profile':profile,'transactions':txns,'rentals':rentals,'kyc':kyc})


@login_required
@user_passes_test(is_admin)
def admin_add_funds(request):
    users = User.objects.filter(is_superuser=False).order_by('username')
    for u in users: get_or_create_profile(u)
    users = User.objects.filter(is_superuser=False).select_related('profile').order_by('username')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        amount  = request.POST.get('amount')
        note    = request.POST.get('note','Manual credit by admin')
        try:
            user       = User.objects.get(pk=user_id)
            profile    = get_or_create_profile(user)
            amount_val = Decimal(str(amount))
            profile.balance += amount_val; profile.save()
            Transaction.objects.create(user=user,transaction_type='manual',amount=amount_val,status='confirmed',description=note,receipt_generated=True)
            Notification.objects.create(user=user,title='Funds Added',message=f'${amount_val:.2f} has been credited to your account. {note}')
            messages.success(request, f'${amount_val:.2f} added to {user.username}.')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'core/admin/add_funds.html', {'users':users})




@login_required
@user_passes_test(is_admin)
def admin_add_referral_bonus(request):
    """Admin page to add referral bonus to any user account."""
    users = User.objects.filter(is_superuser=False).order_by('username')
    for u in users:
        get_or_create_profile(u)
    users = User.objects.filter(is_superuser=False).select_related('profile').order_by('username')

    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        amount  = request.POST.get('amount', '').strip()
        note    = request.POST.get('note', 'Referral bonus credited by admin').strip()
        try:
            user        = User.objects.get(pk=user_id)
            profile     = get_or_create_profile(user)
            amount_val  = Decimal(str(amount))
            if amount_val <= 0:
                messages.error(request, 'Amount must be greater than zero.')
            else:
                profile.referral_bonus += amount_val
                profile.save()
                Transaction.objects.create(
                    user=user,
                    transaction_type='referral',
                    amount=amount_val,
                    status='confirmed',
                    description=note,
                    receipt_generated=True,
                )
                Notification.objects.create(
                    user=user,
                    title='Referral Bonus Credited',
                    message=(
                        f'${amount_val:.2f} referral bonus has been added to your account. '
                        f'{note}'
                    ),
                )
                messages.success(
                    request,
                    f'Referral bonus of ${amount_val:.2f} successfully credited to {user.username}. '
                    f'New referral balance: ${profile.referral_bonus:.2f}'
                )
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f'Invalid amount: {e}')
        except Exception as e:
            messages.error(request, str(e))

    recent_referral_txns = Transaction.objects.filter(
        transaction_type='referral'
    ).select_related('user').order_by('-created_at')[:20]

    return render(request, 'core/admin/add_referral_bonus.html', {
        'users': users,
        'preselect': request.GET.get('user', ''),
        'recent_referral_txns': recent_referral_txns,
    })


@login_required
@user_passes_test(is_admin)
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_superuser:
        messages.error(request, "Cannot delete a superuser.")
        return redirect('admin_users')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" has been permanently deleted.')
        return redirect('admin_users')
    return render(request, 'core/admin/delete_user_confirm.html', {'viewed_user': user})


@login_required
@user_passes_test(is_admin)
def admin_deduct_funds(request, pk):
    viewed_user = get_object_or_404(User, pk=pk)
    profile = get_or_create_profile(viewed_user)
    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        note = request.POST.get('note', 'Manual deduction by admin')
        try:
            amount_val = Decimal(str(amount))
            if amount_val <= 0:
                messages.error(request, 'Amount must be greater than zero.')
            elif amount_val > profile.balance:
                messages.error(request, f'Insufficient balance. User only has ${profile.balance:.2f}.')
            else:
                profile.balance -= amount_val
                profile.save()
                Transaction.objects.create(user=viewed_user, transaction_type='manual', amount=-amount_val, status='confirmed', description=note, receipt_generated=False)
                Notification.objects.create(user=viewed_user, title='Account Adjustment', message=f'${amount_val:.2f} has been deducted from your account. {note}')
                messages.success(request, f'${amount_val:.2f} deducted from {viewed_user.username}.')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f'Invalid amount: {e}')
        return redirect('admin_user_detail', pk=pk)
    return redirect('admin_user_detail', pk=pk)


@login_required
@user_passes_test(is_admin)
def admin_toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_superuser:
        messages.error(request, "Cannot suspend a superuser.")
        return redirect('admin_user_detail', pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "suspended"
        messages.success(request, f'User "{user.username}" has been {status}.')
        Notification.objects.create(user=user, title='Account Status Update', message=f'Your account has been {status} by an administrator.')
    return redirect('admin_user_detail', pk=pk)

@login_required
@user_passes_test(is_admin)
def admin_rentals(request):
    return render(request, 'core/admin/rentals.html', {'rentals':Rental.objects.all().order_by('-created_at')})


# FIXED: wallet_settings - wrapped in try/except to avoid 500 errors
@login_required
@user_passes_test(is_admin)
def admin_wallet_settings(request):
    cryptos = [
        ('USDT','Tether USDT (TRC20)','#26A17B','TRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
        ('BTC', 'Bitcoin (BTC)',      '#F7931A','1Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
        ('ETH', 'Ethereum (ETH)',     '#627EEA','0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
        ('SOL', 'Solana (SOL)',       '#9945FF','SoLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'),
    ]
    try:
        wallets = list(WalletAddress.objects.all())
    except Exception:
        wallets = []
    if request.method == 'POST':
        try:
            for crypto, _, _, _ in cryptos:
                address = request.POST.get(f'address_{crypto}', '').strip()
                network = request.POST.get(f'network_{crypto}', '').strip()
                if address:
                    WalletAddress.objects.update_or_create(
                        crypto=crypto,
                        defaults={'address': address, 'network': network, 'is_active': True}
                    )
            messages.success(request, 'Wallet addresses updated successfully.')
        except Exception as e:
            messages.error(request, f'Error saving wallets: {str(e)}')
        return redirect('admin_wallet_settings')
    return render(request, 'core/admin/wallet_settings.html', {'wallets':wallets,'cryptos':cryptos})


@login_required
@user_passes_test(is_admin)
def admin_transactions(request):
    return render(request, 'core/admin/transactions.html', {'transactions':Transaction.objects.all().order_by('-created_at')})


@login_required
@user_passes_test(is_admin)
def admin_confirm_deposit(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, transaction_type='deposit', status='pending')
    profile = get_or_create_profile(txn.user)
    profile.balance += txn.amount; profile.save()
    txn.status = 'confirmed'; txn.receipt_generated = True; txn.popup_shown = False; txn.save()
    Notification.objects.create(user=txn.user, title='Deposit Confirmed! 🎉',
        message=f'Your crypto deposit of ${txn.amount:.2f} via {txn.crypto_type or "crypto"} has been confirmed and added to your balance.')
    messages.success(request, f'Deposit of ${txn.amount} confirmed for {txn.user.username}.')
    return redirect('admin_transactions')


@login_required
@user_passes_test(is_admin)
def admin_reject_deposit(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, transaction_type='deposit', status='pending')
    txn.status = 'rejected'; txn.save()
    Notification.objects.create(user=txn.user, title='Deposit Rejected',
        message=f'Your deposit of ${txn.amount:.2f} was rejected. Please contact support.')
    messages.warning(request, 'Deposit rejected.')
    return redirect('admin_transactions')


# FIXED: notifications view - wrapped in try/except to avoid 500 errors
@login_required
@user_passes_test(is_admin)
def admin_notifications(request):
    try:
        if request.method == 'POST':
            title   = request.POST.get('title','')
            message = request.POST.get('message','')
            target  = request.POST.get('target','all')
            if not title or not message:
                messages.error(request, 'Title and message are required.')
                return redirect('admin_notifications')
            if target == 'all':
                for u in User.objects.filter(is_staff=False, is_superuser=False):
                    Notification.objects.create(user=u, title=title, message=message, is_broadcast=True)
                messages.success(request, f'Broadcast sent to all users.')
            else:
                uid = request.POST.get('user_id','')
                if uid:
                    try:
                        Notification.objects.create(user=User.objects.get(pk=uid), title=title, message=message)
                        messages.success(request, 'Notification sent.')
                    except User.DoesNotExist:
                        messages.error(request, 'User not found.')
            return redirect('admin_notifications')
        users  = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
        notifs = Notification.objects.all().order_by('-created_at')[:30]
        return render(request, 'core/admin/notifications.html', {'users':users,'notifications':notifs})
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        users  = User.objects.filter(is_staff=False, is_superuser=False)
        return render(request, 'core/admin/notifications.html', {'users':users,'notifications':[]})


@login_required
@user_passes_test(is_admin)
def admin_equipment(request):
    return render(request, 'core/admin/equipment.html', {'equipment':Equipment.objects.all()})


@login_required
@user_passes_test(is_admin)
def admin_add_equipment(request):
    """Disabled — equipment catalogue is managed via seed_equipment management command."""
    messages.info(request,
        'Manual equipment creation is disabled. The catalogue is pre-configured with '
        '20 professional oil & gas equipment items. Contact your system administrator to update.')
    return redirect('admin_equipment')


@login_required
@user_passes_test(is_admin)
def admin_delete_equipment(request, pk):
    """Delete an equipment item. Only works via POST for safety."""
    item = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        name = item.name
        # Also free up any active rentals referencing this equipment
        Rental.objects.filter(equipment=item, status='active').update(status='cancelled')
        item.delete()
        messages.success(request, f'"{name}" has been deleted from the catalog.')
    return redirect('admin_equipment')


@login_required
@user_passes_test(is_admin)
def admin_kyc_list(request):
    status_filter = request.GET.get('status','')
    kycs = KYCVerification.objects.select_related('user').order_by('-submitted_at')
    if status_filter:
        kycs = kycs.filter(status=status_filter)
    return render(request, 'core/admin/kyc_list.html', {'kycs':kycs,'status_filter':status_filter})


@login_required
@user_passes_test(is_admin)
def admin_kyc_detail(request, pk):
    kyc = get_object_or_404(KYCVerification, pk=pk)
    return render(request, 'core/admin/kyc_detail.html', {'kyc':kyc})


@login_required
@user_passes_test(is_admin)
def admin_kyc_approve(request, pk):
    kyc = get_object_or_404(KYCVerification, pk=pk)
    kyc.status = 'approved'; kyc.reviewed_at = timezone.now(); kyc.save()
    Notification.objects.create(user=kyc.user, title='KYC Approved ✅',
        message='Your identity has been verified. Your account is now fully verified on Hordstake.')
    messages.success(request, f'KYC approved for {kyc.user.username}.')
    return redirect('admin_kyc_list')


@login_required
@user_passes_test(is_admin)
def admin_kyc_reject(request, pk):
    kyc  = get_object_or_404(KYCVerification, pk=pk)
    note = request.POST.get('note','Documents did not meet verification requirements.')
    kyc.status = 'rejected'; kyc.admin_note = note; kyc.reviewed_at = timezone.now(); kyc.save()
    Notification.objects.create(user=kyc.user, title='KYC Rejected ❌',
        message=f'Your KYC was rejected. Reason: {note}. Please resubmit with valid documents.')
    messages.warning(request, f'KYC rejected for {kyc.user.username}.')
    return redirect('admin_kyc_list')


# ─── ADMIN SALE LISTINGS ─────────────────────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_listings(request):
    listings = EquipmentListing.objects.all().order_by('-created_at')
    return render(request, 'core/admin/listings.html', {'listings':listings})


@login_required
@user_passes_test(is_admin)
def admin_listing_approve(request, pk):
    listing = get_object_or_404(EquipmentListing, pk=pk)
    listing.status = 'approved'; listing.save()
    Notification.objects.create(user=listing.user, title='Listing Approved ✅',
        message=f'Your listing "{listing.title}" has been approved and is now live on the platform.')
    messages.success(request, f'Listing "{listing.title}" approved.')
    return redirect('admin_listings')


@login_required
@user_passes_test(is_admin)
def admin_listing_sold(request, pk):
    listing = get_object_or_404(EquipmentListing, pk=pk)
    listing.status = 'sold'; listing.save()
    Notification.objects.create(user=listing.user, title='Equipment Sold! 🎉',
        message=f'Your equipment "{listing.title}" listed at ${listing.asking_price:,.2f} has been successfully sold! Payment will be processed to your registered payment details.')
    messages.success(request, f'Listing "{listing.title}" marked as sold.')
    return redirect('admin_listings')


@login_required
@user_passes_test(is_admin)
def admin_listing_reject(request, pk):
    listing = get_object_or_404(EquipmentListing, pk=pk)
    note = request.POST.get('note','Listing did not meet platform requirements.')
    listing.status = 'rejected'; listing.admin_note = note; listing.save()
    Notification.objects.create(user=listing.user, title='Listing Rejected',
        message=f'Your listing "{listing.title}" was rejected. Reason: {note}')
    messages.warning(request, f'Listing "{listing.title}" rejected.')
    return redirect('admin_listings')


# ─── ADMIN MANAGE USER DASHBOARD FIGURES ─────────────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_manage_user_figures(request, pk):
    """Manage active rentals and total spent figures for a specific user."""
    viewed_user = get_object_or_404(User, pk=pk)
    profile = get_or_create_profile(viewed_user)
    
    # Calculate actual figures
    actual_active_rentals = Rental.objects.filter(user=viewed_user, status='active').count()
    actual_total_spent = Transaction.objects.filter(user=viewed_user, transaction_type='rental', status='confirmed').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    # Calculate displayed figures (actual + manual adjustments)
    displayed_active_rentals = actual_active_rentals + profile.manual_active_rentals
    displayed_total_spent = actual_total_spent + profile.manual_total_spent
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        if action == 'adjust_rentals':
            try:
                adjustment = int(request.POST.get('adjustment', 0))
                profile.manual_active_rentals = max(0, profile.manual_active_rentals + adjustment)
                profile.save()
                messages.success(request, f'Active rentals adjusted by {adjustment:+d}. New adjustment: {profile.manual_active_rentals}')
            except (ValueError, TypeError):
                messages.error(request, 'Invalid rental adjustment value.')
        
        elif action == 'adjust_spent':
            try:
                adjustment = Decimal(request.POST.get('adjustment', '0.00'))
                new_value = profile.manual_total_spent + adjustment
                profile.manual_total_spent = max(Decimal('0.00'), new_value)
                profile.save()
                messages.success(request, f'Total spent adjusted by ${adjustment:+.2f}. New adjustment: ${profile.manual_total_spent:.2f}')
            except (ValueError, InvalidOperation):
                messages.error(request, 'Invalid amount.')
        
        elif action == 'reset_rentals':
            profile.manual_active_rentals = 0
            profile.save()
            messages.success(request, 'Active rentals adjustment reset to 0.')
        
        elif action == 'reset_spent':
            profile.manual_total_spent = Decimal('0.00')
            profile.save()
            messages.success(request, 'Total spent adjustment reset to $0.00.')
        
        return redirect('admin_manage_user_figures', pk=pk)
    
    return render(request, 'core/admin/manage_user_figures.html', {
        'viewed_user': viewed_user,
        'profile': profile,
        'actual_active_rentals': actual_active_rentals,
        'actual_total_spent': actual_total_spent,
        'displayed_active_rentals': displayed_active_rentals,
        'displayed_total_spent': displayed_total_spent,
    })


# ═══════════════════════════════════════════════════════════════════════════════
#  PASSWORD RESET  (No SMTP — works on Render free plan & any free hosting)
#  Flow: user enters username → token created → admin sees token URL in admin
#        dashboard OR user gets a link at /reset/<token>/ directly
# ═══════════════════════════════════════════════════════════════════════════════

def forgot_password(request):
    """Step 1: User submits their username to request a reset link."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        try:
            user = User.objects.get(username=username)
            # Invalidate all previous tokens for this user
            PasswordResetToken.objects.filter(user=user, used=False).update(used=True)
            # Create fresh token
            token_obj = PasswordResetToken.objects.create(user=user)
            reset_url = request.build_absolute_uri(f'/reset-password/{token_obj.token}/')
            # Store in session so the page can show the link
            request.session['reset_link'] = reset_url
            request.session['reset_username'] = username
            messages.success(request, f'Reset link generated for <strong>{username}</strong>.')
            return redirect('forgot_password_link')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that username. Please check and try again.')

    return render(request, 'core/forgot_password.html')


def forgot_password_link(request):
    """Step 2: Show the reset link. User copies it or contacts admin to confirm."""
    reset_link = request.session.get('reset_link')
    username   = request.session.get('reset_username')
    if not reset_link:
        return redirect('forgot_password')
    return render(request, 'core/forgot_password_link.html', {
        'reset_link': reset_link,
        'username': username,
    })


def reset_password(request, token):
    """Step 3: User visits the link and sets a new password."""
    token_obj = PasswordResetToken.objects.filter(token=token).first()

    if not token_obj:
        messages.error(request, 'This reset link is invalid.')
        return redirect('forgot_password')
    if not token_obj.is_valid():
        messages.error(request, 'This reset link has expired or already been used. Please request a new one.')
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            token_obj.user.set_password(password1)
            token_obj.user.save()
            token_obj.used = True
            token_obj.save()
            # Clear session
            request.session.pop('reset_link', None)
            request.session.pop('reset_username', None)
            messages.success(request, 'Password updated successfully! You can now sign in.')
            return redirect('login')

    return render(request, 'core/reset_password.html', {'token': token, 'reset_user': token_obj.user})


# ═══════════════════════════════════════════════════════════════════════════════
#  ADMIN — DEDUCT REFERRAL BONUS
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_admin)
def admin_deduct_referral_bonus(request):
    """Admin page to deduct referral bonus from a user account."""
    users = User.objects.filter(is_superuser=False).order_by('username')
    for u in users:
        get_or_create_profile(u)
    users = User.objects.filter(is_superuser=False).select_related('profile').order_by('username')

    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        amount  = request.POST.get('amount', '').strip()
        note    = request.POST.get('note', 'Referral bonus deducted by admin').strip()
        try:
            user        = User.objects.get(pk=user_id)
            profile     = get_or_create_profile(user)
            amount_val  = Decimal(str(amount))
            if amount_val <= 0:
                messages.error(request, 'Amount must be greater than zero.')
            elif amount_val > profile.referral_bonus:
                messages.error(
                    request,
                    f'Cannot deduct ${amount_val:.2f} — {user.username} only has '
                    f'${profile.referral_bonus:.2f} in referral bonus.'
                )
            else:
                profile.referral_bonus -= amount_val
                profile.save()
                Transaction.objects.create(
                    user=user,
                    transaction_type='manual',
                    amount=amount_val,
                    status='confirmed',
                    description=f'[DEDUCT REFERRAL] {note}',
                    receipt_generated=False,
                )
                Notification.objects.create(
                    user=user,
                    title='Referral Bonus Adjustment',
                    message=(
                        f'${amount_val:.2f} has been deducted from your referral bonus balance. '
                        f'{note}'
                    ),
                )
                messages.success(
                    request,
                    f'Deducted ${amount_val:.2f} referral bonus from {user.username}. '
                    f'Remaining referral balance: ${profile.referral_bonus:.2f}'
                )
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        except (InvalidOperation, ValueError) as e:
            messages.error(request, f'Invalid amount: {e}')

    recent_deductions = Transaction.objects.filter(
        description__startswith='[DEDUCT REFERRAL]'
    ).select_related('user').order_by('-created_at')[:20]

    return render(request, 'core/admin/deduct_referral_bonus.html', {
        'users': users,
        'preselect': request.GET.get('user', ''),
        'recent_deductions': recent_deductions,
    })
