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
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
import numpy as np

# Create your views here.

#PROSES AUTENTIKASI
#********************************************************************************
#fitur function LOGIN
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
        user = authenticate(request,username=username,password=password)#PROSES AUTENTIKASI
        if user is not None: #proses validasi jika value dari variabel user apabila tidak ada
            login(request,user)#apabila tidak ada maka proses logn
            return redirect('/',{'form':user})#proses halaman awal(index)
        else: #apabila username & password salah
            messages.error(request,"PASSWORD/USERNAME SALAH!")#messages apabila password/username salah
                
    return redirect(request.META.get("HTTP_REFERER","/"))

#proses logout.
@login_required(login_url=settings.URL_LOGIN)
def sign_out(request):
   if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            print("proses keluar")
            return redirect('login')

#proses tampilan questioner sebelum masuk ke halaman daftar
def question(request):
    if request.method == 'GET':
        return render(request,'ask.html')

#proses ekseskusi questioner untuk mendapatkan informasi pendaftar
@csrf_exempt
def post_question(request):
    if request.method == 'POST':
        nama_usaha = request.POST['nama_pengusaha']
        nama_toko = request.POST['nama_usaha']
        Alamat = request.POST['alamat']
        jumlah_employe = request.POST['jumlah_anggota']
        skala = request.POST['skala_usaha']
        no_whatssapp = request.POST['nomor_whatssapp']
        #simpan ke dalam table pendaftar
        data = pendaftar(nama_usaha=nama_usaha, nama_toko=nama_toko,
                         alamat=Alamat,Jumlah_anggota=jumlah_employe,
                         skala=skala,whatssapp=no_whatssapp)
        data.save()
        return redirect('/registration')#menuju part registrasi.    

#proses daftar
#proses ini harus di lalui tahap questioner. agar tetap bisa mendapatkan informasi user yang mendafatar
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
            return redirect('/login')
        else:
            messages.error(request,"GAGAL MENDAFTAR AKUN")
    return render(request,"registration.html")

#AKHIR BARIS PROSES AUTENTIKASI
#************************************************************************************


#fitur proses katalog menu untuk memilih product untuk dipesan
@login_required(login_url=settings.URL_LOGIN)
def finished(request):
    if request.method == 'GET':
       
        data2=temp.objects.all().values()
        data_table = tablee6.objects.all()
        table_num = numbertable3.objects.all().values()
        keluar = temp.objects.filter(no_user=request.user.id) #variabel ini berfungsi mengambil value nomor meja terakhir bedasarkan id user

        #proses mengambil data terakhir dan di filter oleh id user untuk otomatis input ke dalam form input nomor meja
        #*****************************************
        numbers = []
        for i in table_num:
            numbers.append(i['number_table'])
        #******************************************

        #3 variabel ini difungsikan untuk kode setiap transaksi
        date = dt.now()
        second = date.second
        years = date.year
        #*******************************************************
        
        #fitur search pesanan
        search = request.GET.get('cari_menu')
        data= database.objects.filter(no_user=request.user.id)
        if search:
            data = database.objects.filter(nama_barang__icontains=search,no_user=request.User.id)
        #****************************************************************************************
        context = {
            'data' : data,
            'second' : second,
            'years' : years,
            'table' : data_table,
            'number' : table_num,
            'keluar' : keluar
        }
        return render(request,'page1.html',context=context)

#fitur ini sama seperti sebelumnya, tapi difungsi kan untuk proses tambahan pesanan dari meja yang sebelumnya sudah memesan
#**************************************************************************************************************************
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
#function finished dan finished 2 akan berlanjut ke function process dan process 2
#**************************************************************************************************************************
    

