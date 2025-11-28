# Database Manager for Pet Clinic Vaccination Record System

import sqlite3
from typing import List, Optional, Tuple
from models import Pet, Vaccination
import os


class DatabaseManager:
    _instance = None
    
    def __new__(cls, db_name: str = "pet_clinic.db"):
        # Implement Singleton pattern
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_name: str = "pet_clinic.db"):
        # database connection and create tables
        if self._initialized:
            return
        
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._connect()
        self._create_tables()
        self._initialized = True
    
    def _connect(self):
        # connect database connection
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            # foreign key support
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")
    
    def _create_tables(self):
        # Create database tables from schema
        try:
            # Read and execute schema file
            schema_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                    self.cursor.executescript(schema_sql)
            else:
                # Create tables inline if schema file doesn't exist
                self._create_tables_inline()
            
            self.connection.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error creating tables: {e}")
    
    def _create_tables_inline(self):
        # Create tables inline
        pet_table = """
        CREATE TABLE IF NOT EXISTS Pet (
            pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            breed TEXT,
            date_of_birth DATE,
            gender TEXT,
            color TEXT,
            owner_name TEXT NOT NULL,
            owner_phone TEXT NOT NULL,
            owner_email TEXT,
            owner_address TEXT,
            microchip_number TEXT UNIQUE,
            registration_date DATE DEFAULT CURRENT_DATE,
            notes TEXT,
            is_active INTEGER DEFAULT 1
        )
        """
        
        vaccination_table = """
        CREATE TABLE IF NOT EXISTS Vaccination (
            vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER NOT NULL,
            vaccine_name TEXT NOT NULL,
            vaccination_date DATE NOT NULL,
            next_due_date DATE,
            veterinarian_name TEXT,
            batch_number TEXT,
            manufacturer TEXT,
            dose_number INTEGER,
            site_administered TEXT,
            adverse_reactions TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES Pet(pet_id) ON DELETE CASCADE
        )
        """
        
        self.cursor.execute(pet_table)
        self.cursor.execute(vaccination_table)
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_pet_owner ON Pet(owner_name)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_vaccination_pet ON Vaccination(pet_id)")
    
    def close(self):
        # Close database connection
        if self.connection:
            self.connection.close()
    
    # ==================== PET CRUD OPERATIONS ====================
    
    def create_pet(self, pet: Pet) -> int:
        # Create a new pet record
        try:
            query = """
            INSERT INTO Pet (name, species, breed, date_of_birth, gender, color,
                        owner_name, owner_phone, owner_email, owner_address,
                        microchip_number, registration_date, notes, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(query, (
                pet.name, pet.species, pet.breed, pet.date_of_birth,
                pet.gender, pet.color, pet.owner_name, pet.owner_phone,
                pet.owner_email, pet.owner_address, pet.microchip_number,
                pet.registration_date, pet.notes, pet.is_active
            ))
            
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise Exception(f"Integrity error: {e}")
        except sqlite3.Error as e:
            raise Exception(f"Error creating pet: {e}")
    
    def read_pet(self, pet_id: int) -> Optional[Pet]:
        # Read a pet record by ID
        try:
            query = "SELECT * FROM Pet WHERE pet_id = ?"
            self.cursor.execute(query, (pet_id,))
            row = self.cursor.fetchone()
            
            if row:
                return self._row_to_pet(row)
            return None
        except sqlite3.Error as e:
            raise Exception(f"Error reading pet: {e}")
    
    def read_all_pets(self, active_only: bool = True) -> List[Pet]:
        # Read all pet records
        try:
            if active_only:
                query = "SELECT * FROM Pet WHERE is_active = 1 ORDER BY name"
            else:
                query = "SELECT * FROM Pet ORDER BY name"
            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            return [self._row_to_pet(row) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Error reading pets: {e}")
    
    def update_pet(self, pet: Pet) -> bool:
        # Update an existing pet record
        try:
            query = """
            UPDATE Pet SET name = ?, species = ?, breed = ?, date_of_birth = ?,
                        gender = ?, color = ?, owner_name = ?, owner_phone = ?,
                        owner_email = ?, owner_address = ?, microchip_number = ?,
                        notes = ?, is_active = ?
            WHERE pet_id = ?
            """
            
            self.cursor.execute(query, (
                pet.name, pet.species, pet.breed, pet.date_of_birth,
                pet.gender, pet.color, pet.owner_name, pet.owner_phone,
                pet.owner_email, pet.owner_address, pet.microchip_number,
                pet.notes, pet.is_active, pet.pet_id
            ))
            
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            raise Exception(f"Integrity error: {e}")
        except sqlite3.Error as e:
            raise Exception(f"Error updating pet: {e}")
    
    def delete_pet(self, pet_id: int) -> bool:
        # Delete a pet record (also deletes associated vaccinations due to CASCADE)
        try:
            query = "DELETE FROM Pet WHERE pet_id = ?"
            self.cursor.execute(query, (pet_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error deleting pet: {e}")
    
    def soft_delete_pet(self, pet_id: int) -> bool:
        # Soft delete a pet
        try:
            query = "UPDATE Pet SET is_active = 0 WHERE pet_id = ?"
            self.cursor.execute(query, (pet_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error soft deleting pet: {e}")
    
    def search_pets(self, search_term: str) -> List[Pet]:
        # Search pets by name, species, or owner name
        try:
            query = """
            SELECT * FROM Pet 
            WHERE (name LIKE ? OR species LIKE ? OR owner_name LIKE ?) 
            AND is_active = 1
            ORDER BY name
            """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            rows = self.cursor.fetchall()
            
            return [self._row_to_pet(row) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Error searching pets: {e}")
    
    # CRUD OPERATIONS
    
    def create_vaccination(self, vaccination: Vaccination) -> int:
        # Create a new vaccination record
        try:
            query = """
            INSERT INTO Vaccination (pet_id, vaccine_name, vaccination_date, next_due_date,
                                veterinarian_name, batch_number, manufacturer, dose_number,
                                site_administered, adverse_reactions, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.cursor.execute(query, (
                vaccination.pet_id, vaccination.vaccine_name, vaccination.vaccination_date,
                vaccination.next_due_date, vaccination.veterinarian_name, vaccination.batch_number,
                vaccination.manufacturer, vaccination.dose_number, vaccination.site_administered,
                vaccination.adverse_reactions, vaccination.notes
            ))
            
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            raise Exception(f"Error creating vaccination: {e}")
    
    def read_vaccination(self, vaccination_id: int) -> Optional[Vaccination]:
        # Read a vaccination record by ID
        try:
            query = "SELECT * FROM Vaccination WHERE vaccination_id = ?"
            self.cursor.execute(query, (vaccination_id,))
            row = self.cursor.fetchone()
            
            if row:
                return self._row_to_vaccination(row)
            return None
        except sqlite3.Error as e:
            raise Exception(f"Error reading vaccination: {e}")
    
    def read_vaccinations_by_pet(self, pet_id: int) -> List[Vaccination]:
        # Read all vaccination records for a specific pet
        try:
            query = "SELECT * FROM Vaccination WHERE pet_id = ? ORDER BY vaccination_date DESC"
            self.cursor.execute(query, (pet_id,))
            rows = self.cursor.fetchall()
            
            return [self._row_to_vaccination(row) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Error reading vaccinations: {e}")
    
    def read_all_vaccinations(self) -> List[Vaccination]:
        # Read all vaccination records
        try:
            query = "SELECT * FROM Vaccination ORDER BY vaccination_date DESC"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            return [self._row_to_vaccination(row) for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Error reading all vaccinations: {e}")
    
    def update_vaccination(self, vaccination: Vaccination) -> bool:
        # Update an existing vaccination record
        try:
            query = """
            UPDATE Vaccination SET pet_id = ?, vaccine_name = ?, vaccination_date = ?,
                                next_due_date = ?, veterinarian_name = ?, batch_number = ?,
                                manufacturer = ?, dose_number = ?, site_administered = ?,
                                adverse_reactions = ?, notes = ?
            WHERE vaccination_id = ?
            """
            
            self.cursor.execute(query, (
                vaccination.pet_id, vaccination.vaccine_name, vaccination.vaccination_date,
                vaccination.next_due_date, vaccination.veterinarian_name, vaccination.batch_number,
                vaccination.manufacturer, vaccination.dose_number, vaccination.site_administered,
                vaccination.adverse_reactions, vaccination.notes, vaccination.vaccination_id
            ))
            
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error updating vaccination: {e}")
    
    def delete_vaccination(self, vaccination_id: int) -> bool:
        # Delete a vaccination record
        try:
            query = "DELETE FROM Vaccination WHERE vaccination_id = ?"
            self.cursor.execute(query, (vaccination_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error deleting vaccination: {e}")
    
    def get_upcoming_vaccinations(self, days: int = 30) -> List[Tuple]:
        # Get vaccinations due within specified days
        try:
            query = """
            SELECT p.name, v.vaccine_name, v.next_due_date, p.owner_name, p.owner_phone
            FROM Vaccination v
            JOIN Pet p ON v.pet_id = p.pet_id
            WHERE v.next_due_date IS NOT NULL 
            AND v.next_due_date <= date('now', '+' || ? || ' days')
            AND v.next_due_date >= date('now')
            AND p.is_active = 1
            ORDER BY v.next_due_date
            """
            self.cursor.execute(query, (days,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error getting upcoming vaccinations: {e}")
    
    # STATISTICS AND REPORTS 
    
    def get_pet_count(self) -> int:
        # Get total number of active pets
        try:
            query = "SELECT COUNT(*) FROM Pet WHERE is_active = 1"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise Exception(f"Error getting pet count: {e}")
    
    def get_vaccination_count(self) -> int:
        # Get total number of vaccinations
        try:
            query = "SELECT COUNT(*) FROM Vaccination"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise Exception(f"Error getting vaccination count: {e}")
    
    def get_species_distribution(self) -> List[Tuple]:
        # Get distribution of pets by species
        try:
            query = """
            SELECT species, COUNT(*) as count 
            FROM Pet 
            WHERE is_active = 1
            GROUP BY species 
            ORDER BY count DESC
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error getting species distribution: {e}")
    
    # HELPER METHODS
    
    def _row_to_pet(self, row) -> Pet:
        # Convert database row to Pet object
        return Pet(
            pet_id=row['pet_id'],
            name=row['name'],
            species=row['species'],
            breed=row['breed'] or "",
            date_of_birth=row['date_of_birth'] or "",
            gender=row['gender'] or "",
            color=row['color'] or "",
            owner_name=row['owner_name'],
            owner_phone=row['owner_phone'],
            owner_email=row['owner_email'] or "",
            owner_address=row['owner_address'] or "",
            microchip_number=row['microchip_number'] or "",
            registration_date=row['registration_date'] or "",
            notes=row['notes'] or "",
            is_active=row['is_active']
        )
    
    def _row_to_vaccination(self, row) -> Vaccination:
        # Convert database row to Vaccination object
        return Vaccination(
            vaccination_id=row['vaccination_id'],
            pet_id=row['pet_id'],
            vaccine_name=row['vaccine_name'],
            vaccination_date=row['vaccination_date'],
            next_due_date=row['next_due_date'] or "",
            veterinarian_name=row['veterinarian_name'] or "",
            batch_number=row['batch_number'] or "",
            manufacturer=row['manufacturer'] or "",
            dose_number=row['dose_number'] or 1,
            site_administered=row['site_administered'] or "",
            adverse_reactions=row['adverse_reactions'] or "",
            notes=row['notes'] or ""
        )
