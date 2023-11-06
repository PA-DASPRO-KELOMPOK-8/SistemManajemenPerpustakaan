import datetime
import json
#import pwinput
from prettytable import PrettyTable
import os
os.system('cls')

# Untuk login admin gunakan
# Username: admin
# Password: admin123

def clear():
    os.system('cls')

# Daftar buku reguler
books = {
    1: {'title': 'Python Programming', 'available': True},
    2: {'title': 'Java Programming', 'available': True},
    3: {'title': 'C++ Programming', 'available': True},
    4: {'title': 'PHP Programming', 'available': True},
    5: {'title': 'Java Script Programming', 'available': True}
}

# Daftar buku premium
books_premium = {
    1: {'title': 'IPA KELAS 2', 'available': True},
    2: {'title': 'IPS KELAS 4', 'available': True},
    3: {'title': 'MATEMATIKA DISKRIT', 'available': True},
    4: {'title': 'BIOLOGI KELAS 9', 'available': True},
    5: {'title': 'SENI BUDAYA', 'available': True},
    6: {'title': 'KIMIA', 'available': True}
}

# Database pengguna
Users = r"D:\PA AKHIR\users.json"
# Database admin
Admins = r"D:\PA AKHIR\admins.json"

with open(Users,"r") as userdata:
    users = json.loads(userdata.read())


# Membuat atau memuat database JSON
try:
    with open(Users) as f:
        users = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    pass

# Membuat atau memuat database JSON untuk admin
try:
    with open(Admins) as f:
        admins = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    admins = {}

# Fungsi untuk menyimpan data pengguna ke database JSON
def save_users():
    with open(Users, 'w') as f:
        json.dump(users, f, indent=4)

# Fungsi untuk menyimpan data admin ke dalam file JSON
def save_admins():
    with open(Admins, 'w') as f:
        json.dump(admins, f, indent=4)


# Fungsi untuk menyimpan data buku ke database JSON
def save_books():
    with open("books.json", 'w') as f:
        json.dump(books, f, indent=4)

# Menyimpan data buku premium ke dalam file JSON
def save_premium_books():
    with open("books_premium.json", 'w') as f:
        json.dump(books_premium, f, indent=4)


# Fungsi untuk membayar biaya akses ke buku premium
def access_premium_book():
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return False

    if users[logged_in_user]['emoney'] >= 100000:
        users[logged_in_user]['emoney'] -= 100000
        print(f"Anda telah membayar 100000 E-Money untuk mengakses buku premium.")
        return True
    else:
        print("Anda tidak memiliki cukup E-Money untuk mengakses buku premium.")
        return False

# Fungsi untuk menampilkan daftar buku dengan prettytable
def display_books(books_list):
    table = PrettyTable(['ID', 'Title', 'Available'])
    for key, book in books_list.items():
        table.add_row([key, book['title'], 'Available' if book['available'] else 'Not Available'])
    print(table)


# Fungsi untuk membuat atau login akun pengguna atau admin
def login_or_register_user():
    clear()
    global logged_in_user
    while True:
        print("""
    ----------------------------------------------
    |       SELAMAT DATANG DI PERPUSTAKAAN 8     |
    |--------------------------------------------|
    |                                            |
    |1.                 LOGIN USER               |
    |2.                 LOGIN ADMIN              |
    |3.                 REGISTRASI               |
    |4.                 KELUAR                   |
    |                                            |
    ---------------------------------------------
        """)
        choice = input("Pilih opsi: ")

        if choice == '1':
            login_user()
        elif choice == '2':
            login_admin()
        elif choice == '3':
            register_user()
        elif choice == '4':
            save_users()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def login_admin():
    global logged_in_user
    clear()
    print("---------------------- MENU LOGIN ADMIN ----------------------")
    username = input("Masukkan username admin: ")
    password = input("Masukkan password admin: ")

    if not username or not password:
        print("Username atau password tidak boleh kosong.")
        return

    try:
        with open(Admins) as f:
                Admins = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        admins = {}

    if username in admins and admins[username]['password'] == password:
        clear()
        print(f"Login admin berhasil. Selamat datang, {username}!")
        logged_in_user = username
        admin_menu()
    else:
        print("Login admin gagal. Username atau password salah.")


def login_user():
    global logged_in_user
    clear()
    print("---------------------- MENU LOGIN ----------------------")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if not username or not password:
        print("Username atau password tidak boleh kosong.")
        return

    try:
        with open(Users) as userdata:
            users = json.load(userdata)
    except (json.JSONDecodeError, FileNotFoundError):
        users = {}

    if username in users and users[username]['password'] == password:
        clear()
        print(f"Login berhasil. Selamat datang, {username}!")
        logged_in_user = username
        main_menu()
    else:
        print("Login gagal. Username atau password salah.")