#function proses(GET) adalam tampilan dalam memproses pesanan customer
#dalam return html akan di sisipkan value pada context dibawah
@login_required(login_url=settings.URL_LOGIN)
@csrf_exempt
def process(request,kode_id):
    
    if request.method == 'GET':
        try:
            data1 = database.objects.get(kode_id=kode_id)
            data_table = tablee6.objects.all()
            table_num = numbertable3.objects.all().values()
            keluar = temp.objects.filter(no_user=request.user.id)

            #proses iterasi setiap value nomor meja dan di ambil yang akhir pada pada context nantinya
            numbers = []
            for i in table_num:
                numbers.append(i['number_table'])  
                        
            #value context ini di siapkan untuk disisipkan ke dalam masing masing input form
            date = dt.now()
            second = date.second
            years = date.year
            context = {
                'data1' : data1,
                'second' : second,
                'years' : years,
                'table' : data_table,
                'number' : numbers[-1],
                'keluar' : keluar,
            }
            return render(request,'page2.html',context=context)
        
        except IndexError as e:#antisipasi kesalahan user(HUMAN ERROR)
            redirect('/finished')#DIARAHKAN KE PART FINISHED UNTUK OTOMATIS MEMPERBAIKI PROSEDUR YANG SEHARUSNYA

#EKSEKUSI BAGIAN PROSES
@csrf_exempt
def proses_post(request):
    if request.method == 'POST':
        try:
            transaction_id = request.POST['transaction_id']#value ini sudah default terisi dari function proses bagian baris context
            kode_barang = request.POST['kode_barang'] #value ini sudah default terisi dari function proses bagian baris context
            no_table_id = request.POST['number_table'] #value ini sudah default terisi dari function proses bagian baris context
            tanggal = date.today() #variabel ini disiapkan untuk kolom tanggal pada table 
            tanggal = tanggal.strftime('%Y-%m-%d') #setting tanggal dan mengambil DAY/MONTH/YEAR
            nama_barang = request.POST['nama_barang']##value ini sudah default terisi dari function proses bagian baris context
            harga_jual = request.POST['harga_jual']#value ini sudah default terisi dari function proses bagian baris context
            quantity = int(request.POST['quantity'])#***HANYA INPUT BAGIAN QUANTITY YANG TIDAK ADA REFERERNSI VALUE PADA GET PROCESS FUNTUION**
            no_user = request.user.id #variabel ini berfungsi untuk mengambil value id dari user pengguna. agar bisa dipakai untuk mengisi kolom no_user pada table yang akan di masukan data.
            total_harga = int(quantity) * int(harga_jual)
            is_complete = False


            if quantity >= 1: #validasi quantity agar tidak di input 0 atau < 0
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
                barang.out_barang = barang.out_barang + quantity #update keluar barang untuk proses kalkukasi tersisa barang
                barang.tersisa = barang.tersisa - quantity #eksekusi tersisa barang dari pengurangan tersisa nya barang dan keluar barang
                if barang.tersisa >= 0: #valiasi apabila barang tersisa lebih dari 0.
                    barang.save()
                    sementara.save()
                    data.save() 
                    orders.save() 
                    return redirect('/finished')#kembali ke halaman katalog pilihan produk untuk tambahan pesanan
                else: #apabila sudah melewati 0 dan hasilnya minus
                    messages.error(request,"Stok Tersisa Tidak Mencukupi") #pesan messages
                    print(barang.tersisa)
                    return redirect(request.META.get("HTTP_REFERER","/")) # mengembalikan ke halaman yang sama/RELOAD
            else :
                messages.error(request,"Quantity Tidak Boleh Kurang Dari 1.")#pesan dari eksekusi quantity yang di pesan.
                return redirect(request.META.get("HTTP_REFERER","/")) #RELOAD
        except ValueError as e: #ANTISIPASI APABILA USER MENGALAMI KESALAHAN DALAM MENGGUNAKAN SISTEM INI
            return redirect(request.META.get("HTTP_REFERER","/"))

#fungsi ini sama seperti penggunakan fungsi process. dan bisa dilihat dari fungsi process
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

