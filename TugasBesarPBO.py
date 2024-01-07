from datetime import time, timedelta
from random import randint
import mysql.connector

#Kelas yang berisikan daftar-daftar aset
class Aset:
	idLok = 0
	daftab = []
	idFilm = 0
	dafilm = []
	daftari = ("Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu")
	jadwal = []
	for i in range(6, 24, 3):
		jadwal.append(time(hour=i))
	id_tabel = 'id INT(10) AUTO_INCREMENT PRIMARY KEY'
	def_kolom_reguler = 'a INT(1), b INT(1), c INT(1), d INT(1), e INT(1), f INT(1), g INT(1)'
	def_kolom_premium = 'a INT(1), b INT(1), c INT(1), d INT(1), e INT(1), f INT(1)'
	kolom_reguler = '(a,b,c,d,e,f,g)'
	kolom_premium = '(a,b,c,d,e,f)'
	isi_reguler = [0,0,0,0,0,0,0]
	isi_premium = [0,0,0,0,0,0]

#Kelas abstrak yang berisikan satuan waktu dan jadwal
#Kelas ini memiliki properti (privat) __Hari dan __waktu
class Waktu():
	#penentuan hari: berisikan hari, dipilih dari daftar hari
	def tentukanHari(self, Hari):
		self.__Hari = Aset.daftari[Hari]	

	#penentuan hari: berisikan waktu, dipilih dari jadwal
	def tentukanWaktu(self, pilihan):
		self.__waktu = Aset.jadwal[pilihan].strftime('%H:%M')
	
	#metode untuk menampilkan properti (privat) dari suatu Waktu
	def tampilHari(self): return self.__Hari
	def tampilWaktu(self): return self.__waktu
	
class Tingkatan():
	#penentuan tingkat (layanan) dari suatu ruang
	def __init__(self, namaTingkatan, baris, kolom, biaya):
		self.__nama = namaTingkatan
		self._baris = baris
		self._kolom = kolom
		self.__biayadasar = biaya
		
	def tampilTingkat(self): return self.__nama
	def tampilBiaya(self): return self.__biayadasar
	
	def Uang(self, hari):
		if hari == "Sabtu" or hari == "Minggu":
			self.__biaya = self.__biayadasar * 1.2
		else: self.__biaya = self.__biayadasar
		return self.__biaya

class Film(Waktu):
	#inisialisasi Film: berisikan judul dan durasi dari sebuah film
	def __init__(self, judulFilm:str, durasi:float):
		self.__judul = judulFilm
		self.__lama = timedelta(minutes=durasi)
		self.__id = Aset.idFilm
		Aset.dafilm.append(self)
		Aset.idFilm+=1
	
	def film(self, judulFilm:str, durasi:float):
		self.__judul = judulFilm
		self.__lama = durasi

	#metode untuk menampilkan properti (privat) dari suatu film
	def tampilJudul(self): return self.__judul
	def tampilLama(self): return self.__lama
	
	#penentuan waktu penontonan: berisikan hari dan waktu
	def tentukanHari(self, Hari):
		super().tentukanHari(Hari)	
	def tentukanWaktu(self, pilihan):
		super().tentukanWaktu(pilihan)

