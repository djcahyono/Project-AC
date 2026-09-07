class ACKelas:
# main data class 
    def __init__(self, suhuDinding, jumlahAC, merkAC, jumlahRemot, merkRemot):
        self.suhuDinding = suhuDinding
        self.jumlahAC = jumlahAC
        self.merkAC = merkAC
        self.jumlahRemot = jumlahRemot
        self.merkRemot = merkRemot
 

class kondisiKelas:
    def __init__(self):
        self.daftar_kelas = {
            # Contoh data kelas (isi nanti)
            "Example": ACKelas(
                suhuDinding=30,
                jumlahAC=2,
                merkAC="Daikin",
                jumlahRemot=2,
                merkRemot="Daikin"
            )
        }
    # update situation of the class (for data manipulation)
    def tambah_kelas(self, nama_kelas, ac_kelas_obj):
        self.daftar_kelas[nama_kelas] = ac_kelas_obj
sekolah = kondisiKelas()
