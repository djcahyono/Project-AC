from contextlib import contextmanager
from pathlib import Path
import sqlite3
#Initial Data
InitialRoomData = {
    # Kelas 10
    "X A": {"temp": 24, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "X B": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "X C": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "X D": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "X E": {"temp": 21, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "X F": {"temp": 24, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "X G": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "X H": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 1, "remoteBrand": "Mitsubishi"},
    "X I": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},

    # Kelas 11
    "XI A": {"temp": 20, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XI B": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "XI C": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XI D": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XI E": {"temp": 26, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 0, "remoteBrand": "None"},
    "XI F": {"temp": 24, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XI G": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Mitsubishi, Universal"},
    "XI H": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XI I": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},

    # Kelas 12
    "XII A": {"temp": 20, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XII B": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Panasonic, Mitsubishi"},
    "XII C": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XII D": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XII E": {"temp": 25, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XII F": {"temp": 24, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},
    "XII G": {"temp": None, "jumlahAc": None, "merkAc": "Belum pasti", "remoteCount": None, "remoteBrand": None},
    "XII H": {"temp": 22, "jumlahAc": 2, "merkAc": "Panasonic, Mitsubishi", "remoteCount": 2, "remoteBrand": "Mitsubishi, Universal"},
    "XII I": {"temp": 23, "jumlahAc": 2, "merkAc": "Panasonic", "remoteCount": 1, "remoteBrand": "Panasonic"},

    #misc
    "R. Data": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "R. Kepsek": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "R. TU": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "Ruang Guru": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False}
}

databasePath = Path(__file__).resolve().parents[2] / "facilityData.db"


class RoomDataProvider:
    def __init__(self, databasePath=databasePath, roomData=None):
        self.databasePath = Path(databasePath)
        self.roomData = roomData if roomData is not None else InitialRoomData
        self.createTables()
        self.seedInitialData()

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.databasePath)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def createTables(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS AcCondition (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roomName TEXT UNIQUE NOT NULL,
                    temperature REAL,
                    status TEXT,
                    acPower TEXT,
                    acCount INTEGER,
                    acBrand TEXT,
                    remoteCount INTEGER,
                    remoteBrand TEXT,
                    hasStats INTEGER NOT NULL DEFAULT 1
                )
            """)
            existingColumns = {
                row[1] for row in connection.execute("PRAGMA table_info(AcCondition)")
            }
            legacyColumns = {
                "room_name": "roomName",
                "ac_power": "acPower",
                "ac_count": "acCount",
                "ac_brand": "acBrand",
                "remote_count": "remoteCount",
                "remote_brand": "remoteBrand",
                "has_stats": "hasStats",
            }
            for oldName, newName in legacyColumns.items():
                if oldName in existingColumns and newName not in existingColumns:
                    connection.execute(
                        f"ALTER TABLE AcCondition RENAME COLUMN {oldName} TO {newName}"
                    )
            connection.execute("""
                CREATE TABLE IF NOT EXISTS RoomAuth (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roomName TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

    def seedInitialData(self):
        with self.connect() as connection:
            for roomName, values in self.roomData.items():
                connection.execute("""
                    INSERT OR IGNORE INTO AcCondition
                    (roomName, temperature, status, acPower, acCount,
                     acBrand, remoteCount, remoteBrand, hasStats)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    roomName,
                    values.get("temp"),
                    values.get("status"),
                    values.get("acPower", "ON"),
                    values.get("jumlahAc"),
                    values.get("merkAc"),
                    values.get("remoteCount"),
                    values.get("remoteBrand"),
                    int(values.get("hasStats", True)),
                ))

    def getRoom(self, roomName):
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM AcCondition WHERE roomName = ?", (roomName,)
            ).fetchone()
        return dict(row) if row else None

    def updateRoom(self, roomName, **values):
        allowed = {
            "temperature", "status", "acPower", "acCount", "acBrand",
            "remoteCount", "remoteBrand", "hasStats",
        }
        changes = {key: value for key, value in values.items() if key in allowed}
        if not changes:
            raise ValueError("No valid room fields were provided")

        assignments = ", ".join(f"{key} = ?" for key in changes)
        with self.connect() as connection:
            cursor = connection.execute(
            f"UPDATE AcCondition SET {assignments} WHERE roomName = ?",
            [*changes.values(), roomName],
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Room not found: {roomName}")

    def getFloorsData(self, floorLayout):
        floorsData = {}
        acNumber = 1

        for floorName, rooms in floorLayout.items():
            floorsData[floorName] = []
            for roomLayout in rooms:
                room = dict(roomLayout)
                stored = self.getRoom(room["name"])
                if stored:
                    room.update({
                        "temp": stored["temperature"],
                        "status": stored["status"],
                        "acPower": stored["acPower"],
                        "jumlahAc": stored["acCount"],
                        "merkAc": stored["acBrand"],
                        "remoteCount": stored["remoteCount"],
                        "remoteBrand": stored["remoteBrand"],
                        "hasStats": bool(stored["hasStats"]),
                    })
                room.update({
                    "acId": f"AC-{acNumber:02d}",
                    "acIds": [f"AC-{acNumber:02d}A", f"AC-{acNumber:02d}B"],
                    "acModel": room.get("merkAc") or "Unknown",
                    "acCondition": "Needs service" if room.get("status") == "Warning" else "Good",
                })
                floorsData[floorName].append(room)
                acNumber += 1

        return floorsData
