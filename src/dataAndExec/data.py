from abc import ABC, abstractmethod
from contextlib import contextmanager
import hmac
from pathlib import Path
import sqlite3

# =====================================================================
# OOP Principle: Abstraction & Interface Inheritance
# =====================================================================
class FacilityEntity(ABC):
    """Abstract Base Class representing any facility element in Marsudirini school."""

    @abstractmethod
    def get_status_summary(self) -> str:
        """Polymorphic summary text describing entity status."""
        pass

    @abstractmethod
    def is_interactive(self) -> bool:
        """Determines if the entity responds to tactical click/zoom interactions."""
        pass


class FacilityRoom(dict, FacilityEntity):
    """
    Base OOP Room Class.
    Demonstrates:
    - Multiple Inheritance (inherits dict for seamless mapping compatibility + FacilityEntity)
    - Encapsulation (managed properties & internal validation)
    - Polymorphism (methods overridden in derived subclasses)
    """

    def __init__(self, name, coords, **kwargs):
        super().__init__(name=name, coords=coords, **kwargs)
        self._name = name
        self._coords = coords

    @property
    def name(self):
        """Encapsulated name getter."""
        return self.get("name", self._name)

    @property
    def coords(self):
        """Encapsulated coordinates getter."""
        return self.get("coords", self._coords)

    @property
    def temperature(self):
        """Encapsulated temperature getter."""
        return self.get("temp")

    @property
    def ac_power(self):
        """Encapsulated power state getter."""
        return self.get("acPower", "ON")

    def is_interactive(self) -> bool:
        return self.get("hasStats", True)

    def get_status_summary(self) -> str:
        return f"ROOM: {self.name} | POWER: {self.ac_power}"

    def get_theme_colors(self):
        """Polymorphic color calculation returning (fill, outline, accent)."""
        return ("#0B111D", "#1E293B", "#64748B")


class Classroom(FacilityRoom):
    """
    Subclass representing regular student classrooms equipped with AC.
    Demonstrates Inheritance and Polymorphism.
    """

    def is_interactive(self) -> bool:
        return True

    def get_status_summary(self) -> str:
        t_str = f"{self.temperature:.1f}°C" if self.temperature is not None else "--°C"
        return f"CLASSROOM {self.name} // TEMP: {t_str} // PWR: {self.ac_power}"

    def get_theme_colors(self):
        """Polymorphic implementation based on real-time temperature and power state."""
        power = str(self.ac_power).upper()
        if power == "OFF":
            return ("#131B29", "#334155", "#64748B")

        temp = self.temperature
        if temp is None:
            return ("#0E1726", "#1E293B", "#94A3B8")
        if temp >= 25:
            # Danger / Hot -> Persona Crimson alert
            return ("#2D0B14", "#FF2A42", "#FF4D6D")
        if temp >= 23:
            # Moderate -> Warm Amber
            return ("#221A08", "#F59E0B", "#FBBF24")
        # Cool / Optimal -> Electric Cyan
        return ("#061E34", "#00A2FF", "#00D2FF")


class OfficeRoom(FacilityRoom):
    """
    Subclass representing administration / faculty rooms (Ruang Guru, TU, Kepsek).
    Demonstrates Polymorphism: non-interactive and distinct stealth palette.
    """

    def is_interactive(self) -> bool:
        return False

    def get_status_summary(self) -> str:
        return f"STAFF FACILITY: {self.name}"

    def get_theme_colors(self):
        return ("#0B111D", "#1E293B", "#64748B")


class ConstructionSector(FacilityRoom):
    """
    Subclass representing sectors under construction (e.g. Floor 4).
    Demonstrates Polymorphism: specialized banner messaging.
    """

    def is_interactive(self) -> bool:
        return False

    def get_status_summary(self) -> str:
        return "MARSUDIRINI LEVEL 4 // ACCESS RESTRICTED"

    def get_theme_colors(self):
        return ("#070D18", "#00A2FF", "#00D2FF")


