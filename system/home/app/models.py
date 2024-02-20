from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class database(models.Model):
    kode_id = models.BigIntegerField(primary_key=True,null=False)
    nama_barang = models.CharField(max_length=30)
    jenis = models.CharField(max_length=30)
    outlet = models.CharField(max_length=30)
    harga_modal = models.IntegerField(null=False)
    harga_jual = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    sum_of_modal = models.IntegerField(null=False)
    sum_of_jual = models.IntegerField(null=False)
    income_unit = models.IntegerField(null=False)
    sum_of_income = models.IntegerField(null=False)
    no_user = models.CharField(max_length=30,null=True)
    out_barang = models.IntegerField(null=True, default=0)
    tersisa = models.IntegerField(null=True,default=0)


class transaction(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    kode_barang = models.IntegerField(null=False)
    tanggal = models.DateTimeField(null=False)
    nama_barang = models.CharField(max_length = 30, null=False)
    harga_jual = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    total_harga = models.IntegerField(null=False)


class tablee66(models.Model):
    no_table = models.IntegerField(null=True)
    nomor_meja = models.IntegerField(null=True)
    no_user = models.CharField(max_length=30,null=True)

class tablee6(models.Model):
    no_table = models.IntegerField(null=True)
    nomor_meja = models.IntegerField(null=True)
    no_user = models.CharField(max_length=30,null=True)


class orderss6(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField()
    kode_barang = models.BigIntegerField(null=False)
    tanggal = models.DateField(null=False)
    nama_barang = models.CharField(max_length = 30, null=False)
    harga_jual = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    total_harga = models.IntegerField(null=False)
    is_complete = models.BooleanField(default=False)
    no_user = models.CharField(max_length=30,null=True)

class penjualan(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField(null=False)
    kode_barang = models.BigIntegerField(null=False)
    tanggal = models.DateField(null=False)
    nama_barang = models.CharField(max_length = 30, null=False)
    harga_jual = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    total_harga = models.IntegerField(null=False)
    no_user = models.CharField(max_length=30,null=True)

class numbertable(models.Model):
    id_no = models.IntegerField(primary_key= True,null=False)
    number_table = models.IntegerField(null=False)
    cashier_name = models.CharField(max_length=30)
    


class numbertable3(models.Model):
    number_table = models.IntegerField(null=False)
    cashier_name = models.CharField(max_length=30)
    no_user = models.CharField(max_length=30,null=True)

class history(models.Model):
    history = models.IntegerField()

class temp(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField()
    kode_barang = models.BigIntegerField(null=False)
    tanggal = models.DateTimeField(null=False)
    nama_barang = models.CharField(max_length = 30, null=False)
    harga_jual = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    total_harga = models.IntegerField(null=False)
    is_complete = models.BooleanField(default=False)
    no_user = models.CharField(max_length=30,null=True)

class report_table(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 50)
    no_table = models.IntegerField()
    tanggal = models.DateTimeField(null=False)
    total_amount = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
    no_user = models.CharField(max_length=30,null=True)

class transaction_finish(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField()
    tanggal = models.DateTimeField(null=False)
    total_amount = models.IntegerField(null=False)
    pay = models.IntegerField(null=False)
    kembalian = models.IntegerField(null=False)

class transaction_done(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField()
    tanggal = models.DateTimeField(null=False)
    total_amount = models.IntegerField(null=False)
    pay = models.IntegerField(null=False)
    kembalian = models.IntegerField(null=False)


class master(models.Model):
    transaction_id = models.CharField(primary_key=True,null=False,max_length = 30)
    no_table = models.IntegerField()
    tanggal = models.DateTimeField(null=False)
    total_amount = models.IntegerField(null=False)
    discount = models.DecimalField(default=0,null=False, max_digits=10, decimal_places=2)
    pay = models.IntegerField(null=False)
    kembalian = models.IntegerField(null=False)


class kumpulan_table(models.Model):
    no_table = models.IntegerField(null=False)
    no_user = models.CharField(max_length=30,null=True)

class kumpulan_cashier(models.Model):
    name_cashier = models.CharField(max_length=30)
    no_user = models.CharField(max_length=30,null=True)


class pendaftar(models.Model):
    nama_usaha = models.CharField(max_length=50)
    nama_toko = models.CharField(max_length=50)
    alamat = models.CharField(max_length=50)
    Jumlah_anggota = models.CharField(max_length=20)
    skala = models.CharField(max_length=20)
    whatssapp = models.CharField(max_length=12)
