from django.shortcuts import render, redirect
from . models import *
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from . decorators import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
@login_required
@logged_inn2
def admin_home(request):
    return render(request, "admin_home.html")

def home(request):
    return render(request,'login.html',)

def logout(request):
    del request.session['logg']
    auth.logout(request)
    if 'logg' in request.session:
        del request.session['logg']
        return redirect('home')
    return redirect('home')

def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('home')
        x = datetime.datetime.now()
        z = x.strftime("%Y-%m-%d")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pnm = request.POST.get('pnm')
        psw = request.POST.get('psw')
        qual = request.POST.get('qualification')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        admin = request.POST.get('adminn1')
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.Email == email:
                messages.success(request, 'User already exists')
                return render(request, 'register_admin.html')
        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'register_admin.html')
        user = User.objects.create_user(username=user_name, email=email, password=psw)
        user.save()
        t = Registration()
        t.First_name = first_name
        t.Last_name = last_name
        t.Email = email
        t.Image = photo
        t.Phone_number = pnm
        t.Password = psw
        t.Registration_date = z
        t.Qualification = qual
        t.User_role = admin
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('home')
    else:
        return render(request, 'register_admin.html')

def bnb(request):
    bb1 = Registration.objects.get(User_role='admin')
    um = User.objects.get(email=bb1.Email)
    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        em = request.POST.get('em')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        m = User.objects.all().exclude(username = um.username)
        for t in m:
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return render(request, 'update_admin.html',{'bb1':bb1,'um':um})
        passwor = make_password(psw)
        df = Registration.objects.get(id=request.session['logg'])
        kmk = df.user.pk
        kmk = User.objects.get(id=kmk)
        kmk.username = user_name
        kmk.password = passwor
        kmk.email = em
        kmk.save()
        user = auth.authenticate(username = user_name, password = psw)
        auth.login(request,user)
        dcd = Registration.objects.get(User_role = 'admin')
        dcd.Email = em
        dcd.Password = psw
        dcd.First_name = first
        dcd.Last_name = last
        dcd.user = kmk
        dcd.save()
        b = Registration.objects.get(User_role='admin')
        m = int(b.id)
        request.session['logg'] = m
        gtt = Registration.objects.filter(User_role='admin')
        messages.success(request, 'You have successfully updated your profile')
        return render(request, 'adm_prof.html', {'gtt': gtt})
    else:
        return render(request, 'admin_home.html')

def del_admin(request, id):
    bb1 = Registration.objects.get(id = id)
    User.objects.get(email = bb1.Email).delete()
    messages.success(request, 'You have successfully resigned from administration')
    return redirect('home')