class FacilityReportItem:
    """
    Encapsulates an incident report record.
    Demonstrates Encapsulation with property getters and validation setters.
    """

    def __init__(self, report_id, room_name, ac_id, issue_type, description, reporter_name="Anonymous", status="PENDING", created_at=None):
        self._id = report_id
        self._room_name = room_name
        self._ac_id = ac_id
        self._issue_type = issue_type
        self._description = description
        self._reporter_name = reporter_name
        self._status = status
        self._created_at = created_at

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        valid = {"PENDING", "IN PROGRESS", "RESOLVED"}
        if str(new_status).upper() in valid:
            self._status = str(new_status).upper()
        else:
            raise ValueError(f"Invalid report status: {new_status}")

    def to_dict(self):
        return {
            "id": self._id,
            "roomName": self._room_name,
            "acId": self._ac_id,
            "issueType": self._issue_type,
            "description": self._description,
            "reporterName": self._reporter_name,
            "status": self._status,
            "createdAt": self._created_at,
        }


# =====================================================================
# OOP Principle: Inheritance & Polymorphic Editors
# =====================================================================
class _RoomEditor(ABC):
    """Abstract room editor interface."""

    def __init__(self, provider, roomName):
        self.provider = provider
        self.roomName = roomName

    @abstractmethod
    def update(self, **values):
        """Polymorphic update method."""
        pass


class _EditableRoomEditor(_RoomEditor):
    """Concrete editor for classrooms allowing data mutation."""

    def update(self, **values):
        self.provider.updateRoom(self.roomName, **values)


class _ReadOnlyRoomEditor(_RoomEditor):
    """Concrete editor for non-classroom facilities enforcing read-only access."""

    def update(self, **values):
        raise PermissionError(f"Room cannot be edited: {self.roomName}")



