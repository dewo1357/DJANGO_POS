from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import django.contrib.messages as messages
from .forms import UserForm,SignUpForm
from django.conf import settings
from .models import database,orderss6,tablee6,numbertable3,history,temp,report_table,transaction_done,master,kumpulan_cashier,kumpulan_table,penjualan,pendaftar
from django.http import HttpResponse
from django.template import loader
from datetime import datetime as dt
from datetime import date as date
from django.http import FileResponse
import io
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
import numpy as np

# Create your views here.

@csrf_exempt
def welcome(request):
    if request.method == 'GET':
            if request.user.is_authenticated:
                return redirect('/')
            else:
                user = UserForm()
                return render(request,"welcome.html",{'form':user})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/',{'form':user})
        else:
            messages.error(request,"PASSWORD/USERNAME SALAH!")
                
    return redirect(request.META.get("HTTP_REFERER","/"))

@login_required(login_url=settings.URL_LOGIN)
def sign_out(request):
   if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            print("proses keluar")
            return redirect('login')
    

@csrf_exempt
def sign_up(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request,"registration.html",{'form':form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"AKUN BERHASIL DI DAFTAR, SILAHKAN LOGIN")
            return redirect('/question')
        else:
            messages.error(request,"GAGAL MENDAFTAR AKUN")
    return render(request,"registration.html")


def question(request):
    if request.method == 'GET':
        return render(request,'ask.html')

@csrf_exempt
def post_question(request):
    if request.method == 'POST':
        nama_usaha = request.POST['nama_pengusaha']
        nama_toko = request.POST['nama_usaha']
        Alamat = request.POST['alamat']
        jumlah_employe = request.POST['jumlah_anggota']
        skala = request.POST['skala_usaha']
        no_whatssapp = request.POST['nomor_whatssapp']
        data = pendaftar(nama_usaha=nama_usaha, nama_toko=nama_toko,
                         alamat=Alamat,Jumlah_anggota=jumlah_employe,
                         skala=skala,whatssapp=no_whatssapp)
        data.save()
        return redirect('/registration')

@login_required(login_url=settings.URL_LOGIN)
def finished(request):
    if request.method == 'GET':
       
        data2=temp.objects.all().values()
        data_table = tablee6.objects.all()
        table_num = numbertable3.objects.all().values()
        keluar = temp.objects.filter(no_user=request.user.id)

        numbers = []
        for i in table_num:
            numbers.append(i['number_table'])  

        data2 = []
        for table_filter in data2:
           data2.append(table_filter['no_table_id'])
        date = dt.now()
        second = date.second
        years = date.year

        search = request.GET.get('cari_menu')
        data= database.objects.filter(no_user=request.user.id)
        if search:
            data = database.objects.filter(nama_barang__icontains=search,no_user=request.User.id)
        context = {
            'data' : data,
            'out' : data2,
            'second' : second,
            'years' : years,
            'table' : data_table,
            'number' : table_num,
            'keluar' : keluar
        }
        return render(request,'page1.html',context=context)

@login_required(login_url=settings.URL_LOGIN)
def finished2(request):
    if request.method == 'GET':
        data2=orderss6.objects.all().values()
        data_table = tablee6.objects.all()
        table_num = history.objects.all().values()
        keluar = temp.objects.filter(no_user=request.user.id)

        
        date = dt.now()
        second = date.second
        years = date.year

        search = request.GET.get('cari_menu')
        data= database.objects.filter(no_user=request.user.id)
        if search:
            data = database.objects.filter(nama_barang__icontains=search,no_user=request.User.id)
        context = {
            'data' : data,
            'out' : data2,
            'second' : second,
            'years' : years,
            'table' : data_table,
            'number' : table_num,
            'keluar' : keluar,
        }
        return render(request,'page8.html',context=context)
    

@login_required(login_url=settings.URL_LOGIN)
@csrf_exempt
def process(request,kode_id):
    
    if request.method == 'GET':
        try:
            data1 = database.objects.get(kode_id=kode_id)
            data = orderss6.objects.all().values()
            data_table = tablee6.objects.all()
            table_num = numbertable3.objects.all().values()
            keluar = temp.objects.filter(no_user=request.user.id)
            numbers = []
            for i in table_num:
                numbers.append(i['number_table'])  
                        
            data = {}
            for table_filter in data:
                if table_filter in numbers['no_table']:
                    data.update(table_filter)

            date = dt.now()
            second = date.second
            years = date.year
            context = {
                'data1' : data1,
                'out' : data,
                'second' : second,
                'years' : years,
                'table' : data_table,
                'number' : numbers[-1],
                'keluar' : keluar,
            }
            return render(request,'page2.html',context=context)
        
        except IndexError as e:
            redirect('/finished')

@csrf_exempt
def proses_post(request):
    if request.method == 'POST':
        try:
            transaction_id = request.POST['transaction_id']
            kode_barang = request.POST['kode_barang']
            no_table_id = request.POST['number_table']
            tanggal = date.today()
            tanggal = tanggal.strftime('%Y-%m-%d')
            nama_barang = request.POST['nama_barang']
            harga_jual = request.POST['harga_jual']
            quantity = int(request.POST['quantity'])
            no_user = request.user.id
            total_harga = int(quantity) * int(harga_jual)
            is_complete = False


            if quantity >= 1:
                data = orderss6(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                        tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                        quantity=quantity,total_harga=total_harga,is_complete=is_complete,no_user=no_user)
            
                sementara = temp(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                            tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                            quantity=quantity,total_harga=total_harga,is_complete=is_complete,no_user=no_user)
                
                orders = penjualan(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                            tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                            quantity=quantity,total_harga=total_harga,no_user=no_user)
                barang = database.objects.get(kode_id=kode_barang,no_user=request.user.id)
                barang.out_barang = barang.out_barang + quantity
                barang.tersisa = barang.tersisa - quantity
                if barang.tersisa >= 0:
                    barang.save()
                    sementara.save()
                    data.save() 
                    orders.save() 
                    return redirect('/finished')
                else:
                    messages.error(request,"Stok Tersisa Tidak Mencukupi")
                    print(barang.tersisa)
                    return redirect(request.META.get("HTTP_REFERER","/"))
            else :
                messages.error(request,"Quantity Tidak Boleh Kurang Dari 1.")
                return redirect(request.META.get("HTTP_REFERER","/"))
        except ValueError as e:
            return redirect(request.META.get("HTTP_REFERER","/"))

def proses_post2(request):
    if request.method == 'POST':
        try:
            transaction_id = request.POST['transaction_id']
            kode_barang = request.POST['kode_barang']
            no_table_id = request.POST['number_table']
            tanggal = date.today()
            tanggal = tanggal.strftime('%Y-%m-%d')
            nama_barang = request.POST['nama_barang']
            harga_jual = request.POST['harga_jual']
            quantity = int(request.POST['quantity'])
            no_user = request.user.id
            total_harga = int(quantity) * int(harga_jual)
            is_complete = False


            if quantity >= 1:
                data = orderss6(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                        tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                        quantity=quantity,total_harga=total_harga,is_complete=is_complete,no_user=no_user)
            
                sementara = temp(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                            tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                            quantity=quantity,total_harga=total_harga,is_complete=is_complete,no_user=no_user)
                
                orders = penjualan(transaction_id=transaction_id,kode_barang=kode_barang,no_table=no_table_id,
                            tanggal=tanggal,nama_barang=nama_barang,harga_jual=harga_jual,
                            quantity=quantity,total_harga=total_harga,no_user=no_user)
                barang = database.objects.get(kode_id=kode_barang,no_user=request.user.id)
                barang.out_barang = barang.out_barang + quantity
                barang.tersisa = barang.tersisa - quantity
                if barang.tersisa >= 0:
                    barang.save()
                    sementara.save()
                    data.save() 
                    orders.save() 
                    return redirect('/order_table')
                else:
                    messages.error(request,"Stok Tersisa Tidak Mencukupi")
                    print(barang.tersisa)
                    return redirect(request.META.get("HTTP_REFERER","/"))
            else :
                messages.error(request,"Quantity Tidak Boleh Kurang Dari 1.")
                return redirect(request.META.get("HTTP_REFERER","/"))
        except ValueError as e:
            return redirect(request.META.get("HTTP_REFERER","/"))
    
def process2(request,kode_id):    
    if request.method == 'GET':
        data1 = database.objects.get(kode_id=kode_id)
        data = orderss6.objects.all().values()
        data_table = tablee6.objects.all()
        table_num = history.objects.all().values()
        keluar = temp.objects.filter(no_user=request.user.id)
        number = []
        for i in table_num:
            number.append(i['history'])   
        date = dt.now()
        second = date.second
        years = date.year
        context = {
            'data1' : data1,
            'out' : data,
            'second' : second,
            'years' : years,
            'table' : data_table,
            'number' : number[-1],
            'keluar' : keluar
        }
        return render(request,'page22.html',context=context)
        
@login_required(login_url=settings.URL_LOGIN)
def list_table(request):
    if request.method == 'GET':
        
        count = 1
        message = "Choose Table"

        if count == 1:
            message = "Choose Table"
        else:
            message = "Table Sudah Tersedia"
        try:
            table = orderss6.objects.filter(no_user=request.user.id)
            order = tablee6.objects.filter(no_user=request.user.id)
            table_num = numbertable3.objects.all()
            
            cashier = kumpulan_cashier.objects.all()
            meja = kumpulan_table.objects.all()
            context = {
                'orders' : order,
                'table' : table,
                'number' : table_num,
                'message' : message,
                'cashier' : cashier,
                'meja' : meja, 
            }
            
            return render(request,'page3.html',context=context)
        
        except IndexError:
            numbers = []
            for i in table:
                if i != None:
                    numbers.append(i.no_table_id)
                else:
                    tablee6.objects.get(no_table=table_num).delete()

        
        

@csrf_exempt
def post_list_table(request):
    if request.method=='POST':
        try:
            table = orderss6.objects.all().values()
            order = tablee6.objects.filter(no_user=request.user.id)
            meja = kumpulan_table.objects.all()
            cashier = kumpulan_cashier.objects.all()

            table_num = request.POST['number_table']
            cashier_name = request.POST['cashier_name']
            if numbertable3.objects.filter(number_table=table_num,no_user=request.user.id).exists():
                print(request.user.id)
                count = 0
                count += 1
                message = "Choose Table"
                if count == 0:
                    message = "Choose Table"
                else:
                    message = "Table Sudah Tersedia"

                context = {
                    'orders' : order,
                    'table' : table,
                    'number' : table_num,
                    'message' : message,
                    'meja' : meja,
                    'cashier' : cashier,
                    
                }
                return render(request,'page3.html',context=context)         
            else:
                table_num = request.POST['number_table']
                cashier_name = request.POST['cashier_name']
                table = orderss6.objects.all()
                order = tablee6.objects.all()
                number_table = numbertable3(number_table=table_num,cashier_name=cashier_name,no_user=request.user.id)
                table_number = tablee6(no_table=table_num,nomor_meja=table_num,no_user=request.user.id)
                number_table.save()
                table_number.save()                   
                context = {
                    'orders' : order,
                    'table' : table,
                    'number' : table_num,
                }
                return redirect('/finished',context=context)     
        except ValueError:
            return redirect(request.META.get("HTTP_REFERER","/"))


           

@csrf_exempt    
def list_orders(request,no_table_id):
        if request.method=='GET':
            try:
                data = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
                data1 = history.objects.all()
                data3 = report_table.objects.all().values()
                date = dt.now()
                transaction = []

                for i in data3:
                    transaction.append(i['transaction_id'])
                total_amount = 0

                if data is None:
                    for i in data:
                        total_amount += i.total_harga
                    context = {
                        'orders' : data,
                        'numbers' : data.no_table_id,
                        'total_harga' : total_amount,
                        'info' : data.transaction_id,
                        'tanggal' : date    
                        }
                        
                    return render(request,'page4.html',context=context)
                else:
                    data = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
                    data3 = report_table.objects.all().values()
                    nomor = numbertable3.objects.filter(number_table=no_table_id)
                    time = dt.now()
                    second = time.second
                    transaction = 1324214647
                    table = []
                    for i in data:
                        if no_table_id != i.no_table:
                            total_amount += i.total_harga
                            table.append(i.no_table)
                            

                    for i in nomor:
                        if no_table_id != i.number_table:
                            table.append(i.number_table)
                
                                               

                context = {
                    'orders' : data,
                    'numbers' : table[-1],
                    'total_harga' : total_amount,
                    'info' : transaction,
                    'time' : second,
                    'tanggal' : date    
                    }
                return render(request,'page4.html',context=context)
            except IndexError:
                data = orderss6.objects.filter(no_table_id=no_table_id)
                data1 = history.objects.all()
                data3 = report_table.objects.filter(no_table_id=no_table_id)
                date = dt.now()
                total_amount = 0

                transaction_id=[]
                numbers = []
                for i in data:
                    numbers.append(i.no_table_id)
                    total_amount += i.total_harga
                    transaction_id.append(i.transaction_id)
                context = {
                    'orders' : data,
                    'numbers' : numbers[-1],
                    'total_harga' : total_amount,
                    'info' : transaction_id[-1],
                    'tanggal' : date,             
                }
                return render(request,'page4.html',context=context)
        elif request.method == 'POST':
            data = history.objects.all()
            data1 = request.POST['nomor_table']
            data = history(history=data1)
            data.save()
            return redirect('/order_table')
        
        
@csrf_exempt       
def finishpay(request,no_table_id):
    orders = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
    detail = master.objects.filter(no_table=no_table_id)


    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']
        no_table = request.POST['nomor_table']
        tanggal = dt.now()
        total_amount = request.POST['total_harga']
        pembayaran = request.POST['pembayaran']
        pay=int(request.POST['pembayaran'])
        discount = request.POST['Discount']
        total_harga = 0
        harga = []
        amount = []
        nama_product = []
        quantity = []
        ukuran = 0
        for i in orders:
            total_harga += i.total_harga
            nama_product.append(i.nama_barang)
            quantity.append(i.quantity)
            harga.append(i.harga_jual)
            amount.append(i.total_harga)
            ukuran += 50
        
        total_amount =  int(total_harga) - (int(total_harga) * float(discount))
        total_amount = int(total_amount)
        if pay >= total_amount or pay == total_amount :
            kembalian = int(pay) - int(total_amount)
            print(pay)
            data = transaction_done(transaction_id=transaction_id,no_table=no_table,
                                tanggal=tanggal,total_amount=total_amount,
                                pay=pembayaran,kembalian=kembalian)        
            data2 = master(transaction_id=transaction_id,no_table=no_table,
                        tanggal=tanggal,total_amount=total_amount,discount=discount,
                        pay=pembayaran,kembalian=kembalian)
            context = {
                'orders' : orders,
                'detail' : detail,
                
            }

            data.save()
            data2.save()

            return render(request,'page9.html',context=context)

            
        else:
            return redirect(request.META.get("HTTP_REFERER","/"))
        
    

def print_receipt(request,no_table_id):
    orders = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
    detail = master.objects.get(no_table=no_table_id)
    total_harga = 0
    harga = []
    amount = []
    nama_product = []
    quantity = []
    ukuran = 400
    for i in orders:
        total_harga += i.total_harga
        nama_product.append(i.nama_barang)
        quantity.append(i.quantity)
        harga.append(i.harga_jual)
        amount.append(i.total_harga)
        ukuran += 10    

    buf = io.BytesIO()
            
    #prinr_receipt
    width = 250
    heigth = ukuran
    custom_size = (width,heigth)
    c = canvas.Canvas(buf, pagesize=custom_size,bottomup=0)
    
    #Header
    c.setFont('Helvetica-Bold',40)
    c.drawString(40,50,"mariPOS")

    tanggal = dt.today()
    tahun = tanggal.year
    c.setFont('Helvetica',8)
    c.drawString(35,70,f"{tanggal} | {detail.transaction_id}{tahun} |")

            
    c.setFont('Helvetica-Bold',9)
    c.drawString(13,90,"Nama & Harga                                  |  Qty  | Total Harga")

    #create Text
    c.setFont('Helvetica',10)
    height = 80
    count = 30
    for i in nama_product:
        height += count
        c.drawString(13,height,f"-{i}")

    height = 90
    for i in harga:
        height += count
        c.drawString(20,height,f"Rp.{i}")

    height = 90
    for i in quantity:
        height += count
        c.drawString(170,height,f"x{i}")

    height = 90
    for i in amount:
        height += count
        c.drawString(190,height,f"Rp.{i}")
            
    c.setFont('Helvetica-Bold',25)
    c.drawString(13,height+33,f"Total   :  Rp.{detail.total_amount}")
    c.setFont('Helvetica-Bold',10)
    c.drawString(125,height+52,f"Dibayar        :  Rp.{detail.pay}")
    discount = int(detail.discount * 100)
    c.drawString(125,height+67,f"Discount      :  {discount}%")
    c.drawString(125,height+82,f"Kembalian   :  Rp.{detail.kembalian}")
    c.setFont('Helvetica-Bold',10)
    c.drawString(40,height+110,"Terima Kasih Atas Kunjungan nya :)")
        
    #finish_up
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report.pdf')

      

def information(request,no_table_id):
    orders = orderss6.objects.filter(no_table_id=no_table_id)
    context = {
        'orders' : orders,
    }   
    return render(request,'page9.html',context=context)

def execute(request):
    try:
        data1 = temp.objects.filter(no_user=request.user.id).values()
        total = 0
        transaction_id1 = []
        numbertable = []
        tanggal = []
        qty = 0
        for i in data1:
            transaction_id1.append(i['transaction_id'])
            numbertable.append(i['no_table'])
            tanggal.append(i['tanggal'])
            total += i['total_harga']
            qty += i['quantity']  
        transaction_id = transaction_id1[-1]
        no_table_id = numbertable[-1]
        date = tanggal[-1]
        sementara = report_table(transaction_id=transaction_id,no_table=no_table_id,
                        tanggal=date,total_amount=total,quantity=qty,no_user=request.user.id)       
        sementara.save()
        temp.objects.filter(no_user=request.user.id).delete()
        return redirect('/')   
    except IndexError:
        messages.error(request,"KLIK TOMBOL ADD DAHULU UNTUK PROSES PESANAN ANDA!")
        return redirect(request.META.get("HTTP_REFERER","/"))
   

def executecancel(request):
    temp.objects.all().delete()
    data = tablee6.objects.all().values()
    numbers = []
    no_user = []
    for i in data:
        numbers.append(i['no_table'])  
        no_user.append(i['no_user'])
    tablee6.objects.filter(nomor_meja=numbers[-1],no_user=request.user.id).delete()
    numbertable3.objects.filter(number_table=numbers[-1],no_user=request.user.id).delete()
    return redirect('/')

def settings(request,transaction_id):
    orders = orderss6.objects.get(transaction_id=transaction_id)
    meja = kumpulan_table.objects.all()
    context = {
        'orders' : orders,
        'meja' : meja,
    }
    return render(request,'settings.html',context=context)

@csrf_exempt
def process_settings(request,transaction_id):
    data = orderss6.objects.get(transaction_id=transaction_id,no_user=request.user.id)
    meja = tablee6.objects.all().values()
    table = request.POST['no_table_id']

    kumpulan = []
    for i in meja:
        kumpulan.append(i['no_table'])

    if table in kumpulan:
        pass
    else:
        daftar = tablee6(no_table=table,nomor_meja=table,no_user=request.user.id)
        daftar.save()

    data.no_table = table
    data.save()
    return redirect('/')

def deleteitems(request,transaction_id):
    temp.objects.get(transaction_id=transaction_id).delete()
    orderss6.objects.get(transaction_id=transaction_id).delete()
    return redirect(request.META.get("HTTP_REFERER","/"))

@login_required
def read(request):
    if request.method == 'GET':
        data = database.objects.all().values()
        return render(request,'read.html',{'data':data})

@login_required
@csrf_exempt   
def tambah(request):
    if request.method == 'GET':
        waktu = dt.today()
        detik = waktu.second
        tahun = waktu.year
        random = np.random.randint(1000)
        template = loader.get_template("tambah.html")
        data = database.objects.all()
        context={
            'waktu':detik,
            'tahun':tahun,
            'random':random
        }
        return HttpResponse(template.render(context,request))
    if request.method == 'POST':
        data = database.objects.all()
        kode_id = request.POST['kode_id']
        nama_barang = request.POST['nama_barang']
        jenis = request.POST['jenis']
        outlet = request.POST['outlet']
        harga_modal = request.POST['harga_modal']
        harga_jual = request.POST['harga_jual']
        quantity = request.POST['quantity']
        sum_of_modal = int(harga_modal) * int(quantity)
        sum_of_jual = int(harga_jual) * int(quantity)
        income_unit = int(harga_jual) - int(harga_modal)
        sum_of_income = int(income_unit) * int(quantity)
        tersisa = quantity
        no_user = request.user.id
        if database.objects.filter(kode_id=kode_id).exists():
            return redirect('tambah')
        else:
            data = database(
                        kode_id=kode_id,nama_barang=nama_barang,
                        jenis=jenis,outlet=outlet,harga_modal=harga_modal,
                        harga_jual=harga_jual,
                        quantity=quantity,sum_of_modal=sum_of_modal,
                        sum_of_jual=sum_of_jual,income_unit=income_unit,
                        sum_of_income=sum_of_income,no_user=no_user,tersisa=tersisa
                        )
            print(no_user)
            data.save()
    return redirect(request.META.get("HTTP_REFERER","/"))


@login_required
@csrf_exempt
def edit(request,kode_id):
    if request.method=='GET':
        
        data = database.objects.get(kode_id=kode_id)
        context = {
            'data' : data
        }
        return render(request,"edit.html",context)
    else :
        kode_id = request.POST['kode_id']
        nama_barang = request.POST['nama_barang']
        jenis = request.POST['jenis']
        outlet = request.POST['outlet']
        harga_modal = request.POST['harga_modal']
        harga_jual = request.POST['harga_jual']
        quantity = request.POST['quantity']
        sum_of_modal = int(harga_modal) * int(quantity)
        sum_of_jual = int(harga_jual) * int(quantity)
        income_unit = int(harga_jual) * int(harga_modal)
        sum_of_income = int(income_unit) - int(quantity)
       
        data = database.objects.get(kode_id=kode_id)
        data.kode_id = kode_id
        data.nama_barang = nama_barang
        data.jenis = jenis
        data.outlet = outlet
        data.harga_modal = harga_modal
        data.harga_jual = harga_jual
        data.quantity = quantity
        data.tersisa = quantity
        data.sum_of_modal = sum_of_modal
        data.sum_of_jual = sum_of_jual
        data.sum_of_income = sum_of_income
        data.save()
        messages.success(request,"Data Berhasil Di Perbarui")
    return redirect(request.META.get("HTTP_REFERER","/"))

@login_required
def delete(request,kode_id):
    database.objects.get(kode_id=kode_id).delete()
    messages.success(request,"DATA BERHASIL DIHAPUS")
    return redirect(request.META.get("HTTP_REFERER","/"))


def overview(request):
    if request.method=='GET':
        return render(request,'overview.html')
    
def done(request):
    no_table_id = []
    data = transaction_done.objects.all().values()

    for i in data :
        no_table_id.append(i['no_table'])
    meja = tablee6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id)

    for i in meja:
        if no_table_id == meja:
            tablee6.objects.get(no_table=no_table_id[-1],no_user=request.user.id).delete()
        else:
            meja = tablee6(no_table=no_table_id[-1],no_user=request.user.id)
            meja.save()
            tablee6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id).delete()

    numbertable3.objects.filter(number_table=no_table_id[-1],no_user=request.user.id).delete()
    orderss6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id).delete()
    return redirect('/')


