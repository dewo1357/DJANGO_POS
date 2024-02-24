# Point Of Sale Menggunakan Python Dan Django Framework

![POS](https://github.com/dewo1357/DJANGO_POS/assets/130409621/46886e4f-1109-442a-87a4-1a18ad5cc1c3)


## Apaitu Django?
Django adalah sebuah framework web yang ditulis dalam bahasa pemrograman Python. Tujuan utamanya adalah memudahkan pembangunan situs web dengan menyediakan seperangkat alat dan fitur yang dapat digunakan untuk mengelola berbagai aspek pengembangan web, termasuk pembuatan tampilan (frontend), pengelolaan basis data, dan penanganan permintaan HTTP.

Berikut ini beberapa poin penting tentang Django:

Model-View-Template (MVT) Architecture: Django mengikuti pola desain Model-View-Template (MVT). Ini adalah varian dari pola desain Model-View-Controller (MVC), di mana model mewakili struktur data, tampilan menangani logika aplikasi, dan template mengatur tampilan.

ORM (Object-Relational Mapping): Django menyediakan ORM yang kuat, yang memungkinkan pengembang untuk berinteraksi dengan basis data menggunakan objek Python, tanpa perlu menulis SQL secara langsung. ORM ini mendukung berbagai jenis basis data, seperti PostgreSQL, MySQL, SQLite, dan Oracle.

Admin Interface Bawaan: Django menyertakan antarmuka admin bawaan yang memudahkan pengelolaan data aplikasi. Dengan sedikit konfigurasi, Anda dapat membuat antarmuka admin yang interaktif untuk menambah, mengedit, dan menghapus data aplikasi Anda.

URL Routing: Django menyediakan sistem routing yang kuat, yang memetakan URL ke tampilan (views) yang sesuai. Ini memungkinkan pengembang untuk membuat struktur URL yang bersih dan terorganisir.

Keamanan: Django secara otomatis mengatasi sejumlah masalah keamanan umum seperti serangan injeksi SQL, serangan cross-site scripting (XSS), dan serangan cross-site request forgery (CSRF). Ini dilakukan melalui berbagai lapisan keamanan bawaan.

Pengujian Otomatis: Django menyediakan kerangka kerja pengujian yang kuat untuk menguji aplikasi secara otomatis. Ini memungkinkan pengembang untuk menulis dan menjalankan tes unit, tes integrasi, dan tes fungsional untuk memastikan aplikasi berjalan dengan baik.

Komunitas yang Besar: Django memiliki komunitas yang besar dan aktif, yang berarti terdapat banyak sumber daya, tutorial, dan paket tambahan yang tersedia untuk membantu pengembang dalam mengembangkan aplikasi.

Dengan fitur-fitur ini dan banyak lagi, Django telah menjadi salah satu framework web Python yang paling populer dan sering digunakan untuk membangun berbagai jenis situs web, mulai dari aplikasi sederhana hingga situs web skala besar.

# Cara Akses Sumber Code

1. Silahkan Download Ke dalam direktori anda
2. Buka projectnya menggunakan Code Editor Favorit Kalian.
3. Aktifkan virtual environment pada path 'e'
   contoh cmd command : e\Scripts\activate.bat
4. masuk ke direkori 'cd system/home/'


## Mempersiapkan Database MySQL
masuk ke direktori 'home/.env/'
![image](https://github.com/dewo1357/DJANGO_POS/assets/130409621/84372b35-561f-41e3-985a-d8e1c5f2be3e)
Gambar diatas adalah direktori yang dimaksud. dalam nya terdapat parameter untuk integerasi ke database local kamu. 
DAN PASTIKAN BENAR AGAR BISA TERHUBUNG!
Note : Jika Kamu Menggunakan Postgreql, kamu bisa mengganti nya menggunakan 'postgresql' pada bagian DB_ENGINE

next:
Lakukan command 'py manage.py migrate'

### kamu akan menjumpai output seperti ini pada terminal kamu : 
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   Applying admin.0001_initial... OK
   Applying admin.0002_logentry_remove_auto_add... OK
   Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying app.0001_initial... OK
  Applying app.0002_tablee6... OK
  Applying app.0003_penjualan_no_user... OK
  Applying app.0004_temp_no_user... OK
  Applying app.0005_kumpulan_cashier_no_user_kumpulan_table_no_user... OK
  Applying app.0006_report_table_no_user... OK
  Applying app.0007_alter_report_table_transaction_id... OK
  Applying app.0008_database_out_database_tersisa... OK
  Applying app.0009_rename_out_database_out_barang... OK
  Applying app.0010_alter_database_kode_id... OK
  Applying app.0011_alter_orderss6_kode_barang... OK
  Applying app.0012_alter_penjualan_kode_barang_alter_temp_kode_barang... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK

5. eksekusi dengan cmd 'py manage.py runserver'
6. default halaman masih di dalam quistioner. sangat berfungsi apabila kamu ingin deploy dan publish. sehingga user yang mendaftar tetap terpantau.
![mariPOS - Google Chrome 23_02_2024 14_53_45](https://github.com/dewo1357/DJANGO_POS/assets/130409621/9d8c812c-a63d-43c5-95f6-5c550bcde1f5)
7. untuk lebih lanjut tentang pemakaian kamu bisa check link video dibawah
      -https://drive.google.com/file/d/1c_29B2nBdPG11kF_p1E04MlCuL79I1eS/view?usp=sharing