# Fungsi untuk registrasi pengguna
def register_user():
    clear()
    print("---------------------- MENU REGISTRASI ----------------------")
    username = input("Masukkan username baru: ")
    password = input("Masukkan password baru: ")

    if not username or not password:
        print("Username atau password tidak boleh kosong.")
        return

    if username in users:
        print("Username sudah terdaftar. Silakan coba dengan username lain.")
    else:
        akun_baru = {'username': username, 'password': password, 'emoney': 0}
        users[username] = akun_baru  # Perbarui kamus users dengan informasi pengguna baru
        save_users()
        print("Registrasi berhasil. Silahkan Login")


# Fungsi untuk cek saldo
def cek_saldo():
    clear()
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return

    print(f"Saldo E-Money Anda saat ini: {users[logged_in_user]['emoney']}")

# Fungsi untuk top up saldo E-Money
def top_up_emoney():
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return

    amount_input = input("Masukkan jumlah saldo yang ingin ditambahkan: ")

    if not amount_input:
        print("Jumlah tidak boleh kosong.")
        return

    try:
        amount = int(amount_input)

        if amount < 0:
            print("Jumlah tidak valid.")
            return

        users[logged_in_user]['emoney'] += amount
        print(f"\n---------------------- !!! TOP-UP BERHASIL !!! ----------------------\n------------------ Saldo E-Money Anda sekarang: {users[logged_in_user]['emoney']} ------------------")
    except ValueError:
        print("Jumlah harus berupa angka.")



# Fungsi untuk meminjam buku
def borrow_book():
    clear()
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return

    display_books(books)
    book_id_input = input("Masukkan ID buku yang ingin dipinjam\n(tekan Enter untuk batal): ")

    if not book_id_input:
        clear()
        return

    try:
        book_id = int(book_id_input)

        if book_id in books and books[book_id]['available']:
            today = datetime.date.today()
            due_date = today + datetime.timedelta(days=7)
            books[book_id]['available'] = False
            books[book_id]['Peminjam'] = logged_in_user
            books[book_id]['due_date'] = due_date
            clear()
            print(f"------------------ Buku dengan ID {book_id} berhasil dipinjam ------------------\n ------------------ Tanggal pengembalian: {due_date} ------------------")
        else:
            print("Buku tidak tersedia atau ID tidak valid.")
    except ValueError:
        print("ID buku harus berupa angka.")

# Fungsi untuk mengembalikan buku
def return_book():
    clear()
    global logged_in_user
    display_books(books)
    book_id_input = input("Masukkan ID buku yang ingin dikembalikan\n(tekan Enter untuk batal): ")

    if not book_id_input:
        clear()
        return

    try:
        book_id = int(book_id_input)

        if book_id in books and not books[book_id]['available'] and books[book_id]['Peminjam'] == logged_in_user:
            today = datetime.date.today()
            due_date = books[book_id]['due_date']
            # Hapus bagian kode yang menangani perhitungan denda
            books[book_id]['available'] = True
            books[book_id]['Peminjam'] = None
            books[book_id]['due_date'] = None
            print(f"Buku dengan ID {book_id} berhasil dikembalikan.")
        else:
            clear()
            print("Buku tersedia, Anda tidak meminjam buku tersebut.")
    except ValueError:
        clear()
        print("ID buku harus berupa angka.")


def borrow_premium_book():
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return
    display_premium_books()

    try:
        book_id_input = input("Masukkan ID buku premium yang ingin dipinjam (tekan Enter untuk batal): ")

        if not book_id_input:
            return

        book_id = int(book_id_input)

        if book_id in books_premium and books_premium[book_id]['available']:
            print(f"Anda perlu membayar 100000 E-Money untuk mengakses buku premium.")
            confirmation = input("Apakah Anda yakin ingin melanjutkan? (y/n): ")

            if confirmation.lower() == 'y':
                if access_premium_book():
                    today = datetime.date.today()
                    due_date = today + datetime.timedelta(days=7)
                    books_premium[book_id]['available'] = False
                    books_premium[book_id]['Peminjam'] = logged_in_user
                    books_premium[book_id]['due_date'] = due_date
                    print(f"------------------ Buku premium dengan ID {book_id} berhasil dipinjam ------------------\n ------------------ Tanggal pengembalian: {due_date} ------------------")
            else:
                print("Peminjaman dibatalkan.")
        else:
            print("Buku tidak tersedia atau ID tidak valid.")
    except ValueError:
        print("ID buku harus berupa angka.")


