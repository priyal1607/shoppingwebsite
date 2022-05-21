from datetime import date
from operator import index
from tkinter import LAST
from django.contrib import messages
from email.message import EmailMessage
from turtle import color
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from shopping.models import product,category,register,addtocart,deresses,contactss
import random
from django.db.models import Q
import ssl ,smtplib
from email.mime.text import MIMEText
from .forms import productform
import razorpay
from django.views.decorators.csrf import csrf_exempt
def showall(req):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        a=product.objects.all()
        v=product.objects.all().order_by('-date')
        j=deresses.objects.all()
        return render(req,'index.html',{'a':a,'m':m,'vv':v,'j':j})
    else:
        a=product.objects.all()
        v=product.objects.all().order_by('-date')
        j=deresses.objects.all()
        return render(req,'index.html',{'a':a,'vv':v,'j':j})

def cart(req):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        return render(req,'cart.html',{'m':m})
    
def check(req):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        return render(req,'checkout.html',{'m':m})
        
def checkout(req):
    if req.session.has_key('email'):
        a=req.session['email']
        m=register.objects.get(email=a)
        cart=addtocart.objects.filter(personname=m.pk)
        count = addtocart.objects.filter(personname=m.pk).count()
        l=[]
        p=0
        for i in cart:
            l.append(i.productname)
            p=p+i.price
        return render(req,'checkout.html',{'cart':cart,'p':p,'l':l,'m':m,'d':p+100,'g':count})
    else:
        return redirect(loginview)
def details(req):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        a=product.objects.all()
        return render(req,'detail.html',{'a':a,'m':m})
    else:
        a=product.objects.all()
        return render(req,'detail.html',{'a':a})
def shop(req):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        a=product.objects.all()
        return render(req,'shop.html',{'a':a,'m':m})
    else:
        a=product.objects.all()
        return render(req,'shop.html',{'a':a})

def view(req,pk):
    if req.session.has_key('email'):
        s=req.session['email']
        m=register.objects.get(email=s)
        a=product.objects.all()
        c=get_object_or_404(product,pk=pk)
        return render(req,'detail.html',{'c':c,'a':a,'m':m})
    else:
        a=product.objects.all()
        c=get_object_or_404(product,pk=pk)
        return render(req,'detail.html',{'c':c,'a':a})
def delete(req,pk):
        c=get_object_or_404(product,pk=pk)
        c.delete()
        return redirect(showall)
def edit(request,pk):
    c=get_object_or_404(product,pk=pk)
    f=productform(request.POST or None,instance=c)
    if f.is_valid():
        f.save()
        return redirect(showall)
    return render(request,'edit.html',{'f':f})
def registerview(request):
    if request.method=="POST":
        a=register()
        a.name=request.POST['name']
        a.password=request.POST['password']
        a.cpassword=request.POST['cpassword']
        a.email=request.POST['email']
        a.phoneno=request.POST['phoneno']
        if a.password==a.cpassword:
            a.save()
        else:
            return HttpResponse("pls re-enter confirm password")
    return render(request,'register.html')

def loginview(request):
    if request.method=="POST":
        try:
            b=register.objects.get(email=request.POST['email'])
            if b.password==request.POST['password']:
                email=request.POST.get('email')
                request.session['email']=email
                return redirect(showall)
            else:
                return HttpResponse("<h1>pls enter valid password</h1>")
        except:
             return HttpResponse("not found")
    return render(request,'login.html')
def logoutUSer(request):
    if request.session.has_key('email'):
        del request.session['email']
        return redirect(showall)

def forgotpwd(request):
    email=request.POST.get('email')
    request.session['email'] = email
    if email==None:
        return render(request,'email.html')
    print(email)
    otp=""
    rand1=random.choice('0123456789')
    rand2=random.choice('0123456789')
    rand3=random.choice('0123456789')
    rand4=random.choice('0123456789')
    otp=rand1+rand2+rand3+rand4
    print(otp)
    request.session['otp']=otp

    port = 465
    password = "123456Pp@"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
    server.login("psavaliya943@gmail.com",password)
    msg=MIMEText("welcome\n" + email + "\nyour otp is : "+ otp +"\nplease don't share with others")
    msg['subject']='security mail'
    server.sendmail("psavaliya943@gmail.com",email,msg.as_string())
    server.quit()
    print(msg)
    
    return redirect(otpcheck)