# Initial Data
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

    # misc
    "R. Data": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "R. Kepsek": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "R. TU": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "Ruang Guru": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False},
    "coming soon": {"temp": None, "jumlahAc": None, "merkAc": None, "remoteCount": None, "remoteBrand": None, "hasStats": False}
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
            authColumns = {
                row[1] for row in connection.execute("PRAGMA table_info(RoomAuth)")
            }
            if "room_name" in authColumns and "roomName" not in authColumns:
                connection.execute(
                    "ALTER TABLE RoomAuth RENAME COLUMN room_name TO roomName"
                )
            connection.execute("""
                CREATE TABLE IF NOT EXISTS FacilityReports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roomName TEXT NOT NULL,
                    acId TEXT,
                    issueType TEXT NOT NULL,
                    description TEXT,
                    reporterName TEXT,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                connection.execute(
                    "INSERT OR IGNORE INTO RoomAuth (roomName, password) VALUES (?, ?)",
                    (roomName, self.__roomPassword(roomName)),
                )
            connection.execute(
                "INSERT OR IGNORE INTO RoomAuth (roomName, password) VALUES (?, ?)",
                ("admin", "admin123"),
            )
            # Seed initial sample reports if table is empty
            reportCount = connection.execute("SELECT COUNT(*) as count FROM FacilityReports").fetchone()["count"]
            if reportCount == 0:
                sampleReports = [
                    ("XII A", "AC-01", "Water Leaking / Bocor Air", "Air menetes dari bagian kiri AC saat dinyalakan lama.", "Budi (XII A)", "PENDING"),
                    ("XI B", "AC-02", "AC Not Cold / Kurang Dingin", "Hembusan angin kurang dingin meski diset 18C.", "Siti (XI B)", "IN PROGRESS"),
                    ("X D", "AC-01", "Remote Missing / Rusak", "Tombol power pada remote tidak merespons.", "Pak Guru", "RESOLVED"),
                ]
                for r in sampleReports:
                    connection.execute("""
                        INSERT INTO FacilityReports (roomName, acId, issueType, description, reporterName, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, r)

    @staticmethod
    def __roomPassword(roomName):
        return f"{roomName}123"

    @staticmethod
    def __normalizeBrand(value):
        if value is None:
            return None
        return ", ".join(part.strip().capitalize() for part in str(value).split(","))

    def authenticateRoom(self, roomName, password):
        with self.connect() as connection:
            row = connection.execute(
                "SELECT password FROM RoomAuth WHERE roomName = ?", (roomName,)
            ).fetchone()
        return bool(row) and hmac.compare_digest(row["password"], password)

    def authenticateAdmin(self, password):
        with self.connect() as connection:
            row = connection.execute(
                "SELECT password FROM RoomAuth WHERE roomName = 'admin'"
            ).fetchone()
        if row and hmac.compare_digest(row["password"], password):
            return True
        return password == "admin123"

    def createReport(self, roomName, acId, issueType, description, reporterName="Anonymous"):
        with self.connect() as connection:
            cursor = connection.execute("""
                INSERT INTO FacilityReports (roomName, acId, issueType, description, reporterName, status)
                VALUES (?, ?, ?, ?, ?, 'PENDING')
            """, (roomName, acId, issueType, description, reporterName or "Anonymous"))
            return cursor.lastrowid

    def getReports(self, statusFilter=None, roomFilter=None):
        query = "SELECT * FROM FacilityReports WHERE 1=1"
        params = []
        if statusFilter and statusFilter != "ALL":
            query += " AND status = ?"
            params.append(statusFilter)
        if roomFilter and roomFilter != "ALL":
            query += " AND roomName = ?"
            params.append(roomFilter)
        query += " ORDER BY id DESC"
        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def updateReportStatus(self, reportId, newStatus):
        with self.connect() as connection:
            connection.execute(
                "UPDATE FacilityReports SET status = ? WHERE id = ?",
                (newStatus, reportId)
            )

    def deleteReport(self, reportId):
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM FacilityReports WHERE id = ?",
                (reportId,)
            )

    def getReportStats(self):
        with self.connect() as connection:
            total = connection.execute("SELECT COUNT(*) as c FROM FacilityReports").fetchone()["c"]
            pending = connection.execute("SELECT COUNT(*) as c FROM FacilityReports WHERE status = 'PENDING'").fetchone()["c"]
            in_progress = connection.execute("SELECT COUNT(*) as c FROM FacilityReports WHERE status = 'IN PROGRESS'").fetchone()["c"]
            resolved = connection.execute("SELECT COUNT(*) as c FROM FacilityReports WHERE status = 'RESOLVED'").fetchone()["c"]
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "resolved": resolved
        }

    def getRoomEditor(self, roomName):
        room = self.getRoom(roomName)
        if room and room.get("hasStats"):
            return _EditableRoomEditor(self, roomName)
        return _ReadOnlyRoomEditor(self, roomName)

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

        for key in ("acBrand", "remoteBrand"):
            if key in changes:
                changes[key] = self.__normalizeBrand(changes[key])

        assignments = ", ".join(f"{key} = ?" for key in changes)
        with self.connect() as connection:
            cursor = connection.execute(
            f"UPDATE AcCondition SET {assignments} WHERE roomName = ?",
            [*changes.values(), roomName],
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Room not found: {roomName}")

    def getFloorsData(self, floorLayout):
        """
        Polymorphically instantiates the correct FacilityRoom subclass for each room.
        - ConstructionSector  → rooms named "coming soon"
        - OfficeRoom          → rooms where hasStats is False (staff/admin areas)
        - Classroom           → all interactive student classrooms
        This is where Polymorphism is exercised: callers iterate a uniform list of
        FacilityRoom objects and call .is_interactive() / .get_theme_colors() /
        .get_status_summary() without knowing the concrete subtype.
        """
        floorsData = {}
        acNumber = 1

        for floorName, rooms in floorLayout.items():
            floorsData[floorName] = []
            for roomLayout in rooms:
                name = roomLayout["name"]
                coords = roomLayout["coords"]

                # Merge stored DB values on top of layout defaults
                kwargs = {}
                stored = self.getRoom(name)
                if stored:
                    kwargs.update({
                        "temp": stored["temperature"],
                        "status": stored["status"],
                        "acPower": stored["acPower"],
                        "jumlahAc": stored["acCount"],
                        "merkAc": stored["acBrand"],
                        "remoteCount": stored["remoteCount"],
                        "remoteBrand": stored["remoteBrand"],
                        "hasStats": bool(stored["hasStats"]),
                    })

                # Extra computed fields
                kwargs.update({
                    "acId": f"AC-{acNumber:02d}",
                    "acIds": [f"AC-{acNumber:02d}A", f"AC-{acNumber:02d}B"],
                    "acModel": kwargs.get("merkAc") or "Unknown",
                    "acCondition": "Needs service" if kwargs.get("status") == "Warning" else "Good",
                })

                # --- Polymorphic subclass selection ---
                if name.lower() == "coming soon":
                    room_obj = ConstructionSector(name, coords, **kwargs)
                elif not kwargs.get("hasStats", True):
                    room_obj = OfficeRoom(name, coords, **kwargs)
                else:
                    room_obj = Classroom(name, coords, **kwargs)

                floorsData[floorName].append(room_obj)
                acNumber += 1

        return floorsData