def overalsetting(request):
    data = database.objects.filter(no_user=request.user.id)
    context = {
        'data' : data
    }
    return render(request,'overalsettings.html',context=context)

def overalsetting1(request):
    meja = kumpulan_table.objects.all().values()
    context = {
        'meja' : meja
    }
    return render(request,'overalsettings1.html',context=context)

def overalsetting2(request):
    cashier = kumpulan_cashier.objects.all().values()
    context = {
        'cashier' : cashier
    }
    return render(request,'overalsettings2.html',context=context)

def tambah_meja(request):
    tambah_meja = request.POST['tambah_meja']
    meja = kumpulan_table(no_table=tambah_meja)
    if kumpulan_table.objects.filter(no_table=tambah_meja).exists():
        pass
    else:
        meja.save()
    return redirect(request.META.get("HTTP_REFERER","/"))

def tambah_cashier(request):
    cashier = request.POST['cashier']
    meja = kumpulan_cashier(name_cashier=cashier)
    if kumpulan_cashier.objects.filter(name_cashier=cashier).exists():
        pass
    else:
        meja.save()
    return redirect(request.META.get("HTTP_REFERER","/"))

def delete_cashier(request,id):
    kumpulan_cashier.objects.get(id=id).delete()
    return redirect(request.META.get("HTTP_REFERER","/"))

