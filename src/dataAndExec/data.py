#placeholder database and stuff
ROOM_DATA = {
    "XII G": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "XII F": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "R. Data": {"temp": None, "status": None, "ac_power": None, "has_stats": False},
    "XII E": {"temp": 71, "status": "Cooling", "ac_power": "ON"},
    "XII D": {"temp": 73, "status": "Cooling", "ac_power": "ON"},
    "XII C": {"temp": 75, "status": "Eco", "ac_power": "ON"},
    "XII B": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "XII A": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "R. Kepsek": {"temp": None, "status": None, "ac_power": None, "has_stats": False},
    "R. TU": {"temp": 72, "status": "Cooling", "ac_power": "ON", "has_stats": False},
    "XII H": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "XII I": {"temp": 71, "status": "Cooling", "ac_power": "ON"},
    "XI G": {"temp": 74, "status": "Eco", "ac_power": "ON"},
    "XI F": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "XI E": {"temp": 73, "status": "Cooling", "ac_power": "ON"},
    "Ruang guru": {"temp": None, "status": None, "ac_power": None, "has_stats": False},
    "XI D": {"temp": 75, "status": "Warning", "ac_power": "ON"},
    "XI A": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "XI B": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "XI C": {"temp": 74, "status": "Eco", "ac_power": "ON"},
    "XI H": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "XI I": {"temp": 71, "status": "Cooling", "ac_power": "ON"},
    "X A": {"temp": 73, "status": "Cooling", "ac_power": "ON"},
    "X B": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "X C": {"temp": 71, "status": "Cooling", "ac_power": "ON"},
    "X D": {"temp": 74, "status": "Eco", "ac_power": "ON"},
    "X E": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "X F": {"temp": 73, "status": "Cooling", "ac_power": "ON"},
    "R. Heru": {"temp": 68, "status": "Cooling", "ac_power": "OFF", "has_stats": False},
    "X I": {"temp": 70, "status": "Cooling", "ac_power": "ON"},
    "X H": {"temp": 72, "status": "Cooling", "ac_power": "ON"},
    "X G": {"temp": 74, "status": "Cooling", "ac_power": "ON"},
    "coming soon": {"temp": None, "status": None, "ac_power": None, "has_stats" : False}
}


class RoomDataProvider:
#database stuff

    def __init__(self, room_data=None):
        self._room_data = room_data if room_data is not None else ROOM_DATA

    def get_floors_data(self, floor_layout):
        floors_data = {}
        ac_number = 1

        for floor_name, rooms in floor_layout.items():
            floors_data[floor_name] = []
            for room_layout in rooms:
                room = dict(room_layout)
                room.update(self._room_data.get(room["name"], {}))
                room.update({
                    "ac_id": f"AC-{ac_number:02d}",
                    "ac_ids": [f"AC-{ac_number:02d}A", f"AC-{ac_number:02d}B"],
                    "ac_model": "Daikin Inverter",
                    "ac_condition": "Needs service" if room.get("status") == "Warning" else "Good",
                })
                floors_data[floor_name].append(room)
                ac_number += 1

        return floors_data


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