#		
class Ruang(Tingkatan):
	def __init__(self, urutan):
		self.__urutan = urutan	
	
	def tipeRuang(self, tingkat:Tingkatan):
		super().__init__(tingkat.tampilTingkat(), tingkat._baris, tingkat._kolom, tingkat.tampilBiaya())
	
	def tampilUrutan(self): return self.__urutan
	
	def bacaRuang(self, urcab, hari, waktu):
		self.bdruang = "Cabang" + str(urcab+1) + '_' + str(self.tampilUrutan() + 1) + '_' + hari + '_' + waktu[0:2]
		tunjuk.execute(f"SELECT * FROM {self.bdruang}")
		pesanan = tunjuk.fetchall()
		return pesanan
	
	def lihatkursi(self, baris, kolom):
		tunjuk.execute(f"SELECT {kolom} FROM {self.bdruang} WHERE id = {baris}")
		status = tunjuk.fetchone()
		print(status)
		if status[0] == 0: return True
		else: return False

	def tetapkanKursi(self, baris, kolom):
		tunjuk.execute(f"UPDATE {self.bdruang} SET {kolom} = {1} WHERE id = {baris}")

	def tataRuang(self, urcab, tingkat, hari, waktu):
		self.tipeRuang(tingkat)
		self.bdruang = "Cabang" + str(urcab+1) + '_' + str(self.__urutan + 1) + '_' + Aset.daftari[hari] + '_' + str(Aset.jadwal[waktu].strftime('%H'))
		
		if self.tampilTingkat() == 'Premium':
			tunjuk.execute(f"CREATE TABLE IF NOT EXISTS {self.bdruang} ({Aset.id_tabel}, {Aset.def_kolom_premium})")
			for i in range(self._baris):
				tunjuk.execute(f"INSERT INTO {self.bdruang} {Aset.kolom_premium} VALUES (%s, %s, %s, %s, %s, %s)", Aset.isi_premium)
		else:
			tunjuk.execute(f"CREATE TABLE IF NOT EXISTS {self.bdruang} ({Aset.id_tabel}, {Aset.def_kolom_reguler})")
			for i in range(self._baris):
				tunjuk.execute(f"INSERT INTO {self.bdruang} {Aset.kolom_reguler} VALUES (%s, %s, %s, %s, %s, %s, %s)", Aset.isi_reguler)
		basis.commit()
	
#Kelas yang berisikan tempat bioskop, yang merupakan turunan dari ruang yang dimiliknya
#Kelas Tempat memiliki properti 
class Tempat(Ruang):
	#inisialisasi Tempat: berisikan nama, alamat, dan jumlah studio dari bioskop
	def __init__(self, namatempat, alamat, jumstudio):
		self.__nama = str(namatempat)
		self.__alamat = str(alamat)
		self.__jumlah = int(jumstudio)
		self.__id = Aset.idLok
		Aset.daftab.append(self)
		Aset.idLok+=1
		
	def lokasi(self, namatempat, alamat, jumstudio):
		self.__nama = str(namatempat)
		self.__alamat = str(alamat)
		self.__jumlah = int(jumstudio)
	
	def tetapkanKursi(self, baris, kolom):
		super().tetapkanKursi(baris, kolom)
		basis.commit()
	
	def lihatkursi(self, baris, kolom):
		return super().lihatkursi(baris, kolom)

	def tentukanStudio(self, pilihan): 
		super().__init__(pilihan)

	def tipeRuang(self, tingkat: Tingkatan):
		super().tipeRuang(tingkat)
		self.tipe = tingkat
			
	def Studio(self):
		self._studio = []
		for i in range(self.__jumlah):
			self._studio.append([])
			for j in range(len(Aset.daftari)):
				self._studio[i].append([])
				for k in range(len(Aset.jadwal)):
					self._studio[i][j].append(Ruang(i))
	
	def filmTayang(self):
		self.Studio()
		for i in range(self.__jumlah):
			for j in range(len(Aset.daftari)):
				for k in range(len(Aset.jadwal)):
					acak = randint(0, Aset.idFilm-1)
					self._studio[i][j][k].film = Aset.dafilm[acak]
	
	def tataStudio(self, tingkat):
		self.Studio()
		for i in range(self.__jumlah):
			for j in range(len(Aset.daftari)):
				for k in range(len(Aset.jadwal)):
					self._studio[i][j][k].tataRuang(self.__id, tingkat, j, k)
					
	#metode untuk menampilkan properti (privat) dari suatu Tempat
	def tampilNama(self): return self.__nama
	def tampilAlamat(self): return self.__alamat
	def tampilJumlah(self): return self.__jumlah
	def tampilCabang(self): return self.__id
	def tampilUrutan(self): return super().tampilUrutan()
	def tampilTingkat(self): return self.tipe.tampilTingkat()
	def Uang(self, hari): return super().Uang(hari)

