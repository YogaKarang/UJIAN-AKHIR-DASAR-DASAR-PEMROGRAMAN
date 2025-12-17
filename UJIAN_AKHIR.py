import csv
import os


# Class Mahasiswa (OOP)
class Mahasiswa:
    def __init__(self, nim, nama, tugas=0, uts=0, uas=0, presensi=None):
        self.nim = nim
        self.nama = nama
        self.tugas = tugas
        self.uts = uts
        self.uas = uas
        self.presensi = presensi if presensi else []

    def set_nilai(self, tugas, uts, uas):
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def add_presensi(self, status):
        self.presensi.append(status)

    # Menghitung nilai akhir menggunakan lambda function
    def nilai_akhir(self):
        hitung = lambda t, u, a: (0.30 * t) + (0.35 * u) + (0.35 * a)
        return hitung(self.tugas, self.uts, self.uas)

    # Menentukan grade berdasarkan nilai akhir
    def grade(self):
        na = self.nilai_akhir()
        if na >= 85:
            return "A"
        elif na >= 70:
            return "B"
        elif na >= 55:
            return "C"
        elif na >= 40:
            return "D"
        else:
            return "E"

    # Menghitung persentase kehadiran
    def persentase_hadir(self):
        if len(self.presensi) == 0:
            return 0
        hadir = self.presensi.count("HADIR")
        return round((hadir / len(self.presensi)) * 100, 2)


# List untuk menyimpan seluruh data mahasiswa
daftar_mahasiswa = []


# File I/O (CSV)
def save_data():
    with open("mahasiswa.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["nim", "nama", "tugas", "uts", "uas", "presensi"])
        for m in daftar_mahasiswa:
            writer.writerow([
                m.nim,
                m.nama,
                m.tugas,
                m.uts,
                m.uas,
                "|".join(m.presensi)
            ])


def load_data():
    if not os.path.exists("mahasiswa.csv"):
        return

    with open("mahasiswa.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            presensi = row["presensi"].split("|") if row["presensi"] else []
            m = Mahasiswa(
                row["nim"],
                row["nama"],
                float(row["tugas"]),
                float(row["uts"]),
                float(row["uas"]),
                presensi
            )
            daftar_mahasiswa.append(m)


# Fungsi Pendukung
def cari_mahasiswa(nim):
    for m in daftar_mahasiswa:
        if m.nim == nim:
            return m
    return None


# Validasi nilai 0 - 100
def validasi_nilai(nilai):
    if nilai < 0 or nilai > 100:
        return False
    return True


# Menu Program
def tambah_mahasiswa():
    print("\n=== TAMBAH MAHASISWA ===")
    nim = input("Masukkan NIM: ")
    if cari_mahasiswa(nim):
        print("NIM sudah terdaftar.")
        return

    nama = input("Masukkan Nama: ")
    daftar_mahasiswa.append(Mahasiswa(nim, nama))
    save_data()
    print("Mahasiswa berhasil ditambahkan.")


def tampilkan_mahasiswa():
    print("\n=== DAFTAR MAHASISWA ===")
    if not daftar_mahasiswa:
        print("Belum ada data mahasiswa.")
        return

    for m in sorted(daftar_mahasiswa, key=lambda m: int(m.nim)):
        print(f"{m.nim} - {m.nama}")


def input_nilai():
    print("\n=== INPUT NILAI ===")
    nim = input("Masukkan NIM: ")
    m = cari_mahasiswa(nim)
    if not m:
        print("Mahasiswa tidak ditemukan.")
        return

    tugas = float(input("Masukkan Nilai Tugas (0-100): "))
    if not validasi_nilai(tugas):
        print("Error, Nilai harus di antara 0-100.")
        return

    uts = float(input("Masukkan Nilai UTS (0-100): "))
    if not validasi_nilai(uts):
        print("Error, Nilai harus di antara 0-100.")
        return

    uas = float(input("Masukkan Nilai UAS (0-100): "))
    if not validasi_nilai(uas):
        print("Error, Nilai harus di antara 0-100.")
        return

    m.set_nilai(tugas, uts, uas)
    save_data()
    print("Nilai berhasil disimpan.")


def input_presensi():
    print("\n=== INPUT PRESENSI ===")
    nim = input("Masukkan NIM: ")
    m = cari_mahasiswa(nim)
    if not m:
        print("Mahasiswa tidak ditemukan.")
        return

    pertemuan = int(input("Pertemuan ke berapa?: "))
    if pertemuan <= 0:
        print("Nomor pertemuan harus lebih dari 0.")
        return

    if pertemuan % 2 == 0:
        jenis = "GENAP"
    else:
        jenis = "GANJIL"

    print(f"Pertemuan ke-{pertemuan} termasuk pertemuan {jenis}")

    status = input("Status (Hadir/Alpa/Izin): ").upper()
    if status not in ["HADIR", "ALPA", "IZIN"]:
        print("Presensi tidak valid.")
        return

    m.add_presensi(status)
    save_data()
    print("Presensi berhasil dicatat.")


def laporan():
    print("\n=== LAPORAN NILAI MAHASISWA ===")
    if not daftar_mahasiswa:
        print("Belum ada data mahasiswa.")
        return

    print("-" * 85)
    print(f"{'NIM':<10} {'Nama':<30} {'Nilai Akhir':<12} {'Grade':<7} {'Hadir (%)':<10}")
    print("-" * 85)

    for m in sorted(daftar_mahasiswa, key=lambda m: int(m.nim)):
        print(
            f"{m.nim:<10} {m.nama:<30} "
            f"{round(m.nilai_akhir(), 2):<12} "
            f"{m.grade():<7} "
            f"{m.persentase_hadir():<10}"
        )


def menu_utama():
    load_data()

    while True:
        print("\n======================")
        print(" MENU UTAMA ")
        print("======================")
        print("1. Tambah Mahasiswa")
        print("2. Tampilkan Mahasiswa")
        print("3. Input Nilai")
        print("4. Input Presensi")
        print("5. Laporan Nilai Akhir")
        print("0. Keluar")
        print("======================")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_mahasiswa()
        elif pilih == "2":
            tampilkan_mahasiswa()
        elif pilih == "3":
            input_nilai()
        elif pilih == "4":
            input_presensi()
        elif pilih == "5":
            laporan()
        elif pilih == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan menu tidak valid.")


menu_utama()
