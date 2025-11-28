# Model Classes for Pet Clinic Vaccination Record System

from datetime import datetime
from typing import Optional


class Pet:
    # Pet model class representing a pet entity
    def __init__(self, pet_id: Optional[int] = None, name: str = "", species: str = "",
                breed: str = "", date_of_birth: str = "", gender: str = "",
                color: str = "", owner_name: str = "", owner_phone: str = "",
                owner_email: str = "", owner_address: str = "", 
                microchip_number: str = "", registration_date: str = "",
                notes: str = "", is_active: int = 1):
        # Initialize Pet object with validation
        self._pet_id = pet_id
        self._name = name
        self._species = species
        self._breed = breed
        self._date_of_birth = date_of_birth
        self._gender = gender
        self._color = color
        self._owner_name = owner_name
        self._owner_phone = owner_phone
        self._owner_email = owner_email
        self._owner_address = owner_address
        self._microchip_number = microchip_number
        self._registration_date = registration_date or datetime.now().strftime("%Y-%m-%d")
        self._notes = notes
        self._is_active = is_active
    
    # Getters and Setters
    @property
    def pet_id(self) -> Optional[int]:
        return self._pet_id
    
    @pet_id.setter
    def pet_id(self, value: int):
        self._pet_id = value
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Pet name cannot be empty")
        self._name = value.strip()
    
    @property
    def species(self) -> str:
        return self._species
    
    @species.setter
    def species(self, value: str):
        if not value.strip():
            raise ValueError("Species cannot be empty")
        self._species = value.strip()
    
    @property
    def breed(self) -> str:
        return self._breed
    
    @breed.setter
    def breed(self, value: str):
        self._breed = value.strip()
    
    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth
    
    @date_of_birth.setter
    def date_of_birth(self, value: str):
        self._date_of_birth = value
    
    @property
    def gender(self) -> str:
        return self._gender
    
    @gender.setter
    def gender(self, value: str):
        self._gender = value
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str):
        self._color = value.strip()
    
    @property
    def owner_name(self) -> str:
        return self._owner_name
    
    @owner_name.setter
    def owner_name(self, value: str):
        if not value.strip():
            raise ValueError("Owner name cannot be empty")
        self._owner_name = value.strip()
    
    @property
    def owner_phone(self) -> str:
        return self._owner_phone
    
    @owner_phone.setter
    def owner_phone(self, value: str):
        if not value.strip():
            raise ValueError("Owner phone cannot be empty")
        self._owner_phone = value.strip()
    
    @property
    def owner_email(self) -> str:
        return self._owner_email
    
    @owner_email.setter
    def owner_email(self, value: str):
        self._owner_email = value.strip()
    
    @property
    def owner_address(self) -> str:
        return self._owner_address
    
    @owner_address.setter
    def owner_address(self, value: str):
        self._owner_address = value.strip()
    
    @property
    def microchip_number(self) -> str:
        return self._microchip_number
    
    @microchip_number.setter
    def microchip_number(self, value: str):
        self._microchip_number = value.strip()
    
    @property
    def registration_date(self) -> str:
        return self._registration_date
    
    @registration_date.setter
    def registration_date(self, value: str):
        self._registration_date = value
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, value: str):
        self._notes = value.strip()
    
    @property
    def is_active(self) -> int:
        return self._is_active
    
    @is_active.setter
    def is_active(self, value: int):
        self._is_active = value
    
    def to_dict(self) -> dict:
        # Convert Pet object to dictionary
        return {
            'pet_id': self._pet_id,
            'name': self._name,
            'species': self._species,
            'breed': self._breed,
            'date_of_birth': self._date_of_birth,
            'gender': self._gender,
            'color': self._color,
            'owner_name': self._owner_name,
            'owner_phone': self._owner_phone,
            'owner_email': self._owner_email,
            'owner_address': self._owner_address,
            'microchip_number': self._microchip_number,
            'registration_date': self._registration_date,
            'notes': self._notes,
            'is_active': self._is_active
        }
    
    def __str__(self) -> str:
        # String representation of Pet
        return f"Pet(ID: {self._pet_id}, Name: {self._name}, Species: {self._species}, Owner: {self._owner_name})"