class Tiket(Film, Tempat):	
	def __init__(self, nama:str):
		self.namapembeli = nama
	
	def memilih(self, batas):
		pilihan = int(input("Pilihan?\t"))
		while(pilihan < 0 or pilihan > batas): 
			print("Pilihan di luar jangkauan")
			pilihan = int(input("Pilihan?\t"))
		else:
			return pilihan - 1

	def tentukanLokasi(self):
		print("\nCabang Bioskop yang buka:")
		for i in range(Aset.idLok):
			print(str(i+1) + '. ', Aset.daftab[i].tampilNama()) 
			print("   Alamat:", Aset.daftab[i].tampilAlamat(), "\t\tTipe:", Aset.daftab[i].tampilTingkat())
		self.tempat = self.memilih(Aset.idLok)
		lokasi = Aset.daftab[self.tempat]
		super().lokasi(lokasi.tampilNama(),lokasi.tampilAlamat(),lokasi.tampilJumlah())
		super().tipeRuang(lokasi.tipe)
		print(self.tampilNama())
	
	def tentukanFilm(self):
		print("\nFilm yang tersedia:")
		for i in range(Aset.idFilm):
			print(str(i+1) + '. ', Aset.dafilm[i].tampilJudul())
			print("   Durasi:", Aset.dafilm[i].tampilLama())
		film = Aset.dafilm[self.memilih(Aset.idFilm)]
		super().film(film.tampilJudul(), film.tampilLama())
		print(self.tampilJudul())

	def tentukanHari(self):
		print("\nHari:")
		for i in range(len(Aset.daftari)):
			print(str(i+1) + '.', Aset.daftari[i])
		super().tentukanHari(self.memilih(len(Aset.daftari)))
		print(self.tampilHari())
	
	def tentukanWaktu(self):
		print("\nJadwal:")
		for i in range(6):
			print(str(i+1) + '. ',Aset.jadwal[i].strftime('%H:%M'))
		super().tentukanWaktu(self.memilih(6))
		print(self.tampilWaktu())	
	
	def filmTayang(self):
		super().filmTayang()	
		for i in range(len(Aset.daftari)):
			if self.tampilHari() == Aset.daftari[i]:
				idhar = i
		print(f"\nRuang yang tersedia untuk menonton {self.tampilJudul()}")
		print(f"di {self.tampilNama()} pada hari {self.tampilHari()} pukul {self.tampilWaktu()}:")	
		no = 0
		ruangtayang = []
		for i in range(len(Aset.jadwal)):
			if self._studio[self.tempat][idhar][i].film.tampilJudul() == self.tampilJudul():
				print(str(no + 1) + ". Ruang ", str(i + 1))
				no +=1
				ruangtayang.append(i)
		return ruangtayang

	def tentukanStudio(self):
		ruangtayang = self.filmTayang()
		if len(ruangtayang) == 0:
			print(f"Maaf, film {self.tampilJudul()} tidak sedang ditayangkan di {self.tampilNama()}\n\n")
			main()
		else:
			pilihan = int(input("Pilihan?\t"))
			super().tentukanStudio(ruangtayang[pilihan-1])
			print("Ruang", self.tampilUrutan()+1)

		'''
		print("\nRuang (untuk percobaan):")
		for i in range(self.tampilJumlah()):
			print(str(i+1) + '. Ruang', i+1)
		super().tentukanStudio(self.memilih(self.tampilJumlah()))
		print("Ruang", self.tampilUrutan()+1)
		'''

	def pilihKolom(self, pilkol, lenkol):
		sedia = False
		if lenkol == 7:
			if pilkol == 'a' or pilkol == 'b' or pilkol == 'c' or pilkol == 'd' or pilkol == 'e' or pilkol == 'f':
				sedia = True
		elif lenkol == 8:
			if pilkol == 'a' or pilkol == 'b' or pilkol == 'c' or pilkol == 'd' or pilkol == 'e' or pilkol == 'f' or pilkol == 'g':
				sedia = True
		return sedia	

	def pilihKursi(self, lenkol):
		self._baris = int(input("Pilihan baris?\t"))
		if self._baris < 1 or self._baris > lenkol:
			print("Pilihan di luar jangkauan")
			self._baris = int(input("Pilihan baris?\t"))
		self._kolom = input("Pilihan kolom?\t")
		if self.pilihKolom(self._kolom, lenkol) == False:
			print("Pilihan di luar jangkauan")
			self.pilihKolom(self._kolom, lenkol)
		

	def tentukanKursi(self):
		self.__barispesanan = []
		self.__kolompesanan = []
		self.banyak = int(input("\nBanyak kursi?\t"))
		for i in range(self.banyak):
			hamparan = self.bacaRuang(self.tempat, self.tampilHari(), self.tampilWaktu())
			lenkol = len(hamparan[0])
			print("\nKursi Ruang", self.tampilUrutan()+1, self.tampilNama(), " Jadwal", self.tampilHari(), self.tampilWaktu(), ":\n ",end='')
			if lenkol == 7:
					print("  a, b, c, d, e, f ")
			elif lenkol == 8:
					print("  a, b, c, d, e, f, g ")
			for j in hamparan:
				print(j[0], j[1:])
				
			self.pilihKursi(lenkol)
			while super().lihatkursi(self._baris, self._kolom) == False:
					print (f"Kursi {self._baris}{self._kolom} telah ditempati")
					self.pilihKursi(lenkol)
			else:
				self.__barispesanan.append(self._baris)
				self.__kolompesanan.append(self._kolom)
				super().tetapkanKursi(self._baris,self._kolom)
			
	
	def penentuan(self):
		self.tentukanLokasi()
		self.tentukanFilm()
		self.tentukanHari()
		self.tentukanWaktu()
		self.tentukanStudio()
		self.tentukanKursi()

	def cetakTiket(self):
		print("\n=====================================")
		print("Nama pembeli \t:", self.namapembeli)
		print("Tiket untuk menonton")
		print("Film\t:", self.tampilJudul())
		print("Lokasi\t:", self.tampilNama())
		print("Hari\t:", self.tampilHari())
		print("Waktu\t:", self.tampilWaktu())
		print("Ruang\t:", self.tampilUrutan() + 1)
		for i in range(self.banyak):
			print("=====================================")
			print("Tiket", i + 1,)
			print("Kursi", str(self.__barispesanan[i]) + self.__kolompesanan[i])
		print("=====================================")
			
	def pembayaran(self):
		print("\nKeseluruhan biaya\t:", self.Uang(self.tampilHari()) * self.banyak)
		uang = int(input("Uang yang disetor\t: "))
		kembalian = uang - self.Uang(self.tampilHari())
		while kembalian < 0:
			print("Mohon untuk menambah", (kembalian * -1), "lagi")
			uang = int(input("Uang yang disetor\t: "))
			kembalian += uang
		else: print("Kembalian\t:", kembalian)

