from queue_data import dummy_antrian  # import data dummy antrean dari file queue_data
import customtkinter as ctk   # import library CustomTkinter untuk membuat GUI modern
from tkinter import messagebox # import messagebox untuk popup notifikasi 
import heapq  # import heapq untuk struktur data priority queue
import datetime   # import datetime untuk mengambil waktu saat ini


ctk.set_appearance_mode("light")  # mengatur mode tampilan aplikasi menjadi terang
ctk.set_default_color_theme("blue") # mengatur tema warna default menjadi biru

BG        = "#F6F9FC"  # Pengaturan warna
PANEL     = "#FFFFFF"
CARD      = "#FFFFFF"
CARD2     = "#F0F6FB"
BORDER    = "#D4E3F3"
ACCENT    = "#3A7BD5"
ACCENT2   = "#6FA8DC"
ACCENT3   = "#A7C7E7"
PURPLE    = "#5B7BD5"
GRAD1     = "#3A7BD5"
GRAD2     = "#A7C7E7"
TEXT      = "#1E2A38"
MUTED     = "#7A8FA6"
SHADOW    = "#E3EDF7"

F_TITLE  = ("Georgia", 26, "bold")  # Pengaturan font
F_HEAD   = ("Georgia", 18, "bold")  
F_BTN    = ("Trebuchet MS", 13, "bold")   
F_SMALL  = ("Trebuchet MS", 11)  
F_LOGO   = ("Impact", 30)
F_TINY   = ("Trebuchet MS", 10)


# COMPONENT
def _entry(p, ph, show=""):  # fungsi membuat input field
    return ctk.CTkEntry(
        p, width=320, height=44,   # ukuran input
        placeholder_text=ph, show=show,  # placeholder dan mode password
        fg_color=CARD2,  # warna background input
        border_color=BORDER, # Warna border 
        border_width=2, # Ketebalan border
        text_color=TEXT,  # Warna teks yang diketik
        placeholder_text_color=MUTED, # Warna placeholder
        corner_radius=12,  # Sudut melendung
        font=F_SMALL  # Font input
    )


def _btn(p, t, cmd, fg=ACCENT, tc="#FFFFFF"):  # fungsi membuat tombol
    return ctk.CTkButton(
        p, text=t, command=cmd,  # teks tombol dan fungsi saat diklik
        fg_color=fg, text_color=tc,   #warna tombol dan teks
        hover_color="#5C9BE6",   # warna saat hover
        width=250, height=44,  # ukuran tombol
        corner_radius=22,   # sudut melengkung
        font=F_BTN  # font tombol
    )


def _card(p, w=440, h=460):  # fungsi membuat card/frame
    f = ctk.CTkFrame(
        p, width=w, height=h,  # ukuran frame
        fg_color=CARD,   # warna background frame
        corner_radius=20,   # sudut melengkung
        border_width=2,  # ketebalan border
        border_color=BORDER  # warna border
    )
    f.pack_propagate(False)  # ukuran frame tetap
    return f


def _nav(parent, next_cmd, back_cmd):   # fungsi navigasi tombol lanjut dan kembali
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(pady=12)
    _btn(f, "← Kembali", back_cmd, fg=SHADOW, tc=ACCENT).pack(side="left", padx=10)
    _btn(f, "Lanjut →", next_cmd, fg=ACCENT, tc="#FFFFFF").pack(side="left", padx=10)


def _poli_card(p, i, t, d, tm):  # fungsi membuat kartu poli
    f = ctk.CTkFrame(
        p, width=290, height=170,
        fg_color=CARD,
        corner_radius=16,
        border_width=2,
        border_color=BORDER
    )
    f.pack_propagate(False)

    # top accent strip per poli
    strip_colors = {"🏥": ACCENT, "🦷": ACCENT2, "👶": ACCENT3, "👁": PURPLE}
    strip_c = strip_colors.get(i, ACCENT)
    ctk.CTkFrame(f, height=5, fg_color=strip_c, corner_radius=0).pack(fill="x")

    ctk.CTkLabel(f, text=i, font=("Segoe UI Emoji", 26)).pack(pady=(6, 0))
    ctk.CTkLabel(f, text=t, font=("Trebuchet MS", 13, "bold"), text_color=TEXT).pack()
    ctk.CTkLabel(f, text=d, font=(F_SMALL[0], 9), text_color=MUTED, wraplength=250).pack(padx=8)
    ctk.CTkLabel(
        f, text=f"⏰ {tm}",
        font=(F_TINY[0], 10, "bold"),
        text_color=strip_c
    ).pack(pady=(4, 0))
    return f