def return_premium_book():
    global logged_in_user
    if not logged_in_user:
        print("Anda harus login terlebih dahulu.")
        return
    display_books(books_premium)

    book_id_input = input("Masukkan ID buku premium yang ingin dikembalikan (tekan Enter untuk batal): ")

    if not book_id_input:
        return

    try:
        book_id = int(book_id_input)

        if book_id in books_premium and not books_premium[book_id]['available'] and books_premium[book_id]['Peminjam'] == logged_in_user:
            today = datetime.date.today()
            due_date = books_premium[book_id]['due_date']
            days_diff = (today - due_date).days
            fine = max(0, days_diff) * 10000
            if fine > users[logged_in_user]['emoney']:
                print(f"Anda memiliki denda sebesar {fine}, silakan top up saldo E-Money Anda.")
            else:
                books_premium[book_id]['available'] = True
                books_premium[book_id]['Peminjam'] = None
                books_premium[book_id]['due_date'] = None
                users[logged_in_user]['emoney'] -= fine
                print(f"Buku premium dengan ID {book_id} berhasil dikembalikan. Denda yang harus dibayarkan: {fine}")
                print(f"Saldo E-Money Anda sekarang: {users[logged_in_user]['emoney']}")
        else:
            print("Buku sudah tersedia, Anda tidak meminjam buku tersebut, atau ID tidak valid.")
    except ValueError:
        print("ID buku harus berupa angka.")



# Fungsi untuk menambahkan buku baru
def add_book():
    clear()
    title = input("Masukkan judul buku: ")
    books[max(books.keys()) + 1] = {'title': title, 'available': True}
    save_books()
    print(f"Buku '{title}' berhasil ditambahkan.")

# Fungsi untuk mengubah judul buku
def update_book_title():
    clear()
    global books
    display_books(books)
    book_id_input = input("Masukkan ID buku yang ingin diperbarui \n(tekan Enter untuk batal): ")
    if not book_id_input:
        return

    try:
        book_id = int(book_id_input)

        if book_id in books:
            if not books[book_id]['available']:
                print(f"Buku dengan ID {book_id} sedang dipinjam atau tidak tersedia.")
            else:
                new_title = input(f"Masukkan judul baru untuk buku '{books[book_id]['title']}': ")

                if not new_title:
                    print("Judul tidak boleh kosong.")
                    return

                books[book_id]['title'] = new_title
                print(f"Judul buku dengan ID {book_id} berhasil diperbarui.")
        else:
            print("ID buku tidak valid.")
    except ValueError:
        print("ID buku harus berupa angka.")




# Fungsi untuk menghapus buku dari daftar
def delete_book():
    clear()
    display_books(books)
    book_id_input = input("Masukkan ID buku yang ingin dihapus \n(tekan Enter untuk batal): ")
    if not book_id_input:
        return

    try:
        book_id = int(book_id_input)

        if book_id in books:
            if not books[book_id]['available']:
                print(f"Buku dengan ID {book_id} sedang dipinjam atau tidak tersedia.")
            else:
                del books[book_id]
                clear()
                save_books()
                print(f"Buku dengan ID {book_id} berhasil dihapus.")
                
                # Mengurutkan ulang ID buku
                for i, key in enumerate(sorted(books.keys())):
                    if i+1 != key:
                        books[i+1] = books[key]
                        del books[key]
                save_books()
        else:
            print("ID buku tidak valid.")
    except ValueError:
        print("ID buku harus berupa angka.")



# Fungsi untuk menampilkan daftar buku premium
def display_premium_books():
    clear()
    display_books(books_premium)

# Fungsi untuk menambah buku premium baru
def add_premium_book():
    clear()
    title = input("Masukkan judul buku premium: ")
    books_premium[max(books_premium.keys()) + 1] = {'title': title, 'available': True}
    save_premium_books()  # Menyimpan data buku premium ke dalam file JSON
    print(f"Buku premium '{title}' berhasil ditambahkan.")