class Vaccination:
    # Vaccination model class representing a vaccination record
    def __init__(self, vaccination_id: Optional[int] = None, pet_id: int = 0,
                vaccine_name: str = "", vaccination_date: str = "",
                next_due_date: str = "", veterinarian_name: str = "",
                batch_number: str = "", manufacturer: str = "",
                dose_number: int = 1, site_administered: str = "",
                adverse_reactions: str = "", notes: str = ""):
        # Initialize Vaccination object with validation
        self._vaccination_id = vaccination_id
        self._pet_id = pet_id
        self._vaccine_name = vaccine_name
        self._vaccination_date = vaccination_date
        self._next_due_date = next_due_date
        self._veterinarian_name = veterinarian_name
        self._batch_number = batch_number
        self._manufacturer = manufacturer
        self._dose_number = dose_number
        self._site_administered = site_administered
        self._adverse_reactions = adverse_reactions
        self._notes = notes
    
    # Getters and Setters
    @property
    def vaccination_id(self) -> Optional[int]:
        return self._vaccination_id
    
    @vaccination_id.setter
    def vaccination_id(self, value: int):
        self._vaccination_id = value
    
    @property
    def pet_id(self) -> int:
        return self._pet_id
    
    @pet_id.setter
    def pet_id(self, value: int):
        if value <= 0:
            raise ValueError("Pet ID must be a positive integer")
        self._pet_id = value
    
    @property
    def vaccine_name(self) -> str:
        return self._vaccine_name
    
    @vaccine_name.setter
    def vaccine_name(self, value: str):
        if not value.strip():
            raise ValueError("Vaccine name cannot be empty")
        self._vaccine_name = value.strip()
    
    @property
    def vaccination_date(self) -> str:
        return self._vaccination_date
    
    @vaccination_date.setter
    def vaccination_date(self, value: str):
        if not value:
            raise ValueError("Vaccination date cannot be empty")
        self._vaccination_date = value
    
    @property
    def next_due_date(self) -> str:
        return self._next_due_date
    
    @next_due_date.setter
    def next_due_date(self, value: str):
        self._next_due_date = value
    
    @property
    def veterinarian_name(self) -> str:
        return self._veterinarian_name
    
    @veterinarian_name.setter
    def veterinarian_name(self, value: str):
        self._veterinarian_name = value.strip()
    
    @property
    def batch_number(self) -> str:
        return self._batch_number
    
    @batch_number.setter
    def batch_number(self, value: str):
        self._batch_number = value.strip()
    
    @property
    def manufacturer(self) -> str:
        return self._manufacturer
    
    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value.strip()
    
    @property
    def dose_number(self) -> int:
        return self._dose_number
    
    @dose_number.setter
    def dose_number(self, value: int):
        if value < 1:
            raise ValueError("Dose number must be at least 1")
        self._dose_number = value
    
    @property
    def site_administered(self) -> str:
        return self._site_administered
    
    @site_administered.setter
    def site_administered(self, value: str):
        self._site_administered = value.strip()
    
    @property
    def adverse_reactions(self) -> str:
        return self._adverse_reactions
    
    @adverse_reactions.setter
    def adverse_reactions(self, value: str):
        self._adverse_reactions = value.strip()
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, value: str):
        self._notes = value.strip()
    
    def to_dict(self) -> dict:
        # Convert Vaccination object to dictionary
        return {
            'vaccination_id': self._vaccination_id,
            'pet_id': self._pet_id,
            'vaccine_name': self._vaccine_name,
            'vaccination_date': self._vaccination_date,
            'next_due_date': self._next_due_date,
            'veterinarian_name': self._veterinarian_name,
            'batch_number': self._batch_number,
            'manufacturer': self._manufacturer,
            'dose_number': self._dose_number,
            'site_administered': self._site_administered,
            'adverse_reactions': self._adverse_reactions,
            'notes': self._notes
        }
    
    def __str__(self) -> str:
        # String representation of Vaccination
        return f"Vaccination(ID: {self._vaccination_id}, Pet ID: {self._pet_id}, Vaccine: {self._vaccine_name}, Date: {self._vaccination_date})"