# PRIORITY QUEUE 
class PriorityQueue:
    def __init__(self):
        self.data = []  # list untuk menyimpan data antrean
        self.counter = 0  # penghitung ID pasien

    def enqueue(self, nama, poli, keperluan):
        self.counter += 1     # menambah nomor ID pasien
        waktu = datetime.datetime.now().strftime("%H:%M")   # mengambil jam saat pasien mendaftar

        priority_map = {   # mapping tingkat prioritas pasien
            "Darurat": 1,
            "Sakit Berat": 2,
            "Kontrol Rutin": 3,
            "Konsultasi": 4
        }

        prioritas = priority_map.get(keperluan, 5)   # mengambil nilai prioritas

        data_pasien = {   # data pasien disimpan dalam dictionary
            "id": self.counter,
            "nama": nama,
            "poli": poli,
            "keperluan": keperluan,
            "waktu": waktu
        }

        heapq.heappush(self.data, (prioritas, self.counter, data_pasien))     # memasukkan data pasien ke priority queue

        
        sorted_queue = sorted(self.data)   # mengurutkan antrean berdasarkan prioritas

        for i, item in enumerate(sorted_queue, start=1):    # looping mencari nomor antrean pasien
            if item[2]["id"] == self.counter:
                nomor_antrian = i
                break

        return nomor_antrian, waktu   # mengembalikan nomor antrean dan waktu daftar

