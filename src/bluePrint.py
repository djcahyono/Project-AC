class ACKelas:

    def __init__(self, suhuDinding, jumlahAC, merkAC, jumlahRemot, merkRemot):
        self.suhuDinding = suhuDinding
        self.jumlahAC = jumlahAC
        self.merkAC = merkAC
        self.jumlahRemot = jumlahRemot
        self.merkRemot = merkRemot


class GedungSekolah:

    def __init__(self, daftar_kelas=None):
        self.daftar_kelas = daftar_kelas if daftar_kelas is not None else {}

    def tambah_kelas(self, nama_kelas, ac_kelas_obj):
        self.daftar_kelas[nama_kelas] = ac_kelas_obj

    def hitung_total_ac_per_merk(self):
        total_per_merk = {}
        for kelas in self.daftar_kelas.values():
            merk = kelas.merkAC
            jumlah = kelas.jumlahAC
            total_per_merk[merk] = total_per_merk.get(merk, 0) + jumlah
        return total_per_merk
    def hitung_total_remot_per_merk(self): 
        total_per_merk = {}
        for kelas in self.daftar_kelas.values():
            merk = kelas.merkRemot
            jumlah = kelas.jumlahRemot
            total_per_merk[merk] = total_per_merk.get(merk, 0) + jumlah
        return total_per_merk