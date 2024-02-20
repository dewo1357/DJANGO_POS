from django.urls import path
from . import views

urlpatterns = [
    path('',views.list_table,name='table'),#halaman awal dan proses login(1)
    path('registration/',views.sign_up,name='registration'),#proses registrasi
    path('question/',views.question,name='question'),
    path('proses_regist/',views.post_question,name='questioner'),
    path('logout/',views.sign_out,name='logout'),#proses logout
    path('login/',views.welcome,name='login'),# tampilan table(GET)
    path('post_list_table',views.post_list_table,name='post_list_table'),#table(POST)
    path('finished/',views.finished,name='finished'),#tampilan order menu(GET)
    path('finished/process/<str:kode_id>/',views.process,name='process'),#tampilan memproses pesanan(GET)
    path('order_table/',views.finished2,name='order_table'),#tampilan memproses pesanan di dalam table(GET)
    path('post_process',views.proses_post,name='proses_post'),#proses pesanan(POST)
    path('order_table/process2/<str:kode_id>/',views.process2,name='process2'),#Tampilan proses tambahan pesanan dalam table(POST)
    path('post_process2',views.proses_post2,name='proses_post2'),# proses tambahan pesanan dalam table(POST)
    path('delete_t/',views.execute,name="hapus"),#proses pengumpulan produk di waktu memeasan
    path('delete_u/',views.executecancel,name="cancel"),#CANCEL saat proses pengumpulan produk di waktu memesan
    path('delete_item/<str:transaction_id>/',views.deleteitems,name="delete_item"),#menghapus salah satu kumpulan dari proses waltu pengumpulan
    path('done/',views.information,name='done'),#informasi akhir pesanan.
    path('table/list/<str:no_table_id>/',views.list_orders,name='list'),#list pesanan pada masing masing table(GET)
    path('settings/<str:transaction_id>/',views.settings,name='settings'),#edit table/memindahkan produk ke table lain(GET)
    path('settings/process_settings/<str:transaction_id>/',views.process_settings,name='process_settings'),#eksekusi pemindahakn produk
    path('table/finish/<str:no_table_id>/',views.finishpay,name='finish'),#step awal proses pembayaran(POST)
    path('selesai/',views.done,name = 'selesai'),#FINISHED(PROSES PEMBAYARAN STEP AKHIR)
    path('print_receipt/<str:no_table_id>/',views.print_receipt,name='print_receipt'),#print_receipt
    path('refresh/',views.refresh,name='refresh'),#refresh
    path('report/',views.report,name='visualization'),
    path('hasil/',views.visualization,name='hasil'),
    #######SETTINGS (CRUD)#######
    path('product/',views.overalsetting,name='ovr_set'),
    path('cashier/',views.overalsetting1,name='ovr_set1'),
    path('tambah_cashier',views.tambah_cashier,name="tambah_cashier"),
    path('delete_cashier/<str:id>',views.delete_cashier,name="delete_cashier"),
    path('table_/',views.overalsetting2,name='ovr_set2'),
    path('tambah_meja',views.tambah_meja,name="tambah_meja"),
    path('read/',views.read,name='read'),
    path('read/tambah/',views.tambah,name='tambah'),
    path('read/edit/<str:kode_id>/',views.edit,name='edit'),
    path('delete/<str:kode_id>/',views.delete,name='delete'),
]