# BASE 
class BasePage(ctk.CTkFrame):
    def __init__(self, m, title):        # membuat frame dasar untuk semua halaman
        super().__init__(m, fg_color=BG)

        left = ctk.CTkFrame(self, width=280, fg_color=PANEL)  # panel kiri untuk logo dan informasi aplikasi
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ctk.CTkFrame(left, height=6, fg_color=ACCENT).pack(fill="x")   # garis aksen bagian atas


        logo_area = ctk.CTkFrame(left, fg_color="transparent")
        logo_area.pack(pady=30)

        circle = ctk.CTkFrame(              # lingkaran untuk ikon rumah sakit
            logo_area, width=80, height=80,
            fg_color=ACCENT, corner_radius=40
        )
        circle.pack()
        circle.pack_propagate(False)
        ctk.CTkLabel(               # ikon rumah sakit di tengah lingkaran
            circle, text="🏥",
            font=("Segoe UI Emoji", 36),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(                 # logo teks aplikasi    
            left, text="SMART\nHOSPITAL",
            font=F_LOGO, text_color=ACCENT,
            justify="center"
        ).pack(pady=8)

        ctk.CTkLabel(        # subtitle aplikasi
            left, text="Sistem Antrian Digital",
            font=F_TINY, text_color=MUTED
        ).pack()

        ctk.CTkFrame(left, height=2, fg_color=BORDER).pack(fill="x", padx=20, pady=20)

        for tag in ["✅  Cepat", "🎯  Mudah", "💡  Efisien"]:    # menampilkan keunggulan aplikasi
            ctk.CTkLabel(
                left, text=tag,
                font=F_SMALL, text_color=TEXT
            ).pack(pady=4)

        ctk.CTkFrame(left, height=6, fg_color=ACCENT2).pack(side="bottom", fill="x")

        right = ctk.CTkFrame(self, fg_color=BG)
        right.pack(side="left", fill="both", expand=True)

        title_frame = ctk.CTkFrame(right, fg_color="transparent")
        title_frame.pack(pady=(35, 5))
        ctk.CTkLabel(                    # judul halaman
            title_frame, text=title,
            font=F_TITLE, text_color=TEXT
        ).pack()
        ctk.CTkFrame(
            title_frame, height=4, width=120,
            fg_color=ACCENT2, corner_radius=2
        ).pack(pady=(4, 0))

        self.container = _card(right, w=850, h=580)   # area utama untuk isi halaman
        self.container.pack(pady=16)

        self.nav_area = ctk.CTkFrame(right, fg_color="transparent")    # area tombol navigasi
        self.nav_area.pack()


# APP 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SMART HOSPITAL QUEUE")     # judul window aplikasi
        self.state("zoomed")                  # membuka aplikasi dalam mode fullscreen
        self.configure(fg_color=BG)           # warna background utama

        self.queue = PriorityQueue()          # membuat objek priority queue
        for pasien in dummy_antrian:          # memasukkan data dummy ke antrean
            self.queue.enqueue(
                pasien["nama"],
                pasien["poli"],
                pasien["keperluan"]
            )
        self.selected_poli = ""    # menyimpan poli yang dipilih
        self.selected_hari = ""    # menyimpan hari yang dipilih
        self.selected_jam = ""    # menyimpan jam yang dipilih
        self.last_data = {}      # menyimpan data terakhir pasien yang mendaftar
        self.users = {}       # menyimpan data akun pengguna (email dan password)
        self.current_user = None     # menyimpan email pengguna yang sedang login

        self.frames = {}      # dictionary untuk menyimpan semua halaman
        for F in (
            HomePage, PilihanAkunPage,
            LoginPasienPage, RegisterPasienPage,
            PoliPage, JadwalPage, DaftarPage,
            InvoicePage, InvoiceVerifPage, AdminDashboardPage
        ):
            frame = F(self)
            self.frames[F] = frame     # menyimpan halaman ke dictionary
            frame.place(relwidth=1, relheight=1)

        self.show_frame(HomePage)     # halaman pertama yang ditampilkan

    
    def show_frame(self, page):      # mengambil halaman yang ingin ditampilkan
        frame = self.frames[page]
        frame.tkraise()          # memunculkan halaman ke depan

        if hasattr(frame, "refresh"):    # menjalankan refresh jika tersedia
            frame.refresh()

# HOME 
class HomePage(ctk.CTkFrame):     # membuat halaman utama aplikasi
    def __init__(self, m):
        super().__init__(m, fg_color=BG)

        left = ctk.CTkFrame(self, width=560, fg_color=ACCENT)     # panel kiri berisi informasi utama
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        dec1 = ctk.CTkFrame(left, width=220, height=220, fg_color=GRAD2, corner_radius=110)    # dekorasi lingkaran kiri atas
        dec1.place(relx=-0.1, rely=-0.05)

        dec2 = ctk.CTkFrame(left, width=160, height=160, fg_color=ACCENT2, corner_radius=80)  # dekorasi lingkaran kanan bawah
        dec2.place(relx=0.7, rely=0.75)

        body = ctk.CTkFrame(left, fg_color="transparent")
        body.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(         # ikon rumah sakit
            body, text="🏥",
            font=("Segoe UI Emoji", 72),
            text_color="#FFFFFF"
        ).pack(pady=8)

        ctk.CTkLabel(        # logo teks aplikasi
            body, text="SMART\nHOSPITAL\nQUEUE",
            font=("Impact", 46),
            text_color="#FFFFFF",
            justify="center"
        ).pack()

        ctk.CTkLabel(       # deskripsi aplikasi
            body,
            text="Sistem antrian digital rumah sakit\nCepat  •  Mudah  •  Efisien",
            font=F_SMALL,
            text_color="#DFFFFD"
        ).pack(pady=12)

        ctk.CTkButton(            # tombol menuju halaman login/registrasi pasien
            body, text="Masuk Pasien  →",
            command=lambda: m.show_frame(PilihanAkunPage),
            fg_color="#FFFFFF", text_color=ACCENT,
            hover_color=SHADOW,
            width=260, height=50,
            corner_radius=25,
            font=("Trebuchet MS", 14, "bold")
        ).pack(pady=16)

        ctk.CTkButton(          # tombol menuju dashboard admin
            body,
            text="Dashboard Admin",
            command=lambda: m.show_frame(AdminDashboardPage),
            fg_color=ACCENT2,
            hover_color=ACCENT,
            width=260,
            height=45
        ).pack(pady=6)

        right = ctk.CTkFrame(self, fg_color=BG)      # panel kanan untuk menampilkan layanan
        right.pack(side="left", fill="both", expand=True)

        header = ctk.CTkFrame(right, fg_color="transparent")
        header.pack(pady=(28, 4))

        ctk.CTkLabel(      # judul daftar layanan
            header, text="Layanan Tersedia",
            font=F_HEAD, text_color=TEXT
        ).pack()
        ctk.CTkFrame(
            header, height=4, width=100,
            fg_color=ACCENT2, corner_radius=2
        ).pack(pady=4)

        ctk.CTkLabel(        # keterangan layanan
            right,
            text="Pilih poli sesuai kebutuhan kesehatan Anda",
            font=F_SMALL, text_color=MUTED
        ).pack(pady=(0, 14))

        grid = ctk.CTkFrame(right, fg_color="transparent")
        grid.pack()

        r1 = ctk.CTkFrame(grid, fg_color="transparent")
        r1.pack(pady=10)
        _poli_card(r1, "🏥", "Poli Umum",           # kartu Poli Umum
                   "Pemeriksaan kesehatan umum, konsultasi dokter",
                   "07:30 - 23:59").pack(side="left", padx=14)
        _poli_card(r1, "🦷", "Poli Gigi",    # kartu poli gigi
                   "Perawatan gigi, cabut, tambal, scaling",
                   "08:00 - 18:00").pack(side="left", padx=14)

        r2 = ctk.CTkFrame(grid, fg_color="transparent")
        r2.pack(pady=10)
        _poli_card(r2, "👶", "Poli Anak",        # kartu poli anak
                   "Pemeriksaan kesehatan bayi & anak",
                   "08:00 - 13:00").pack(side="left", padx=14)
        _poli_card(r2, "👁", "Poli Mata",             # kartu poli mata
                   "Pemeriksaan mata & konsultasi penglihatan",
                   "10:00 - 16:00").pack(side="left", padx=14)


#PILIHAN AKUN
class PilihanAkunPage(BasePage):       # membuat halaman pilihan login atau registrasi
    def __init__(self, m):
        super().__init__(m, "Pilih Akses")

        ctk.CTkLabel(            # judul sambutan
            self.container,
            text="Selamat Datang! 👋",
            font=("Georgia", 16, "bold"),
            text_color=TEXT
        ).pack(pady=(30, 4))

        ctk.CTkLabel(            # keterangan halaman
            self.container,
            text="Silakan login atau buat akun baru",
            font=F_SMALL, text_color=MUTED
        ).pack(pady=(0, 20))

        ctk.CTkFrame(self.container, height=2, fg_color=BORDER).pack(fill="x", padx=30, pady=8)

        _btn(self.container, "🔐  Login",        # tombol menuju halaman login
             lambda: m.show_frame(LoginPasienPage),
             fg=ACCENT).pack(pady=10)

        _btn(self.container, "📝  Registrasi",   
             lambda: m.show_frame(RegisterPasienPage),
             fg=ACCENT2).pack(pady=10)

        _nav(self.nav_area, lambda: None,    # tombol kembali ke halaman utama
             lambda: m.show_frame(HomePage))


#LOGIN 
class LoginPasienPage(BasePage):        # membuat halaman login pasien
    def __init__(self, m):
        super().__init__(m, "Login")

        ctk.CTkLabel(     # judul halaman login
            self.container,
            text="Masuk ke akun Anda",
            font=("Georgia", 14, "bold"),
            text_color=TEXT
        ).pack(pady=(28, 16))

        self.user = _entry(self.container, "📧  Email")   # input email 
        self.user.pack(pady=6)

        self.pw = _entry(self.container, "🔒  Password", show="*")   # input password
        self.pw.pack(pady=6)

        _nav(self.nav_area,    # tombol login dan kembali 
             lambda: self.login(m),
             lambda: m.show_frame(PilihanAkunPage))

    def login(self, m):    # mengambil data email dan password yang dimasukkan
        email = self.user.get()
        password = self.pw.get()

        if email not in m.users:
            messagebox.showerror("Error", "Akun tidak ditemukan")  # menampilkan error jika email tidak terdaftar
            return

        if m.users[email]["password"] != password:
            messagebox.showerror("Error", "Password salah")   # menampilkan error jika password salah
            return

        m.current_user = email   # menyimpan email pengguna yang berhasil login
        m.show_frame(PoliPage)   # menuju halaman pemilihan poli setelah login berhasil


# REGISTER 
class RegisterPasienPage(BasePage):    # membuat halaman registrasi akun pasien
    def __init__(self, m):
        super().__init__(m, "Registrasi")

        ctk.CTkLabel(       # judul halaman registrasi
            self.container,
            text="Buat akun baru",
            font=("Georgia", 14, "bold"),
            text_color=TEXT
        ).pack(pady=(18, 8))

        self.nama    = _entry(self.container, "👤  Nama");           self.nama.pack(pady=4)      # input data pengguna
        self.alamat  = _entry(self.container, "📍  Alamat");         self.alamat.pack(pady=4)
        self.email   = _entry(self.container, "📧  Email");          self.email.pack(pady=4)
        self.telp    = _entry(self.container, "📱  No Telepon");     self.telp.pack(pady=4)
        self.pw      = _entry(self.container, "🔒  Password", show="*");   self.pw.pack(pady=4)
        self.kpw     = _entry(self.container, "🔒  Konfirmasi Password", show="*"); self.kpw.pack(pady=4)

        _nav(self.nav_area,      # tombol registrasi dan kembali
             lambda: self.validasi(m),
             lambda: m.show_frame(PilihanAkunPage))

    def validasi(self, m):
        if not all([self.nama.get(), self.alamat.get(),    # memastikan semua field sudah diisi
                    self.email.get(), self.telp.get(),
                    self.pw.get(), self.kpw.get()]):
            messagebox.showwarning("Peringatan", "Lengkapi data")
            return
        if self.pw.get() != self.kpw.get():    # memastikan password dan konfirmasi password sama
            messagebox.showerror("Error", "Password tidak sama")
            return
        m.users[self.email.get()] = {"password": self.pw.get()}    # menyimpan data akun baru ke dictionary users dengan email sebagai key
        messagebox.showinfo("Sukses", "Registrasi berhasil")      # menampilkan notifikasi sukses
        m.show_frame(LoginPasienPage)    # kembali ke halaman login setelah registrasi berhasil


#POLI 
class PoliPage(BasePage):     # membuat halaman pemilihan poli
    def __init__(self, m):
        super().__init__(m, "Pilih Poli")

        ctk.CTkLabel(     # judul halaman pemilihan poli
            self.container,
            text="Pilih poli yang Anda tuju",
            font=("Georgia", 14, "bold"),
            text_color=TEXT
        ).pack(pady=(20, 10))

        grid = ctk.CTkFrame(self.container, fg_color="transparent")    # area untuk menampilkan kartu poli
        grid.pack(pady=10)

        r1 = ctk.CTkFrame(grid, fg_color="transparent")
        r1.pack(pady=10)

        def pilih(p):   # fungsi untuk menyimpan poli yang dipilih dan menuju halaman jadwal
            m.selected_poli = p
            m.show_frame(JadwalPage)

        card1 = _poli_card(   # kartu poli Umum
            r1, "🏥", "Poli Umum",
            "Pemeriksaan kesehatan umum, konsultasi dokter",
            "07:30 - 23:59"
        )
        card1.pack(side="left", padx=10,expand=True)
        ctk.CTkButton(card1, text="Pilih",
                  command=lambda: pilih("Umum")).pack(pady=5)

        card2 = _poli_card(    # kartu poli gigi
            r1, "🦷", "Poli Gigi",
            "Perawatan gigi, cabut, tambal, scaling",
            "08:00 - 18:00"
        )
        card2.pack(side="left", padx=10,expand=True)
        ctk.CTkButton(card2, text="Pilih",
                  command=lambda: pilih("Gigi")).pack(pady=5)

        r2 = ctk.CTkFrame(grid, fg_color="transparent")
        r2.pack(pady=10)

        card3 = _poli_card(    # kartu poli anak
            r2, "👶", "Poli Anak",
            "Pemeriksaan kesehatan bayi & anak",
            "08:00 - 13:00"
        )
        card3.pack(side="left", padx=10,expand=True)
        ctk.CTkButton(card3, text="Pilih",
                  command=lambda: pilih("Anak")).pack(pady=5)

        card4 = _poli_card(    # kartu poli mata
            r2, "👁", "Poli Mata",
            "Pemeriksaan mata & konsultasi penglihatan",
            "10:00 - 16:00"
        )
        card4.pack(side="left", padx=10,expand=True)
        ctk.CTkButton(card4, text="Pilih",   
                  command=lambda: pilih("Mata")).pack(pady=5)


# JADWAL
class JadwalPage(BasePage):      # membuat halaman jadwal poliklinik
    def __init__(self, m):
        super().__init__(m, "Jadwal Poliklinik")

        self.title_label = ctk.CTkLabel(
            self.container,
            text="",
            font=("Georgia", 16, "bold"),
            text_color=TEXT
        )
        self.title_label.pack(pady=(10, 10)) # label untuk menampilkan nama poli yang dipilih

        self.table_frame = ctk.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.table_frame.pack(pady=10)    # frame untuk menampilkan jadwal dalam bentuk tabel

        _nav(self.nav_area,    # tombol kembali ke halaman sebelumnya
            lambda: None,
            lambda: m.show_frame(PoliPage))

    def tampilkan_jadwal(self, poli):    # fungsi untuk menampilkan jadwal berdasarkan poli yang dipilih
        for widget in self.table_frame.winfo_children():
            widget.destroy()   # membersihkan jadwal sebelumnya sebelum menampilkan yang baru

        data = {    # data jadwal untuk setiap poli, terdiri dari hari, jam buka, jam tutup, kuota, dan status ketersediaan
            "Gigi": [
                ("Senin", "08:00", "18:00", "50", "Tersedia"),
                ("Selasa", "08:00", "18:00", "40", "Tersedia"),
                ("Rabu", "08:00", "18:00", "30", "Tersedia"),
                ("Kamis", "08:00", "18:00", "20", "Tersedia"),
                ("Jumat", "07:30", "18.00", "5", "Tidak ada"),
            ],
            "Umum": [
                ("Senin", "07:30", "23:59", "40", "Tersedia"),
                ("Selasa", "07:30", "23:59", "20", "Tersedia"),
                ("Rabu", "07:30", "23:59", "13", "Tersedia"),
                ("Kamis", "07:30", "23:59", "10", "Tersedia"),
                ("Jumat", "07:30", "23:59", "30", "Tersedia"),
            ],
            "Anak": [
                ("Senin", "08:00", "13:00", "15", "Tersedia"),
                ("Selasa", "08:00", "13:00", "25", "Tersedia"),
                ("Rabu", "08:00", "13:00", "10", "Tersedia"),
                ("Kamis", "08:00", "13:00", "20", "Tersedia"),   
            ],
            "Mata": [
                ("Senin", "10:00", "16:00", "12", "Tersedia"),
                ("Selasa", "10:00", "16:00", "20", "Tersedia"),
                ("Rabu", "10:00", "16:00", "15", "Tersedia"),
                ("Kamis", "10:00", "16:00", "18", "Tersedia"),
            ]
        }

        self.title_label.configure(text=f"Poliklinik {poli}")   # menampilkan nama poli yang dipilih

        headers = ["Hari", "Jam Buka", "Jam Tutup", "Kuota", "Tindakan"]

        for col, h in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=h,
                font=("Trebuchet MS", 11, "bold"),
                text_color=TEXT
            ).grid(row=0, column=col, padx=10, pady=8)

        for row, item in enumerate(data.get(poli, []), start=1):

            hari, buka, tutup, kuota, status = item    # mengambil data jadwal untuk setiap hari dan menampilkannya dalam tabel
            values = [hari, buka, tutup, kuota]

            for col, val in enumerate(values):   # menampilkan data jadwal dalam tabel
                ctk.CTkLabel(
                    self.table_frame,
                    text=val,
                    font=F_SMALL,
                    text_color=MUTED
                ).grid(row=row, column=col, padx=10, pady=6)

            if status == "Tersedia":   # menampilkan tombol pilih jika jadwal masih tersedia, jika tidak menampilkan keterangan penuh

                btn = ctk.CTkButton(
                    self.table_frame,
                    text="Pilih",
                    width=90,
                    fg_color=ACCENT,
                    command=lambda h=hari, b=buka:
                        self.pilih_hari(h, b)
                )

                btn.grid(row=row, column=4, padx=8)   # menempatkan tombol pilih di kolom tindakan

            else:   # menampilkan keterangan penuh jika jadwal tidak tersedia

                ctk.CTkLabel(
                    self.table_frame,
                    text="Penuh",
                    text_color="red",
                    font=F_SMALL
                ).grid(row=row, column=4)   # menempatkan keterangan penuh di kolom tindakan
        
    def pilih_hari(self, hari, jam):   # fungsi untuk menyimpan hari dan jam yang dipilih dan menuju halaman pendaftaran
        self.master.selected_hari = hari
        self.master.selected_jam = jam
        self.master.show_frame(DaftarPage)   # menuju halaman pendaftaran setelah memilih jadwal

    def tkraise(self, *args):   # dijalankan saat halaman jadwal ditampilkan, memastikan jadwal yang sesuai dengan poli yang dipilih muncul setiap kali halaman ini diakses
        super().tkraise(*args)
        self.tampilkan_jadwal(self.master.selected_poli)   # menampilkan jadwal sesuai dengan poli yang dipilih pada halaman sebelumnya