basis = mysql.connector.connect(host='localhost',user='root', password='', database='bioskop')		
if basis.is_connected():
	print("Terhubung ke server basis data\n")
tunjuk = basis.cursor()

Cabang1 = Tempat("Cabang 1", "Jl. Utara", 8)
Cabang2 = Tempat("Cabang 2", "Jl. Tengah", 8)
Cabang3 = Tempat("Cabang 3", "Jl. Durian", 5)

Premium = Tingkatan("Premium", 4, 6, 200000)
Reguler = Tingkatan("Reguler", 7, 7, 100000)

Cabang1.tipeRuang(Reguler)
Cabang2.tipeRuang(Reguler)
Cabang3.tipeRuang(Premium)

#Cabang1.tataStudio(Reguler)
#Cabang2.tataStudio(Reguler)
#Cabang3.tataStudio(Premium)

Film1 = Film("Film 1", 120)
Film2 = Film("Film 2", 100)
Film3 = Film("Film 3", 150)

def main():
	print("Selamat datang di aplikasi pemesanan Tiket Bioskop")
	diri = Tiket(input("Masukkan nama pembeli\t: "))
	diri.penentuan()
	diri.cetakTiket()
	diri.pembayaran()
	lanjutkah = input("Lanjut memesan tiket?(Y/selainnya)\t")
	if lanjutkah == 'Y' or lanjutkah == 'y':
		print("\n\n")
		lanjut()
	else: return 0

def lanjut():
	main()	
	
main()