def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            return render(request, 'login.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, Password = password).exists():
            logs = Registration.objects.filter(user = user, Password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return render(request, 'login.html')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def expenses_home(request):
   dd = Expenses.objects.filter(Exp_reg = request.session['logg'])
   a = []
   b = []
   c = []
   d = []
   e = []
   f = []
   g = []
   h = []
   for i in dd:
       if i.Grocery not in b:
           a.append(i.Grocery)
           b.append(i.Sl_No)
           c.append(i.Marriage_Expenses)
           d.append(i.Electricity_Charge)
           e.append(i.Water_Charge)
           f.append(i.Govt_Service_Charges)
           g.append(i.Other_Expenses)
           h.append(i.id)
   hh = zip(a,b,c,d,e,f,g,h)
   return render(request,'exp_home.html',{'hh':hh})

def income_home(request):
   di = Income.objects.filter(Inc_reg = request.session['logg'])
   a = []
   b = []
   c = []
   d = []
   e = []
   f = []
   for i in di:
       if i.Salary not in b:
           a.append(i.Salary)
           b.append(i.Sl_No)
           c.append(i.Mutual_Funds)
           d.append(i.Tuition)
           e.append(i.Total_Income)
           f.append(i.id)
   phh = zip(a,b,c,d,e,f)
   return render(request,'inc.html',{'phh':phh})

def edit_expenses(request, id, idd, idm):
    idm = int(idm)
    id = str(id)
    idd = str(idd)
    gh = Expenses.objects.get(id = idm)
    ddr = Expenses.objects.filter(Exp_reg = request.session['logg'], Sl_No = id, Grocery = idd)
    if request.method == 'POST':
        enum = request.POST.get('enum')
        nam = request.POST.get('nam')
        dsn = request.POST.get('dsn')
        bre = request.POST.get('bre')
        adds = request.POST.get('adds')
        mn = request.POST.get('mn')
        tr = request.POST.get('tr')
        for w in ddr:
            w.Sl_No = enum
            w.Grocery= nam
            w.Marriage_Expenses = dsn
            w.Electricity_Charge = adds
            w.Water_Charge = bre
            w.Govt_Service_Charges = mn
            w.Other_Expenses = tr
            w.save()
        dd = Expenses.objects.filter(Exp_reg = request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Grocery not in a:
                a.append(i.Grocery)
                b.append(i.Sl_No)
                c.append(i.Marriage_Expenses)
                d.append(i.Electricity_Charge)
                e.append(i.Water_Charge)
                f.append(i.Govt_Service_Charges)
                g.append(i.Other_Expenses)
                h.append(i.id)
        hh = zip(a, b, c, d, e, f,g, h)
        messages.success(request, ' Edited Successfully')
        return render(request, 'exp_home.html', {'hh': hh})
    return render(request,'edit_expenses.html',{'gh':gh})

def edit_income(request, id, idd, idm):
    idm = int(idm)
    id = int(id)
    idd = float(idd)
    gh = Income.objects.get(id = idm)
    ddr = Income.objects.filter(Inc_reg = request.session['logg'], Sl_No = id, Salary = idd)
    if request.method == 'POST':
        enumm = request.POST.get('enumm')
        namm = request.POST.get('namm')
        dsnn = request.POST.get('dsnn')
        bree = request.POST.get('bree')
        addss = request.POST.get('addss')
        for w in ddr:
            w.Sl_No = enumm
            w.Salary= namm
            w.Mutual_Funds = dsnn
            w.Tuition = bree
            w.Total_Income = addss
            w.save()
        dd = Income.objects.filter(Inc_reg = request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        for i in dd:
            if i.Salary not in a:
                a.append(i.Salary)
                b.append(i.Sl_No)
                c.append(i.Mutual_Funds)
                d.append(i.Tuition)
                e.append(i.Total_Income)
                f.append(i.id)
        hh = zip(a, b, c, d, e, f)
        messages.success(request, ' Edited Successfully')
        return render(request, 'inc.html', {'hh': hh})
    return render(request,'edit_income.html',{'gh':gh})

def delete_expenses(request, id, idd, idm):
    id = str(id)
    idd = str(idd)
    dd = Expenses.objects.filter(Exp_reg=request.session['logg'])
    Expenses.objects.filter(Exp_reg=request.session['logg'], Sl_No=id, Grocery=idd).delete()
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    for i in dd:
        if i.Grocery not in a:
            a.append(i.Grocery)
            b.append(i.Sl_No)
            c.append(i.Marriage_Expenses)
            d.append(i.Electricity_Charge)
            e.append(i.Water_Charge)
            f.append(i.Govt_Service_Charges)
            g.append(i.Other_Expenses)
            h.append(i.id)
    hh = zip(a, b, c, d, e,f,g,  h)
    messages.success(request, 'Deleted Successfully')
    return render(request, 'exp_home.html', {'hh': hh})

def delete_savingss(request, id, idd, idm):
    id = str(id)
    idd = str(idd)
    dd = Savingss.objects.filter(Sav_reg=request.session['logg'])
    Savingss.objects.filter(Sav_reg=request.session['logg'], Sl_No=id, Month=idd).delete()
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    for i in dd:
        if i.Month not in a:
            a.append(i.Month)
            b.append(i.Sl_No)
            c.append(i.Bonus)
            d.append(i.Total_Income)
            e.append(i.Total_Expenses)
            f.append(i.Savings)
            g.append(i.id)
    hh = zip(a, b, c, d, e,f, g)
    messages.success(request, 'Deleted Successfully')
    return render(request, 'savingsss.html', {'hh': hh})


def delete_income(request, id, idd, idm):
    id = str(id)
    idd = str(idd)
    dd = Income.objects.filter(Inc_reg=request.session['logg'])
    Income.objects.filter(Inc_reg=request.session['logg'], Sl_No=id, Salary=idd).delete()
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    for i in dd:
        if i.Salary not in a:
            a.append(i.Salary)
            b.append(i.Sl_No)
            c.append(i.Mutual_Funds)
            d.append(i.Tuition)
            e.append(i.Total_Income)
            f.append(i.id)
    hh = zip(a, b, c, d, e,f )
    messages.success(request, 'Deleted Successfully')
    return render(request, 'inc.html', {'hh': hh})


def add_expenses(request):
    if request.method == 'POST':
        slp = request.POST.get('slp')
        grp = request.POST.get('grp')
        rt = Expenses.objects.filter(Exp_reg = request.session['logg'])
        for u in rt:
            for t in rt:
                if t.Sl_No == 'sl_no':
                    messages.success(request, 'You are not allowed to be registered as admin')
                    return redirect('home')
            if u.Sl_No == slp and u.Grocery == grp:
                dd = Expenses.objects.filter(Exp_reg = request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                h = []
                for i in dd:
                    if i.Grocery not in a:
                        a.append(i.Grocery)
                        b.append(i.Sl_No)
                        c.append(i.Marriage_Expenses)
                        d.append(i.Electricity_Charge)
                        e.append(i.Water_Charge)
                        f.append(i.Govt_Service_Charges)
                        g.append(i.Other_Expenses)
                        h.append(i.id)
                hh = zip(a, b, c, d, e, f,g , h)
                messages.success(request, 'Expense Details already exists')
                return render(request, 'exp_home.html', {'hh': hh})
        mop = request.POST.get('mop')
        elp = request.POST.get('elp')
        wap = request.POST.get('wap')
        sap = request.POST.get('sap')
        to = request.POST.get('to')
        pk = Registration.objects.get(id = request.session['logg'])
        cdt = Expenses()
        cdt.Sl_No = slp
        cdt.Grocery = grp
        cdt.Marriage_Expenses = mop
        cdt.Electricity_Charge = elp
        cdt.Water_Charge = wap
        cdt.Govt_Service_Charges = sap
        cdt.Other_Expenses = to
        cdt.Exp_reg = pk
        cdt.save()
        dd = Expenses.objects.filter(Exp_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        for i in dd:
            if i.Grocery not in a:
                a.append(i.Grocery)
                b.append(i.Sl_No)
                c.append(i.Marriage_Expenses)
                d.append(i.Electricity_Charge)
                e.append(i.Water_Charge)
                f.append(i.Govt_Service_Charges)
                g.append(i.Other_Expenses)
                h.append(i.id)
        hh = zip(a, b, c, d, e,f,g,  h)
        messages.success(request, 'Added  successfully')
        return render(request, 'exp_home.html', {'hh': hh})
    return render(request,'add_expenses.html')

def add_income(request):
    if request.method == 'POST':
        sz = request.POST.get('sz')
        snz = request.POST.get('snz')
        rt = Income.objects.filter(Inc_reg = request.session['logg'])
        for u in rt:
            for t in rt:
                if t.Sl_No == 'sl_no':
                    messages.success(request, 'You are not allowed to be registered as admin')
                    return redirect('home')
            if u.Sl_No == sz and u.Salary == snz:
                dd = Income.objects.filter(Inc_reg = request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                for i in dd:
                    if i.Salary not in a:
                        a.append(i.Salary)
                        b.append(i.Sl_No)
                        c.append(i.Mutual_Funds)
                        d.append(i.Tuition)
                        e.append(i.Total_Income)
                        f.append(i.id)
                hh = zip(a, b, c, d, e,f )
                messages.success(request, 'Income Details already exists')
                return render(request, 'inc.html', {'hh': hh})
        snz = request.POST.get('snz')
        mz = request.POST.get('mz')
        tz = request.POST.get('tz')
        tq = request.POST.get('tq')
        pk = Registration.objects.get(id = request.session['logg'])
        ckp = Income()
        ckp.Sl_No = sz
        ckp.Salary = snz
        ckp.Mutual_Funds = mz
        ckp.Tuition = tz
        ckp.Total_Income = tq
        ckp.Inc_reg = pk
        ckp.save()
        dd = Income.objects.filter(Inc_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        for i in dd:
            if i.Salary not in a:
                a.append(i.Salary)
                b.append(i.Sl_No)
                c.append(i.Mutual_Funds)
                d.append(i.Tuition)
                e.append(i.Total_Income)
                f.append(i.id)
        hh = zip(a, b, c, d, e,f)
        messages.success(request, 'Added Successfully')
        return render(request, 'inc.html', {'hh': hh})
    return render(request,'add_income.html')

def list(request):
    return render(request, 'list.html',)

def savingsss_home(request):
   aa = Savingss.objects.filter(Sav_reg = request.session['logg'])
   a = []
   b = []
   c = []
   d = []
   e = []
   f = []
   g = []
   for i in aa:
       if i.Month not in b:
           a.append(i.Month)
           b.append(i.Sl_No)
           c.append(i.Bonus)
           d.append(i.Total_Income)
           e.append(i.Total_Expenses)
           f.append(i.Savings)
           g.append(i.id)
   hh = zip(a,b,c,d,e,f,g)
   return render(request,'Savingsss.html',{'hh':hh})

def add_savingss(request):
    if request.method == 'POST':
        qw = request.POST.get('qw')
        we = request.POST.get('we')
        rtt = Savingss.objects.filter(Sav_reg = request.session['logg'])
        for u in rtt:
            for t in rtt:
                if t.Sl_No == 'sl_no':
                    messages.success(request, 'You are not allowed to be registered as admin')
                    return redirect('home')
            if u.Sl_No == qw and u.Month == we:
                ddd = Savingss.objects.filter(Sav_reg = request.session['logg'])
                a = []
                b = []
                c = []
                d = []
                e = []
                f = []
                g = []
                for i in ddd:
                    if i.Month not in a:
                        a.append(i.Month)
                        b.append(i.Sl_No)
                        c.append(i.Bonus)
                        d.append(i.Total_Income)
                        e.append(i.Total_Expenses)
                        f.append(i.Savings)
                hh = zip(a, b, c, d, e, f, g)
                messages.success(request, ' Details already exists')
                return render(request, 'savingsss.html', {'hh': hh})
        er = request.POST.get('er')
        rt = request.POST.get('rt')
        ty = request.POST.get('ty')
        yu = request.POST.get('yu')
        pkp = Registration.objects.get(id = request.session['logg'])
        cdt = Savingss()
        cdt.Sl_No = qw
        cdt.Month = we
        cdt.Bonus = er
        cdt.Total_Income= rt
        cdt.Total_Expenses = ty
        cdt.Savings = yu
        cdt.Sav_reg = pkp
        cdt.save()
        ddp = Savingss.objects.filter(Sav_reg=request.session['logg'])
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        for i in ddp:
            if i.Month not in a:
                a.append(i.Month)
                b.append(i.Sl_No)
                c.append(i.Bonus)
                d.append(i.Total_Income)
                e.append(i.Total_Expenses)
                f.append(i.Savings)
                g.append(i.id)
        hh = zip(a, b, c, d, e,f, g)
        messages.success(request, 'Added  successfully')
        return render(request, 'savingsss.html', {'hh':hh })
    return render(request,'add_savingsss.html')

def graph(request):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='hbms')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    x = cursor.execute("SELECT `Month`,`Total_Expenses`,`Total_Income`  FROM `pathss_savingss`")
    rows = cursor.fetchall()
    plt.bar(x, height=x,  width=0.2)
    figure, ax = plt.subplots()
    plt.bar([x['Month'] for x in rows], [y['Total_Expenses'] for y in rows] ,label='Total_Expenses')
    plt.bar([x['Month'] for x in rows], [y['Total_Income'] for y in rows] ,label='Total_Income')
    plt.xlabel('Month ')
    plt.ylabel('Budget ')
    plt.title("Home Budget Planning System")
    ax.legend()
    figure.tight_layout()
    plt.show()
    plt.close()
    return render(request, 'admin_home.html',)


def rough(request):
    return render(request, 'check.html', )