# DAFTAR 
class DaftarPage(BasePage):    # membuat halaman pendaftaran pasien
    def __init__(self, m):
        super().__init__(m, "Pendaftaran Pasien")

        ctk.CTkLabel(    # judul halaman pendaftaran
            self.container,
            text="Lengkapi Data Pendaftaran",
            font=("Georgia", 16, "bold"),
            text_color=TEXT
        ).pack(pady=(10, 10))

        self.info_poli = ctk.CTkLabel(
            self.container,
            text="",
            font=F_SMALL,
            text_color=ACCENT
        )
        self.info_poli.pack(pady=(0, 10))   # label untuk menampilkan poli yang dipilih

        self.nama = _entry(self.container, "Nama Lengkap")   # input data pasien
        self.nama.pack(pady=4)

        self.alamat = _entry(self.container, "Alamat Domisili")   # input alamat pasien
        self.alamat.pack(pady=4)

        row = ctk.CTkFrame(self.container, fg_color="transparent")  # frame untuk menampung input tempat lahir dan tanggal lahir dalam satu baris
        row.pack(pady=4)

        self.tempat = _entry(row, "Tempat Lahir")   # input tempat lahir pasien
        self.tempat.pack(side="left", padx=5)

        self.tgl = _entry(row, "Tanggal Lahir (dd/mm/yyyy)")  # input tanggal lahir pasien
        self.tgl.pack(side="left", padx=5)

        ctk.CTkLabel(
            self.container,
            text="Keperluan",
            font=F_SMALL,
            text_color=TEXT
        ).pack(pady=(6, 0))

        self.keperluan = ctk.CTkComboBox(
            self.container,
            values=[
                "Darurat",
                "Sakit Berat",
                "Kontrol Rutin",
                "Konsultasi"
            ],
            fg_color=CARD2,
            border_color=BORDER,
            text_color=TEXT
        )
        self.keperluan.pack(pady=6)
        self.keperluan.set("Pilih Keperluan")   # pilihan keperluan pasien yang akan mempengaruhi tingkat prioritas antrean

        self.jaminan = ctk.CTkComboBox(
            self.container,
            values=["BPJS / KIS", "Umum", "Asuransi"],
            fg_color=CARD2,
            border_color=BORDER,
            text_color=TEXT
        )
        self.jaminan.pack(pady=6)
        self.jaminan.set("Pilih Jaminan")   # pilihan jaminan pasien

        _nav(self.nav_area,    # tombol submit dan kembali
             lambda: self.submit(m),
             lambda: m.show_frame(JadwalPage))

    def submit(self, m):  
        if not all([
            self.nama.get(),
            self.alamat.get(),
            self.tempat.get(),
            self.tgl.get()
        ]):                    # memastikan semua field data pasien sudah diisi sebelum mendaftar
            messagebox.showwarning("Peringatan", "Lengkapi semua data")
            return

        if self.keperluan.get() == "Pilih Keperluan":   # memastikan pasien sudah memilih keperluan sebelum mendaftar
            messagebox.showwarning("Peringatan", "Pilih keperluan")
            return

        if self.jaminan.get() == "Pilih Jaminan":   # memastikan pasien sudah memilih jaminan sebelum mendaftar
            messagebox.showwarning("Peringatan", "Pilih jaminan")
            return

        nomor, _ = m.queue.enqueue(
            self.nama.get(),
            m.selected_poli,
            self.keperluan.get()
        )   # mendaftarkan pasien ke antrean dengan memasukkan nama, poli, dan keperluan yang dipilih, serta mendapatkan nomor antrean yang diberikan oleh priority queue

        m.last_data = {    # menyimpan data pasien yang mendaftar untuk ditampilkan di halaman invoice
            "nomor": nomor,
            "nama": self.nama.get(),
            "poli": m.selected_poli,
            "hari": m.selected_hari,
            "jam": m.selected_jam,
            "keperluan": self.keperluan.get()
        }

        m.show_frame(InvoicePage)   # menuju halaman invoice setelah pendaftaran berhasil

    def tkraise(self, *args):
        super().tkraise(*args)
        self.info_poli.configure(      # menampilkan nama poli yang dipilih di bagian atas halaman pendaftaran setiap kali halaman ini ditampilkan
            text=f"Anda mendaftar ke: Poli {self.master.selected_poli}"
        )
    def refresh(self):     # fungsi refresh halaman
        self.info_poli.configure(
            text=f"Poli: {self.master.selected_poli}"
        )

        self.info_hari.configure(    # memperbarui informasi hari dan jam yang dipilih setiap kali halaman ini ditampilkan
            text=f"Hari: {self.master.selected_hari} | Jam: {self.master.selected_jam}"
        )

