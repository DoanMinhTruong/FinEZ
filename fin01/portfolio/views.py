from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Portfolio, StockPortfolio
from .forms import CreatePortfolioForm
from django.contrib import messages
# Create your views here.
def index(request):
    portfolios = Portfolio.objects.filter(user=request.user)  # Lấy tất cả các đối tượng Portfolio
    stock_portfolio = []
    for p in portfolios:
        st = StockPortfolio.objects.filter(portfolio = p)
        for i in st:
            stock_portfolio.append(i)
    if not portfolios:
        no_portfolio_message = "Không có dự án Portfolio nào."
        return render(request, 'portfolio/list.html', {'no_portfolio_message': no_portfolio_message})
    return render(request, 'portfolio/list.html', {'portfolios': portfolios , 'stock_portfolio' : stock_portfolio})

def create(request):
    if(request.method == "GET"):
        create_form = CreatePortfolioForm()
        return render(request,'portfolio/create.html' , {'form' : create_form})
    if request.method == "POST":
        create_form = CreatePortfolioForm(request.POST)
        if(create_form.is_valid()):
            create_form.user =request.user
            create_form.save()
            return redirect('portfolio')
        return render(request,'portfolio/list.html')

def delete(request, id=None):
    if(id == None):
        return
    portfolio = Portfolio.objects.filter(user= request.user , id = id).first()
    if portfolio is not None:
        portfolio.delete()
        return redirect('portfolio')

import requests
def get_stock_price_now(code=None):
    url ="https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&size=1&q=code:" + str(code)
    
    res = requests.get(url , headers = {
      'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
  })
    res= res.json()
    print(res)
    if(len(res['data']) == 0 ):
        return -1
    res = res['data'][0]

    return res['adAverage']
    
def buy(request):
    if(request.method == "POST"):
        user = request.user
        portfolio = request.POST['portfolio']
        stock = request.POST['stock']
        amount = request.POST['amount']

        try:
            amount = int(amount)
        except:
            messages.error(request,"Invalid Amount")
            return redirect("dashboard")

        get_portfolio = Portfolio.objects.filter(name = portfolio).first()
        if(get_portfolio is None):
            messages.error(request,"Invalid Portfolio")
            return redirect("dashboard")
        if(get_portfolio.user != user):
            messages.error(request,"It is not your Portfolio")
            return redirect("dashboard")
        price_stock_now = get_stock_price_now(code = stock)
        if(price_stock_now == -1):
            messages.error(request,"Invalid stock")
            return redirect("dashboard")
        if(price_stock_now * amount > request.user.balance):
            messages.error(request,"Not enough balance")
            return redirect("dashboard")
        
        result = StockPortfolio(portfolio = get_portfolio , stock = stock, amount = amount)
        try:
            result.save()
            request.user.balance -= price_stock_now * amount
            request.user.save()
        except:
            messages.error(request , "Something went wrong")
            return redirect("dashboard")
        return redirect("portfolio")
    
def sell(request):
    return redirect("portfolio")