def otpcheck(request):
    if request.session.has_key('otp'):
        otp=request.session['otp']
        try:
            otpobj=request.POST.get('otp')
            if otpobj==None:
                return render(request,'otp.html')
            if otp==request.POST.get('otp'):
                return redirect(newpwd)
            else:
                return HttpResponse("<a href=''>wrong otp entered</a>")
        except:
            return redirect('login')
    return render(request,'otp.html')
def newpwd(request):
    if request.session.has_key('email'):
        newpassword=request.POST.get('password')
        if newpassword==None:
            return render(request,'forgotpassword.html')
        obj=register.objects.get(email=request.session['email'])
        obj.password=newpassword
        obj.cpassword=newpassword
        obj.save()
    else:
            return redirect(loginview)
    return render(request,'forgotpassword.html')
def carts(request,id):
    if 'email' in request.session:
        per=register.objects.get(email=request.session['email'])
        i=product.objects.get(id=id)
        if addtocart.objects.filter(personname_id=per.id,productname_id=i.id).exists():
            return(HttpResponse("this product is already exists,please choose another"))
        else:
            cart=addtocart()
            cart.personname=per
            cart.productname=i
            cart.price=i.price
            cart.save()
        return (redirect(showall))
    else:
        return redirect(loginview)
def add_to_cart(request,id):
    email = request.session['email']
    personname = register.objects.get(email=email)
    productname = product.objects.get(id=id)
    count = addtocart.objects.filter(personname_id=personname.id,productname_id=productname.id).count()
    cart = addtocart.objects.filter(personname_id=personname.id,productname_id=productname.id)
    print("####",count)
    if count>0:
        quantity= cart[0].foodname+1
        price = quantity*productname.price
        addtocart.objects.filter(personname_id=personname.id,productname_id=productname.id).update(quantity=quantity,price=price)
        return redirect('index')
    else:
        addtocart(personname_id=personname.id,productname_id=productname.id,quantity=1,price=productname.price).save()
        return redirect('index')


def minus(request,id):
    cart = addtocart.objects.filter(id=id)
    if cart[0].quantity==1:
        quantity = 1
    else:
        quantity= cart[0].quantity-1

    price = quantity * cart[0].productname.price
    addtocart.objects.filter(id=id).update(price=price,quantity=quantity)
    return redirect(viewcart)

def plus(request,id):
    cart = addtocart.objects.filter(id=id)
    quantity = cart[0].quantity+1
    price = quantity * cart[0].productname.price
    addtocart.objects.filter(id=id).update(price=price,quantity=quantity)
    return redirect(viewcart)

def viewcart(request):
    if request.session.has_key('email'):
        a=request.session['email']
        m=register.objects.get(email=a)
        cart=addtocart.objects.filter(personname=m.pk)
        count=addtocart.objects.filter(personname=m.pk).count()
        l=[]
        p=0
        for i in cart:
            l.append(i.productname)
            p=p+i.price
        return render(request,'cart.html',{'cart':cart,'p':p,'l':l,'m':m,'d':p+100,'g':count})
        
    else:
        return redirect(loginview)
def deletecart(request,pk):
    c=get_object_or_404(addtocart,pk=pk)
    c.delete()
    return redirect(viewcart)

