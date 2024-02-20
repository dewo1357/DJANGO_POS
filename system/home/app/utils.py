import datetime as date

def print_struct(penjualan,no_table):
    total = 0
    print('='*10+"Struk Pesanan"+10*'=')
    for i in penjualan:
        print(f"{i.nama_barang} {i.quantity} {i.harga_jual}")
        total += i.total_harga
    print('='*10+"Struk Pesanan"+10*'=')
    print(f"Total : {total}")
    
    