def proses_post2(request):
    if request.method == 'POST':
        try:
            transaction_id = request.POST['transaction_id']#value ini sudah default terisi dari function proses bagian baris context
            kode_barang = request.POST['kode_barang'] #value ini sudah default terisi dari function proses bagian baris context
            no_table_id = request.POST['number_table'] #value ini sudah default terisi dari function proses bagian baris context
            tanggal = date.today() #variabel ini disiapkan untuk kolom tanggal pada table 
            tanggal = tanggal.strftime('%Y-%m-%d') #setting tanggal dan mengambil DAY/MONTH/YEAR
            nama_barang = request.POST['nama_barang']##value ini sudah default terisi dari function proses bagian baris context
            harga_jual = request.POST['harga_jual']#value ini sudah default terisi dari function proses bagian baris context
            quantity = int(request.POST['quantity'])#***HANYA INPUT BAGIAN QUANTITY YANG TIDAK ADA REFERERNSI VALUE PADA GET PROCESS FUNTUION**
            no_user = request.user.id #variabel ini berfungsi untuk mengambil value id dari user pengguna. agar bisa dipakai untuk mengisi kolom no_user pada table yang akan di masukan data.
            total_harga = int(quantity) * int(harga_jual)
            is_complete = False


            if quantity >= 1: #validasi quantity agar tidak di input 0 atau < 0
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
                barang.out_barang = barang.out_barang + quantity #update keluar barang untuk proses kalkukasi tersisa barang
                barang.tersisa = barang.tersisa - quantity #eksekusi tersisa barang dari pengurangan tersisa nya barang dan keluar barang
                if barang.tersisa >= 0: #valiasi apabila barang tersisa lebih dari 0.
                    barang.save()
                    sementara.save()
                    data.save() 
                    orders.save() 
                    return redirect('/order_table')#kembali ke halaman katalog pilihan produk untuk tambahan pesanan
                else: #apabila sudah melewati 0 dan hasilnya minus
                    messages.error(request,"Stok Tersisa Tidak Mencukupi") #pesan messages
                    print(barang.tersisa)
                    return redirect(request.META.get("HTTP_REFERER","/")) # mengembalikan ke halaman yang sama/RELOAD
            else :
                messages.error(request,"Quantity Tidak Boleh Kurang Dari 1.")#pesan dari eksekusi quantity yang di pesan.
                return redirect(request.META.get("HTTP_REFERER","/")) #RELOAD
        except ValueError as e: #ANTISIPASI APABILA USER MENGALAMI KESALAHAN DALAM MENGGUNAKAN SISTEM INI
            return redirect(request.META.get("HTTP_REFERER","/"))


#function pada halaman awal yaitu menampilkan list table yang sedang memesan        
@login_required(login_url=settings.URL_LOGIN)
def list_table(request):
    if request.method == 'GET':
        message = "Choose Table"
        try:
            table = orderss6.objects.filter(no_user=request.user.id)
            order = tablee6.objects.filter(no_user=request.user.id)
            table_num = numbertable3.objects.all()
            cashier = kumpulan_cashier.objects.all()
            meja = kumpulan_table.objects.all()
            #menampilkan value di halaman html berdasarkan masing masing referensi value variabel diatas
            context = {
                'orders' : order,
                'table' : table,
                'number' : table_num,
                'message' : message,
                'cashier' : cashier,
                'meja' : meja, 
            }
            
            return render(request,'page3.html',context=context)
        
        #antisipasi kesalahan user dalam menggunakan sistem
        except IndexError:
            numbers = []
            for i in table:
                if i != None: #validasi apabila tidak sama dengan None maka di kosong
                    numbers.append(i.no_table_id)
                else:
                    tablee6.objects.get(no_table=table_num).delete()#jika ada maka ambil informasi dari meja tersebut

        
        