def c(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        a=product.objects.all()
        v=category.objects.all()
        j=deresses.objects.all()
        vv=product.objects.filter(date=date.today())
        return render(request,'index.html',{'m':m,'v':v,'a':a,'j':j,'vv':vv})
    else:
        j=deresses.objects.all()
        a=product.objects.all()
        v=category.objects.all()
        vv=product.objects.filter(date=date.today())
        return render(request,'index.html',{'v':v,'a':a,'j':j,'vv':vv})
        
def categ(request,name):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        c=category.objects.get(name=name)
        j=deresses.objects.all()
        p=product.objects.all().filter(cat=c)
        v=product.objects.filter(date=date.today())
        return render(request,'catw.html',{'m':m,'c':c,'p':p,'j':j,'vv':v})
    else:
        c=category.objects.get(name=name)
        j=deresses.objects.all()
        p=product.objects.all().filter(cat=c).distinct()
        v=product.objects.filter(date=date.today())
        return render(request,'catw.html',{'c':c,'p':p,'j':j,'vv':v})
def home(request):
    if request.session.has_key('email'):
        a=request.session['email']
        m=register.objects.get(email=a)
        cart=addtocart.objects.filter(personname=m.pk)
        l=[]
        p=0
        for i in cart:
            l.append(i.productname)
            p=p+i.price
        p=p+100
        pp=p*100
        name = request.POST.get('name')
        amount = 50000
        amount =pp
        if request.method=="POST":
            client = razorpay.Client(
                auth=("rzp_test_X3FfcfEy2LCgca", "nwdqRktfnNsOSMHWOkHfgtBd"))
            payment = client.order.create({'amount': amount,'currency': 'INR',
                                       'payment_capture': '1'})
            cart.delete()
            return redirect(success)
           
        return render(request, 'index1.html',{'amount':amount,'p':p})
    

@csrf_exempt
def success(request):
    return render(request, "success.html")

def search(request):
    try:
        q = request.GET.get('search')
    except:
        q = None
    if q:
        request.session.has_key('email')
        s=request.session['email']
        m=register.objects.get(email=s)
        j=deresses.objects.all()
        products= product.objects.filter(Q(name__icontains=q)| Q(img__icontains=q) | Q(price__icontains=q))
        
        data = {
            'p' : products,
            'm':m,
            'j':j
        }
    else:
        request.session.has_key('email')
        s=request.session['email']
        m=register.objects.get(email=s)
        j=deresses.objects.all()
        data={'m':m,'j':j}
    
    return render(request, 'search.html',data)

def pcat(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        aa=product.objects.filter(range='100-200')
        return render(request,'shop1.html',{'aa':aa,'m':m})

    else:
        aa=product.objects.filter(range='100-200')
        return render(request,'shop1.html',{'aa':aa})

def pcatt(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        bb=product.objects.filter(range='200-300')
        return render(request,'shop1.html',{'bb':bb,'m':m})

    else:
        bb=product.objects.filter(range='200-300')
        return render(request,'shop1.html',{'bb':bb})
def pcattt(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        cc=product.objects.filter(range='300-400')
        return render(request,'shop1.html',{'cc':cc,'m':m})

    else:
        cc=product.objects.filter(range='300-400')
        return render(request,'shop1.html',{'cc':cc})
def pcatttt(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        dd=product.objects.filter(range='400-500')
        return render(request,'shop1.html',{'dd':dd,'m':m})

    else:
        dd=product.objects.filter(range='400-500')
        return render(request,'shop1.html',{'dd':dd})

def col(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        s=product.objects.filter(color='red')
        return render(request,'shop1.html',{'s':s,'m':m})

    else:
        s=product.objects.filter(color='red')
        return render(request,'shop1.html',{'s':s})

def colo(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        t=product.objects.filter(color='white')
        return render(request,'shop1.html',{'t':t,'m':m})

    else:
        t=product.objects.filter(color='white')
        return render(request,'shop1.html',{'t':t})
def color(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        u=product.objects.filter(color='blue')
        return render(request,'shop1.html',{'u':u,'m':m})

    else:
        u=product.objects.filter(color='blue')
        return render(request,'shop1.html',{'u':u})

def colorr(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        v=product.objects.filter(color='black')
        return render(request,'shop1.html',{'v':v,'m':m})

    else:
        v=product.objects.filter(color='black')
        return render(request,'shop1.html',{'v':v})

def size(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        p=product.objects.filter(size='XL')
        return render(request,'shop1.html',{'p':p,'m':m})

    else:
        p=product.objects.filter(size='XL')
        return render(request,'shop1.html',{'p':p})

def sizes(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        q=product.objects.filter(size='S')
        return render(request,'shop1.html',{'q':q,'m':m})

    else:
        q=product.objects.filter(size='S')
        return render(request,'shop1.html',{'q':q})
def sizess(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        r=product.objects.filter(size='M')
        return render(request,'shop1.html',{'r':r,'m':m})

    else:
        r=product.objects.filter(size='M')
        return render(request,'shop1.html',{'r':r})

def sizesss(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        s=product.objects.filter(size='L')
        return render(request,'shop1.html',{'sh':s,'m':m})

    else:
        s=product.objects.filter(size='L')
        return render(request,'shop1.html',{'sh':s})

def sort(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        v=product.objects.filter(date=date.today())
        z=product.objects.all().order_by('-date')
        return render(request,'sort.html',{'vv':v,'m':m,'z':z})
    else:
        v=product.objects.filter(date=date.today())
        z=product.objects.all().order_by('-date')
        return render(request,'sort.html',{'vv':v,'z':z})

def prof(request):
    if request.session.has_key('email'):
        s=request.session['email']
        m=register.objects.get(email=s)
        return render(request,'profile.html',{'m':m})
    else:
        return redirect(loginview)

def editprof(request):
   if request.session.has_key('email'):
       d=register.objects.get(email=request.session['email'])
       if request.method=='POST':
           d.name=request.POST.get('name')
           d.email=request.POST.get('email')
           d.phone=request.POST.get('phone')
           d.save()
           return redirect(loginview)
   return render(request,'editpro.html',{'d':d})


def contactsss(request):
    if request.session.has_key('email'):
        d=register.objects.get(email=request.session['email'])
        if request.method=='POST':
            a=contactss()
            a.name = request.POST['name']
            a.email = request.POST['email']
            a.msg = request.POST['msg']
            a.save()
            print(a.msg)

            msg = EmailMessage()
            msg.set_content(f'''
            Thank you for connecting with us.

            name: {a.name}
            email: {a.email}
            msg: {a.msg}
            ''')

            msg['Subject'] = 'shopping'
            msg['From'] = "psavaliya943@gmail.com"
            msg['To'] = a.email

            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("psavaliya943@gmail.com", "123456Pp@")
            server.send_message(msg)
            server.quit()
            messages.info(request,'Message had been sent. Thank you for your notes.')
            return redirect(showall)
        return render(request,'contact.html',{'m':d})
    else:
        if request.method=='POST':
            a=contactss()
            a.name = request.POST['name']
            a.email = request.POST['email']
            a.msg = request.POST['msg']
            a.save()
            print(a.msg)

            msg = EmailMessage()
            msg.set_content(f'''
            Thank you for connecting with us.

            name: {a.name}
            email: {a.email}
            msg: {a.msg}
            ''')

            msg['Subject'] = 'shopping'
            msg['From'] = "psavaliya943@gmail.com"
            msg['To'] = a.email

            # Send the message via our own SMTP server.
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("psavaliya943@gmail.com", "123456Pp@")
            server.send_message(msg)
            server.quit()
            messages.info(request,'Message had been sent. Thank you for your notes.')
            return redirect(showall)
        return render(request,'contact.html')
    

def ms(request):
    if request.session.has_key('email'):
        a=request.session['email']
        m=register.objects.get(email=a)
        cart=addtocart.objects.filter(personname=m.pk)
        l=[]
        p=0
        for i in cart:
            l.append(i.productname)
            p=p+i.price
        p=p+100
        p=str(p)
        request.session['price']=p
        


        port = 465
        password = "123456Pp@"
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com",port,context=context)
        server.login("psavaliya943@gmail.com",password)
        msg=MIMEText("welcome\n" + a + "\nyour total amount  is : "+ p +"\nyour order will be  delivered in next five days")
        msg['subject']='payment'
        server.sendmail("psavaliya943@gmail.com",a,msg.as_string())
        server.quit()
        print(msg)
        cart.delete()
        return HttpResponse("<h2>your order will be  delivered in next five days </h2>")
    else:
        return redirect(loginview)


            


# Create your views here.