# INVOICE 
class InvoicePage(BasePage):    # membuat halaman invoice pendaftaran pasien
    def __init__(self, m):
        super().__init__(m, "Invoice")

        ctk.CTkLabel(    # judul halaman invoice
            self.container,
            text="🎫  Bukti Pendaftaran Antrean",
            font=("Georgia", 17, "bold"),
            text_color=TEXT
        ).pack(pady=(20, 15))

        ticket = ctk.CTkFrame(
            self.container,
            width=520,
            height=260,
            fg_color=ACCENT,
            corner_radius=22
        )
        ticket.pack(pady=20)   # frame untuk menampilkan tiket pendaftaran pasien
        ticket.pack_propagate(False)

        ctk.CTkLabel(    # judul tiket pendaftaran
            ticket,
            text="SMART HOSPITAL QUEUE",
            font=("Trebuchet MS", 15, "bold"),
            text_color="#DFFFFD"
        ).pack(pady=(18, 5))

        ctk.CTkFrame(
            ticket,
            height=2,
            fg_color="#DFFFFD"
        ).pack(fill="x", padx=35, pady=5)

        self.info = ctk.CTkLabel(
            ticket,
            text="",
            font=("Impact", 46),
            text_color="#FFFFFF"
        )
        self.info.pack(pady=(18, 8))  # label untuk menampilkan nomor antrean yang diberikan kepada pasien

        self.sub_info = ctk.CTkLabel(
            ticket,
            text="",
            font=("Trebuchet MS", 13),
            text_color="#F6F9FC",
            justify="center"
        )
        self.sub_info.pack()   # label untuk menampilkan informasi detail pendaftaran pasien seperti nama, poli, hari, jam, dan keperluan

        ctk.CTkFrame(
            ticket,
            height=2,
            fg_color="#DFFFFD"
        ).pack(fill="x", padx=35, pady=12)

        self.time_label = ctk.CTkLabel(
            ticket,
            text="",
            font=("Trebuchet MS", 11, "italic"),
            text_color="#EAF4FF"
        )
        self.time_label.pack()   # label untuk menampilkan waktu pendaftaran pasien dibuat, memberikan informasi kapan tiket ini dicetak

        _nav(    # tombol kembali ke halaman sebelumnya dan menuju halaman verifikasi invoice
            self.nav_area,
            lambda: m.show_frame(InvoiceVerifPage),
            lambda: m.show_frame(DaftarPage)
        )

    def tkraise(self, *args):     # dijalankan saat halaman invoice ditampilkan, memastikan informasi yang sesuai dengan data pasien yang mendaftar muncul setiap kali halaman ini diakses
        super().tkraise(*args)

        d = self.master.last_data   # mengambil data pasien yang terakhir mendaftar untuk ditampilkan di halaman invoice

        prefix = {        # prefix untuk nomor antrean berdasarkan poli yang dipilih
            "Umum": "PU",
            "Gigi": "PG",
            "Anak": "PA",
            "Mata": "PM"
        }

        kode = prefix.get(d.get("poli"), "P")
        nomor = d.get("nomor", "-")   # mengambil nomor antrean dari data pasien, jika tidak tersedia tampilkan "-"

        self.info.configure(   
            text=f"{kode}{nomor}"   # menampilkan nomor antrean dengan format kode poli diikuti nomor yang diberikan oleh priority queue
        )

        self.sub_info.configure(   # menampilkan informasi detail pendaftaran pasien
            text=
            f"{d.get('nama')}\n"
            f"Poli {d.get('poli')}\n"
            f"{d.get('hari')} • {d.get('jam')}\n"
            f"Keperluan: {d.get('keperluan')}"
        )

        now = datetime.datetime.now().strftime("%d/%m/%Y • %H:%M")   # mendapatkan waktu saat ini dan memformatnya untuk ditampilkan di label waktu pada halaman invoice
        self.time_label.configure(
            text=f"Dibuat pada {now}"
        )                              # menampilkan waktu cetak invoice