#funstion proses untuk eksekusi customer tahap pertama. 
@csrf_exempt
def post_list_table(request):
    if request.method=='POST':
        try:
            table = orderss6.objects.all().values()
            order = tablee6.objects.filter(no_user=request.user.id)
            meja = kumpulan_table.objects.all()
            cashier = kumpulan_cashier.objects.all()

            table_num = request.POST['number_table'] #input customer ingin di meja berapa
            cashier_name = request.POST['cashier_name'] #nama user. default dari user atau anggota si user melalui table kumpulan_table
            #validasi apabila meja pesanan sudah di dipesan oleh customer sebelumnya
            count = 0
            if numbertable3.objects.filter(number_table=table_num,no_user=request.user.id).exists():
                print(request.user.id)
                count += 1
                message = "Choose Table"
                if count == 0:
                    message = "Choose Table"
                else:
                    message = "Table Sudah Tersedia" # akan muncul notif seperti disamping pada bagian select table.

                context = {
                    'orders' : order,
                    'table' : table,
                    'number' : table_num,
                    'message' : message,
                    'meja' : meja,
                    'cashier' : cashier,
                    
                }
                return render(request,'page3.html',context=context)         
            else: #apabila meja pesanan belum di dipesan oleh customer sebelumnya
                table_num = request.POST['number_table']
                cashier_name = request.POST['cashier_name']
                
                #number_table berfungsi untuk referensi proses selanjutnya cth : proses pemilihan menu pesanan custmoer
                #table_number berfungsi untuk index dari table yang di tampilkan.
                number_table = numbertable3(number_table=table_num,cashier_name=cashier_name,no_user=request.user.id)
                table_number = tablee6(no_table=table_num,nomor_meja=table_num,no_user=request.user.id)
                number_table.save()
                table_number.save()    

                table = orderss6.objects.all()
                order = tablee6.objects.all()              
                context = {
                    'orders' : order,
                    'table' : table,
                    'number' : table_num,
                }
                return redirect('/finished',context=context)     
        except ValueError: #antisipasi mengatasi kesalahan user menggunakan sistem.
            return redirect(request.META.get("HTTP_REFERER","/"))

#proses list pesanan customer berdasarkan meja
@csrf_exempt    
def list_orders(request,no_table_id):
        if request.method=='GET':
            try:
                data = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
                data1 = history.objects.all()
                date = dt.now()
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
            except IndexError: #antisipasi kesalahan user menggunakan system
                data = orderss6.objects.filter(no_table_id=no_table_id)
                data1 = history.objects.all()
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
        
    
#proses eksekusi menciptakan struct pdf
def print_receipt(request,no_table_id):
    orders = orderss6.objects.filter(no_table=no_table_id,no_user=request.user.id)
    detail = master.objects.get(no_table=no_table_id)
    total_harga = 0
    harga = []
    amount = []
    nama_product = []
    quantity = []
    ukuran = 400
    #iterasi yang berfungsi untuk mengambil informasi dari setiap pesanan berdasarkan user(pengguna) dan meja.
    for i in orders:
        total_harga += i.total_harga
        nama_product.append(i.nama_barang)
        quantity.append(i.quantity)
        harga.append(i.harga_jual)
        amount.append(i.total_harga)
        ukuran += 10 #proses ini untuk mengatur panjang pdf berdasarkan panjangnnya pesanan customer

    #proses PDF
    buf = io.BytesIO()
            
    #menciptakan ukuran kertas pdf
    width = 250
    heigth = ukuran #ukuran panjang ini tidak statis. melainkan sesuai panjang nya orderan customer
    custom_size = (width,heigth)
    c = canvas.Canvas(buf, pagesize=custom_size,bottomup=0)
    
    #Judul Untuk PDF
    c.setFont('Helvetica-Bold',40)
    c.drawString(40,50,"mariPOS")

    #menampilkan tanggal transaksi
    tanggal = dt.today()
    tahun = tanggal.year
    c.setFont('Helvetica',8)
    c.drawString(35,70,f"{tanggal} | {detail.transaction_id}{tahun} |")

    #menampikan nama barang,qty,harga        
    c.setFont('Helvetica-Bold',9)
    c.drawString(13,90,"Nama & Harga                                  |  Qty  | Total Harga")

    #mengatur margin setiap baris dan mengiterasi agar memanjang

    #1.Iterasi Nama Produk dari variabel List nama_produk
    c.setFont('Helvetica',10)
    height = 80
    count = 30 #nilai ini menjadi acuan margin memanjang kebawah
    for i in nama_product:
        height += count
        c.drawString(13,height,f"-{i}")

    height = 90 #mengembalikan nilai panjang
    #2.Iterasi Harga masing masing Produk dari variabel List harga
    for i in harga:
        height += count # iterasi ukuran kebawah apabila pesannan lebih dari satu
        c.drawString(20,height,f"Rp.{i}")

    height = 90 #mengembalikan nilai panjang
    #3.Iterasi Harga masing masing Produk dari variabel List harga
    for i in quantity:
        height += count # iterasi ukuran kebawah apabila pesannan lebih dari satu
        c.drawString(170,height,f"x{i}")

    height = 90 #mengembalikan nilai panjang
    #4.Iterasi total_harga(amount) masing masing Produk dari variabel List amount
    for i in amount:
        height += count
        c.drawString(190,height,f"Rp.{i}")

    #proses informasi final paling bawah struct        
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

