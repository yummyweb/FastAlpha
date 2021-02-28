from django.shortcuts import render
from products.models import Company, Product
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Home(request):
    return render(request, 'products/home.html')

def CompanyView(request, id):
    company = Company.objects.get(id=id)

    context = {
        "company": company
    }

    return render(request, 'products/company.html', context)

def CompanyCreate(request):
    if request.method == "POST":
        files = request.FILES

        try:
            newCompany = Company.objects.create(
                name=request.POST['name'], 
                description=request.POST['description'], 
                user=request.user,
                logo=files.get('logo'),
                header=files.get('header'),
                merchant_id=request.POST['merchant_id'],
                secret_key=request.POST['secret_key']
            )
        except:
           newCompany = Company.objects.create(
                name=request.POST['name'], 
                description=request.POST['description'], 
                user=request.user,
                logo=files.get('logo'),
                header=files.get('header')
            )

        newCompany.save()

    return render(request, 'products/company_create.html')

def Products(request):
    products = Product.objects.all()

    context = {
        "products": products
    }

    return render(request, 'products/products.html', context)

def ProductCreate(request):
    if request.method == "POST":
        files = request.FILES
        newProduct = Product.objects.create(request.POST['name'], request.POST['description'])
        newProduct.image = files['image']
        newProduct.video = files['video']
        newProduct.company = request.POST['company']
        newProduct.save()

    return render(request, 'products/product_create.html')

def MakeInvestment(request, id):
    if request.method == "GET":
        return render(request, 'products/invest.html')

    company_merchant_key = None
    company_merchant_id = None

    companies = Company.objects.all()
    product_invested = Product.objects.get(id=id)

    for company in companies:
        if product_invested.company == company:
            company_merchant_key = company.secret_key
            company_merchant_id = company.merchant_id

    amount = int(request.POST['amount'])
    transaction = Transaction.objects.create(made_by=request.user, product_invested=product_invested, amount=amount)
    transaction.save()

    params = (
        ('MID', company_merchant_id),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, company_merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'products/redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'products/callback.html', context=received_data)

        return render(request, 'products/callback.html', context=received_data)