# DONE 
class InvoiceVerifPage(BasePage):    # membuat halaman verifikasi invoice setelah pasien melihat bukti pendaftaran mereka
    def __init__(self, m):
        super().__init__(m, "Selesai")

        check_circle = ctk.CTkFrame(
            self.container, width=110, height=110,
            fg_color=ACCENT, corner_radius=55
        )
        check_circle.pack(pady=(40, 12))
        check_circle.pack_propagate(False)
        ctk.CTkLabel(
            check_circle, text="✔",
            font=("Trebuchet MS", 48, "bold"),
            text_color="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(   # judul halaman verifikasi invoice
            self.container,
            text="Pendaftaran Berhasil!",
            font=("Georgia", 18, "bold"),
            text_color=TEXT
        ).pack(pady=8)

        ctk.CTkLabel(    # pesan untuk pasien setelah melihat invoice, menginformasikan bahwa pendaftaran sudah berhasil
            self.container,
            text="Silakan tunggu giliran Anda\ndi ruang tunggu. Terima kasih 😊",
            font=F_SMALL, text_color=MUTED
        ).pack(pady=4)

        _nav(self.nav_area,   # tombol kembali ke halaman utama dan menuju halaman invoice untuk melihat kembali bukti pendaftaran
             lambda: m.show_frame(HomePage),
             lambda: m.show_frame(InvoicePage))