#function proses mengambil informasi berasarkan masing masing meja
def information(request,no_table_id):
    orders = orderss6.objects.filter(no_table_id=no_table_id)
    context = {
        'orders' : orders,
    }   
    return render(request,'page9.html',context=context)

#proses memasukan data pesanan customer. table ini bersifat sementara
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

#fitur hapus barang pada proses pesanan. 
def deleteitems(request,transaction_id):

    order = temp.objects.filter(transaction_id=transaction_id,no_user=request.user.id)
    #iterasi mengambil kode_id kedalam list
    kode = []
    for i in order:
        kode.append(i.kode_barang)
    
    #proses mengembalikan nilai stok quantity yang di cancel 
    #sehingga kolom tersisa dari katalog kembali seperti semula
    for i in kode:
        data = database.objects.get(kode_id=i,no_user=request.user.id)
        sementara = temp.objects.get(kode_barang=i,no_user=request.user.id)
        data.tersisa = sementara.quantity
        data.save()
        
    
    temp.objects.get(transaction_id=transaction_id).delete()
    orderss6.objects.get(transaction_id=transaction_id).delete()
    return redirect(request.META.get("HTTP_REFERER","/"))

#fitur cancel saat proses transaksi input barang ke dalam meja customer
def executecancel(request):
    data = tablee6.objects.all().values()
    sementara = temp.objects.filter(no_user=request.user.id)
    kode_id = []
    count = 0

    #mengambil data kode_id di masing masing table temp
    for i in sementara:
        kode_id.append(i.kode_barang)
        count += 1

    #eksekusi return stok ketika di cancel ke dalam column stok tersisa pada table katalog database
    for i in kode_id:
        barang = database.objects.get(no_user=request.user.id,kode_id=i)
        stok = temp.objects.get(no_user=request.user.id,kode_barang=i)
        barang.tersisa = stok.quantity
        barang.save()
        temp.objects.get(no_user=request.user.id,kode_barang=i).delete()

    #menghapus kode yang sudah di input saat proses eksekusi table dan nama kasir
    numbers = []
    no_user = []
    for i in data:
        numbers.append(i['no_table'])  
        no_user.append(i['no_user'])
    tablee6.objects.filter(nomor_meja=numbers[-1],no_user=request.user.id).delete()
    numbertable3.objects.filter(number_table=numbers[-1],no_user=request.user.id).delete()
    return redirect('/') #mengembalikan ke halaman awal

#fitur untuk mengubah posisi meja customer
#**************************************************
def settings(request,transaction_id):
    orders = orderss6.objects.get(transaction_id=transaction_id) #Mendapatkan detail informasi setiap transaksi
    meja = kumpulan_table.objects.all()#menampilkan kumpulan meja untuk di pilih kemana customer pindah
    #referernsi untuk menampilkan di halaman html
    context = {
        'orders' : orders,
        'meja' : meja,
    }
    return render(request,'settings.html',context=context)#tujuan ke halaman settings.html