def refresh(request):
    return redirect(request.META.get("HTTP_REFERER","/"))

def report(request):
    sekarang = dt.today()
    data = penjualan.objects.filter(tanggal=sekarang,no_user=request.user.id).order_by('-tanggal')
    barang = database.objects.filter(no_user=request.user.id)
    revenue = 0
    quantity = 0
    count = 0
    for i in data:
        revenue += i.total_harga
        count += 1
        quantity += i.quantity
    context = {
        'data' : data,
        'sekarang' : sekarang,
        'revenue' : revenue,
        'count' : count,
        'quantity' : quantity,
        'nama_barang' : barang,
    }
    return render(request,'report.html',context=context)



def visualization(request):
    tanggal = request.GET.get('tanggal')
    nama_barang = request.GET.get('nama_barang')
    barang = database.objects.all()
    sekarang = dt.today()
    data = penjualan.objects.filter(tanggal=sekarang,no_user=request.user.id).order_by('-tanggal')
    revenue = 0
    quantity = 0
    count = 0
    
    if nama_barang: 
        data  = penjualan.objects.filter(nama_barang__icontains=nama_barang).order_by('-tanggal')
    if tanggal:
        data = penjualan.objects.filter(tanggal__icontains=tanggal)
    if nama_barang and tanggal:
        data  = penjualan.objects.filter(nama_barang__icontains=nama_barang,tanggal__icontains=tanggal)
    for i in data:
        revenue += i.total_harga
        count += 1
        quantity += i.quantity

    context = {
        'data' : data,
        'sekarang' : sekarang,
        'revenue' : revenue,
        'count' : count,
        'quantity' : quantity,
        'nama_barang' : barang,
        'hasil_input' : nama_barang,
        'tanggal' : tanggal,

    }
    return render(request,'report2.html',context=context)