# ADMIN DASHBOARD   
class AdminDashboardPage(BasePage):   # membuat halaman dashboard untuk admin rumah sakit yang menampilkan antrean pasien berdasarkan prioritas dan memberikan opsi untuk memverifikasi pasien yang dipanggil
    def __init__(self, m):
        super().__init__(m, "Dashboard Admin")

        ctk.CTkLabel(   # judul halaman dashboard admin
            self.container,
            text="Data Antrean Pasien",
            font=("Georgia", 18, "bold"),
            text_color=TEXT
        ).pack(pady=(15, 5))

        self.total_label = ctk.CTkLabel(
            self.container,
            text="",
            font=("Trebuchet MS", 12, "bold"),
            text_color=ACCENT
        )
        self.total_label.pack(pady=(0, 12))   # label untuk menampilkan total jumlah pasien yang sedang antre

        content = ctk.CTkFrame(self.container, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)   # container utama dashboard

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.table = ctk.CTkScrollableFrame(
            left,
            width=560,
            height=380,
            fg_color=CARD2
        )
        self.table.pack(fill="both", expand=True)  # tabel scrollable untuk menampilkan data antrean pasien

        right = ctk.CTkFrame(
            content,
            width=220,
            fg_color=CARD2,
            corner_radius=16,
            border_width=2,
            border_color=BORDER
        )
        right.pack(side="right", fill="y")
        right.pack_propagate(False)   # panel kanan untuk menampilkan informasi bobot prioritas antrean pasien

        ctk.CTkLabel(   # judul informasi bobot prioritas
            right,
            text="📌 Bobot Prioritas",
            font=("Georgia", 13, "bold"),
            text_color=TEXT
        ).pack(pady=(15, 10))

        data = [   # daftar bobot prioritas 
            ("🚨 Darurat", "1"),
            ("⚠ Sakit Berat", "2"),
            ("🩺 Kontrol Rutin", "3"),
            ("💬 Konsultasi", "4")
        ]

        for nama, bobot in data:
            row = ctk.CTkFrame(right, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=5)

            ctk.CTkLabel(row, text=nama, font=F_SMALL).pack(side="left")     # nama kategori prioritas
            ctk.CTkLabel( # nilai prioritas
                row,
                text=f"→ {bobot}",
                font=("Trebuchet MS", 11, "bold"),
                text_color=ACCENT
            ).pack(side="right")
            
        btn = ctk.CTkFrame(self.container, fg_color="transparent")
        btn.pack(pady=15)   # frame tombol admin

        ctk.CTkButton(   # tombol memanggil pasien berikutnya
            btn,
            text="✔ Verifikasi",
            command=self.verifikasi,
            width=180,
            height=42,
            fg_color=ACCENT
        ).pack(side="left", padx=10)

        ctk.CTkButton(   # tombol kembali ke halaman utama
            btn,
            text="← Kembali",
            command=lambda: self.master.show_frame(HomePage),
            width=150,
            height=42,
            fg_color=ACCENT2
        ).pack(side="left", padx=10)

        self.refresh_data()   # menampilkan data antrean pasien saat dashboard admin pertama kali diakses

    def refresh_data(self):   # fungsi untuk memperbarui data antrean pasien yang ditampilkan di dashboard admin, dijalankan setiap kali halaman ini diakses
        for w in self.table.winfo_children():
            w.destroy()   # membersihkan data antrean sebelumnya sebelum menampilkan yang baru

        total = len(self.master.queue.data)   # menghitung total jumlah pasien yang sedang antre dengan mengambil panjang data antrean dari priority queue
        self.total_label.configure(text=f"Total Antrean : {total} Pasien")   # menampilkan total jumlah pasien yang sedang antre 

        headers = ["No", "Nama", "Poli", "Prioritas"]

        for c, h in enumerate(headers):
            ctk.CTkLabel(
                self.table,
                text=h,
                font=("Trebuchet MS", 11, "bold"),
                text_color=TEXT
            ).grid(row=0, column=c, padx=20, pady=8)

        for r, item in enumerate(sorted(self.master.queue.data), start=1):   # mengurutkan data antrean berdasarkan prioritas dan menampilkannya dalam tabel di dashboard admin
            prioritas, _, pasien = item   # mengambil data prioritas, nama, dan poli pasien dari setiap item antrean

            values = [
                r,
                pasien["nama"],
                pasien["poli"],
                prioritas
            ]

            for c, v in enumerate(values):
                ctk.CTkLabel(
                    self.table,
                    text=v,
                    font=F_SMALL,
                    text_color=MUTED
                ).grid(row=r, column=c, padx=20, pady=8)

    def verifikasi(self):   # fungsi untuk memverifikasi pasien yang dipanggil, dijalankan saat tombol verifikasi ditekan di dashboard admin
        if not self.master.queue.data:   # jika antrean kosong
            messagebox.showinfo("Info", "Tidak ada antrean")
            return

        pasien = heapq.heappop(self.master.queue.data)   # mengambil pasien dengan prioritas tertinggi

        messagebox.showinfo(   # menampilkan pasien yang dipanggil
            "Verifikasi",
            f"Pasien {pasien[2]['nama']} dipanggil"
        )

        self.refresh_data()   # memperbarui tabel setelah pasien dipanggil

    def tkraise(self, *args):    # dijalankan saat halaman dashboard dibuka
        super().tkraise(*args)
        self.refresh_data()   # selalu memperbarui data antrean
# RUN 
if __name__ == "__main__":   # memastikan file dijalankan langsung, bukan diimpor sebagai modul
    app = App()   # membuat objek aplikasi
    app.mainloop()  # menjalankan loop utama aplikasi untuk menampilkan GUI dan menangani interaksi pengguna