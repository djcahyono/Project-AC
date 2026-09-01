from data import load_sekolah_data

if __name__ == "__main__":
    sekolah = load_sekolah_data()
    total_ac_per_merk = sekolah.hitung_total_ac_per_merk()
    total_remot_per_merk = sekolah.hitung_total_remot_per_merk()