@csrf_exempt
def process_settings(request,transaction_id):
    data = orderss6.objects.get(transaction_id=transaction_id,no_user=request.user.id)
    meja = tablee6.objects.all().values()
    table = request.POST['no_table_id']

    kumpulan = []
    for i in meja:
        kumpulan.append(i['no_table'])

    #kondisi ini digunakan jika pesanan customer tidak ada dalam table pesanan.(antisipisasi HUMAN ERROR)
    if table in kumpulan:
        pass #dilewati bila list meja berada di dalam kolom daftar meja
    else:
        daftar = tablee6(no_table=table,nomor_meja=table,no_user=request.user.id)#di input bila tidak ada
        daftar.save() # simpan ke dalam table meja

    data.no_table = table
    data.save()
    return redirect('/')

#**************************************************



#fitur membaca barang
@login_required
def read(request):
    if request.method == 'GET':
        data = database.objects.all().values()
        return render(request,'read.html',{'data':data})

#fitur menambahkan product baru
#**************************************************
@login_required
@csrf_exempt   
def tambah(request):
    if request.method == 'GET':
        waktu = dt.today()
        #bagian untuk kode_id pada barang
        detik = waktu.second
        tahun = waktu.year
        random = np.random.randint(1000)
        #------------------------------
        template = loader.get_template("tambah.html")
        data = database.objects.all()
        #ketiga variabel di atas, di masukan ke dalam halaman html
        context={
            'waktu':detik,
            'tahun':tahun,
            'random':random
        }
        return HttpResponse(template.render(context,request))#masuk ke dalam file html tambah
    
    #proses menambahkan product kedalam table product
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
        #validasi/memastikan menghindari kode_id yang duplikasi
        if database.objects.filter(kode_id=kode_id).exists():
            return redirect('tambah')
        else:#berfungsi jika lolos qualifikasi duplikasi
            data = database(
                        kode_id=kode_id,nama_barang=nama_barang,
                        jenis=jenis,outlet=outlet,harga_modal=harga_modal,
                        harga_jual=harga_jual,
                        quantity=quantity,sum_of_modal=sum_of_modal,
                        sum_of_jual=sum_of_jual,income_unit=income_unit,
                        sum_of_income=sum_of_income,no_user=no_user,tersisa=tersisa
                        )
            data.save()#menyimpan
    return redirect(request.META.get("HTTP_REFERER","/"))
#**************************************************

#fitur mengedit informasi pada product di table product
#*********************************************************
@login_required #validasi decorator untuk login terlebih dahulu
@csrf_exempt # token untuk proses post pada form
def edit(request,kode_id):
    if request.method=='GET':
        #berfungsi menampilkan data pada halaman edit.html
        data = database.objects.get(kode_id=kode_id)
        context = {
            'data' : data
        }
        return render(request,"edit.html",context)
    else : #proses eksekusi edit data
        kode_id = request.POST['kode_id'] # pada bagian form input kode_id hanya readonly.
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
       
        data = database.objects.get(kode_id=kode_id) #variabel yang menampung data product berdasarkan kode_id
        #proses update
        #***************************
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
        #***************************
        data.save() #simpan data update
        messages.success(request,"Data Berhasil Di Perbarui")
    return redirect(request.META.get("HTTP_REFERER","/")) #RELOAD

#menghapus data product
@login_required
def delete(request,kode_id):
    database.objects.get(kode_id=kode_id).delete()
    messages.success(request,"DATA BERHASIL DIHAPUS")
    return redirect(request.META.get("HTTP_REFERER","/"))


def overview(request):
    if request.method=='GET':
        return render(request,'overview.html')