# Fungsi untuk mengubah judul buku premium
def update_premium_book_title():
    clear()
    global books_premium
    display_books(books_premium)
    book_id_input = input("Masukkan ID buku premium yang ingin diperbarui \n(tekan Enter untuk batal): ")
    if not book_id_input:
        return

    try:
        book_id = int(book_id_input)

        if book_id in books_premium:
            if not books_premium[book_id]['available']:
                print(f"Buku premium dengan ID {book_id} sedang dipinjam atau tidak tersedia.")
            else:
                new_title = input(f"Masukkan judul baru untuk buku premium '{books_premium[book_id]['title']}': ")

                if not new_title:
                    print("Judul tidak boleh kosong.")
                    return

                books_premium[book_id]['title'] = new_title
                print(f"Judul buku premium dengan ID {book_id} berhasil diperbarui.")
        else:
            print("ID buku premium tidak valid.")
    except ValueError:
        print("ID buku premium harus berupa angka.")


# Fungsi untuk menghapus buku premium dari daftar
def delete_premium_book():
    clear()
    display_books(books_premium)
    book_id_input = input("Masukkan ID buku premium yang ingin dihapus \n(tekan Enter untuk batal): ")
    if not book_id_input:
        return

    try:
        book_id = int(book_id_input)

        if book_id in books_premium:
            if not books_premium[book_id]['available']:
                print(f"Buku premium dengan ID {book_id} sedang dipinjam atau tidak tersedia.")
            else:
                del books_premium[book_id]
                save_premium_books()  # Menyimpan perubahan ke dalam file JSON
                clear()
                print(f"Buku premium dengan ID {book_id} berhasil dihapus.")
                
                # Mengurutkan ulang ID buku premium
                for i, key in enumerate(sorted(books_premium.keys())):
                    if i+1 != key:
                        books_premium[i+1] = books_premium[key]
                        del books_premium[key]
                save_premium_books()  # Menyimpan perubahan setelah pengurutan ulang
        else:
            print("ID buku premium tidak valid.")
    except ValueError:
        print("ID buku premium harus berupa angka.")



def admin_menu():
    clear()
    while True:
        print("\n===== MENU ADMIN =====")
        print("1. Kelola Buku Reguler\n2. Kelola Buku Premium\n3. Logout")
        choice = input("Pilih opsi: ")

        if choice == '1':
            manage_regular_books()
        elif choice == '2':
            manage_premium_books()
        elif choice == '3':
            global logged_in_user
            logged_in_user = None
            print("Berhasil keluar.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def manage_regular_books():
    clear()
    while True:
        print("\n===== MENU ADMIN - BUKU REGULER =====")
        print("1. Tambah Buku\n2. Ubah Judul Buku\n3. Hapus Buku\n4. Tampilkan Buku\n5. Kembali ke Menu Utama")
        choice = input("Pilih opsi: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            update_book_title()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            clear()
            display_books(books)
        elif choice == '5':
            clear()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def manage_premium_books():
    clear()
    while True:
        print("\n===== MENU ADMIN - BUKU PREMIUM =====")
        print("1. Tambah Buku Premium\n2. Ubah Judul Buku Premium\n3. Hapus Buku Premium\n4. Tampilkan Buku Premium\n5. Kembali ke Menu Utama")
        choice = input("Pilih opsi: ")

        if choice == '1':
            add_premium_book()
        elif choice == '2':
            update_premium_book_title()
        elif choice == '3':
            delete_premium_book()
        elif choice == '4':
            display_books(books_premium)
        elif choice == '5':
            clear()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


def main_menu():
    while True:
        print("""
    ----------------------------------------------
    |                SELAMAT DATANG              |
    |--------------------------------------------|
    |                                            |
    |1.              PINJAM BUKU                 |
    |2.              KEMBALIKAN BUKU             |
    |3.              TOP-UP                      |
    |4.              CEK SALDO                   |
    |5.              PINJAM BUKU PREMIUM         |
    |6.              KEMBALIKAN BUKU PREMIUM     |
    |7.              KELUAR                      |
    |                                            |
    ----------------------------------------------
        """)

        choice = input("Pilih opsi: ")

        if choice == '1':
            borrow_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            top_up_emoney()
        elif choice == '4':
            cek_saldo()
        elif choice == '5':
            borrow_premium_book()
        elif choice == '6':
            return_premium_book()
        elif choice == '7':
            global logged_in_user
            logged_in_user = None
            clear()
            print("Berhasil keluar.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


# Dapatkan direktori tempat skrip Python berada
script_dir = os.path.dirname(__file__) if __file__ else '.'

# Gabungkan direktori dengan nama file JSON
Users = os.path.join(script_dir, 'users.json')

logged_in_user = None

if __name__ == '__main__':
    # Menambahkan user admin
    if 'admin' not in users:
        users['admin'] = {'password': 'admin123', 'emoney': 0}
        save_users()

    login_or_register_user()