#proses akhir transaksi
def done(request):
    no_table_id = []
    data = transaction_done.objects.all().values()

    for i in data :
        no_table_id.append(i['no_table'])#mengambil data transaksi selesai pada kolom table
    meja = tablee6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id) #filter dengan variabel list di posisi paling akhir

    for i in meja:
        #validasi ini berfungsi antisipasi kesalahan user dalam menggunakan sistem.
        if no_table_id == meja: #validasi cek value no_table_id di ada di value table meja
            tablee6.objects.get(no_table=no_table_id[-1],no_user=request.user.id).delete() #maka akan di hapus
        else:
            meja = tablee6(no_table=no_table_id[-1],no_user=request.user.id) #ciptakan nomor meja di table meja
            meja.save() #simpan
            tablee6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id).delete() #hapus kembali

    #menghapus nomor table yang sudah melakukan transaksi pembayaran pada table numbertable
    numbertable3.objects.filter(number_table=no_table_id[-1],no_user=request.user.id).delete() 
    #menghapus nomor table yang sudah melakukan transaksi pembayaran pada table numbertable
    orderss6.objects.filter(no_table=no_table_id[-1],no_user=request.user.id).delete()
    return redirect('/')#kembali ke halaman awal


#kumpulan product untuk di tampilkan di halaman setting
def overalsetting(request):
    data = database.objects.filter(no_user=request.user.id)
    context = {
        'data' : data
    }
    return render(request,'overalsettings.html',context=context)

#kumpulan nomor meja untuk di tampilkan di halaman setting
def overalsetting1(request):
    meja = kumpulan_table.objects.filter(no_user=request.user.id)
    context = {
        'meja' : meja
    }
    return render(request,'overalsettings1.html',context=context)

#kumpulan kasir untuk di tampilkan di halaman setting
def overalsetting2(request):
    cashier = kumpulan_cashier.objects.filter(no_user=request.user.id)
    context = {
        'cashier' : cashier
    }
    return render(request,'overalsettings2.html',context=context)

#function untuk tambah meja pada bagian setting
def tambah_meja(request):
    tambah_meja = request.POST['tambah_meja']
    no_user = request.user.id
    meja = kumpulan_table(no_table=tambah_meja,no_user=no_user)
    if kumpulan_table.objects.filter(no_table=tambah_meja).exists():
        pass
    else:
        meja.save()
    return redirect(request.META.get("HTTP_REFERER","/"))

#function untuk tambah cashier pada bagian setting
def tambah_cashier(request):
    cashier = request.POST['cashier']
    no_user = request.user.id
    meja = kumpulan_cashier(name_cashier=cashier,no_user=no_user)
    if kumpulan_cashier.objects.filter(name_cashier=cashier).exists():
        pass
    else:
        meja.save()
    return redirect(request.META.get("HTTP_REFERER","/"))

#function untuk hapus cashier pada bagian setting
def delete_cashier(request,id):
    kumpulan_cashier.objects.get(id=id).delete()
    return redirect(request.META.get("HTTP_REFERER","/"))

#function refresh
def refresh(request):
    return redirect(request.META.get("HTTP_REFERER","/"))


#function menampilkan laporan 
def report(request):
    sekarang = dt.today()
    data = penjualan.objects.filter(tanggal=sekarang,no_user=request.user.id).order_by('-tanggal') #urut berdasarkan tanggal terakhir
    barang = database.objects.filter(no_user=request.user.id)#filter berdasarkan user pengguna
    revenue = 0
    quantity = 0
    count = 0
    for i in data:
        revenue += i.total_harga
        count += 1
        quantity += i.quantity
    #mengambil value variabel diatas dan di tampilkan ke dalam html
    context = {
        'data' : data,
        'sekarang' : sekarang,
        'revenue' : revenue,
        'count' : count,
        'quantity' : quantity,
        'nama_barang' : barang,
    }
    return render(request,'report.html',context=context)#menuju ke halaman laporan


#menampilkan hasil apabila user memfilter laporan
def visualization(request):
    tanggal = request.GET.get('tanggal')
    nama_barang = request.GET.get('nama_barang')
    barang = database.objects.all()
    sekarang = dt.today()
    data = penjualan.objects.filter(tanggal=sekarang,no_user=request.user.id).order_by('-tanggal')
    revenue = 0
    quantity = 0
    count = 0
    
    #validasi filter laporan
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



