""" Add Pet Window for Pet Clinic Vaccination Record System
    Provides form to add new pets with validation """

import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from models import Pet, Owner
from database import DatabaseManager
from datetime import datetime
import re

class AddPetWindow(ctk.CTkToplevel):
    # Add Pet Window class
    def __init__(self, parent, db: DatabaseManager, callback=None):
        # Initialize Add Pet window
        super().__init__(parent)
        
        self.db = db
        self.callback = callback
        
        # Window configuration
        self.title("Add New Pet")
        self.geometry("800x700")
        self.resizable(False, False)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Setup UI
        self._setup_ui()
        
        # Center window
        self._center_window()
    
    def _center_window(self):
        # Center window on screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_ui(self):
        # Setup user interface
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Add New Pet",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Pet Information Section
        pet_section = ctk.CTkLabel(
            main_frame,
            text="Pet Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pet_section.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 10))
        
        # Pet Name
        ctk.CTkLabel(main_frame, text="Pet Name: *").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = ctk.CTkEntry(main_frame, width=300)
        self.name_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        # Species
        ctk.CTkLabel(main_frame, text="Species: *").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.species_var = ctk.StringVar(value="Dog")
        self.species_menu = ctk.CTkOptionMenu(
            main_frame,
            variable=self.species_var,
            values=["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Guinea Pig", "Other"],
            width=300
        )
        self.species_menu.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        
        # Breed
        ctk.CTkLabel(main_frame, text="Breed:").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.breed_entry = ctk.CTkEntry(main_frame, width=300)
        self.breed_entry.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        
        # Date of Birth
        ctk.CTkLabel(main_frame, text="Date of Birth:").grid(row=5, column=0, sticky="w", pady=5, padx=5)
        self.dob_entry = DateEntry(
            main_frame,
            width=40,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.dob_entry.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        
        # Gender
        ctk.CTkLabel(main_frame, text="Gender:").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.gender_var = ctk.StringVar(value="Male")
        self.gender_menu = ctk.CTkOptionMenu(
            main_frame,
            variable=self.gender_var,
            values=["Male", "Female", "Unknown"],
            width=300
        )
        self.gender_menu.grid(row=6, column=1, pady=5, padx=5, sticky="w")
        
        # Color
        ctk.CTkLabel(main_frame, text="Color:").grid(row=7, column=0, sticky="w", pady=5, padx=5)
        self.color_entry = ctk.CTkEntry(main_frame, width=300)
        self.color_entry.grid(row=7, column=1, pady=5, padx=5, sticky="w")
        
        # Pet ID
        ctk.CTkLabel(main_frame, text="Pet ID:").grid(row=8, column=0, sticky="w", pady=5, padx=5)
        self.microchip_entry = ctk.CTkEntry(main_frame, width=300)
        self.microchip_entry.grid(row=8, column=1, pady=5, padx=5, sticky="w")
        
        # Owner Information Section
        owner_section = ctk.CTkLabel(
            main_frame,
            text="Owner Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        owner_section.grid(row=9, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        # Owner Name
        ctk.CTkLabel(main_frame, text="Owner Name: *").grid(row=10, column=0, sticky="w", pady=5, padx=5)
        self.owner_name_entry = ctk.CTkEntry(main_frame, width=300)
        self.owner_name_entry.grid(row=10, column=1, pady=5, padx=5, sticky="w")
        
        # Owner Phone
        ctk.CTkLabel(main_frame, text="Owner Phone: *").grid(row=11, column=0, sticky="w", pady=5, padx=5)
        self.owner_phone_entry = ctk.CTkEntry(main_frame, width=300)
        self.owner_phone_entry.grid(row=11, column=1, pady=5, padx=5, sticky="w")
        
        # Owner Email
        ctk.CTkLabel(main_frame, text="Owner Email:").grid(row=12, column=0, sticky="w", pady=5, padx=5)
        self.owner_email_entry = ctk.CTkEntry(main_frame, width=300)
        self.owner_email_entry.grid(row=12, column=1, pady=5, padx=5, sticky="w")
        
        # Owner Address
        ctk.CTkLabel(main_frame, text="Owner Address:").grid(row=13, column=0, sticky="w", pady=5, padx=5)
        self.owner_address_entry = ctk.CTkTextbox(main_frame, width=300, height=60)
        self.owner_address_entry.grid(row=13, column=1, pady=5, padx=5, sticky="w")
        
        # Notes
        ctk.CTkLabel(main_frame, text="Notes:").grid(row=14, column=0, sticky="w", pady=5, padx=5)
        self.notes_entry = ctk.CTkTextbox(main_frame, width=300, height=80)
        self.notes_entry.grid(row=14, column=1, pady=5, padx=5, sticky="w")
        
        # Required fields note
        required_note = ctk.CTkLabel(
            main_frame,
            text="* Required fields",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        required_note.grid(row=15, column=0, columnspan=2, pady=(10, 5))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=16, column=0, columnspan=2, pady=(20, 10))
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Save Pet",
            command=self._save_pet,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.save_btn.grid(row=0, column=0, padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            width=150,
            height=40,
            fg_color="gray",
            font=ctk.CTkFont(size=14)
        )
        self.cancel_btn.grid(row=0, column=1, padx=10)
    
    def _validate_email(self, email: str) -> bool:
        # Validate email format
        if not email:
            return True  # Email is optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _validate_phone(self, phone: str) -> bool:
        # Validate phone number
        if not phone.strip():
            return False
        # Allow various phone formats
        return len(phone.strip()) >= 7
    
    def _validate_form(self) -> tuple[bool, str]:
        # Validate form
        # Pet name
        if not self.name_entry.get().strip():
            return False, "Pet name is required"
        
        # Species
        if not self.species_var.get().strip():
            return False, "Species is required"
        
        # Owner name
        if not self.owner_name_entry.get().strip():
            return False, "Owner name is required"
        
        # Owner phone
        if not self._validate_phone(self.owner_phone_entry.get()):
            return False, "Valid owner phone is required"
        
        # Owner email (if provided)
        email = self.owner_email_entry.get().strip()
        if email and not self._validate_email(email):
            return False, "Invalid email format"
        
        return True, ""
    
    def _save_pet(self):
        # Save pet to database
        is_valid, error_msg = self._validate_form()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        try:
            # Create or get owner
            owner_name = self.owner_name_entry.get().strip()
            owner_phone = self.owner_phone_entry.get().strip()
            owner_email = self.owner_email_entry.get().strip()
            owner_address = self.owner_address_entry.get("1.0", "end-1c").strip()
            
            owner = Owner(
                name=owner_name,
                phone=owner_phone,
                email=owner_email,
                address=owner_address
            )
            
            owner_id = self.db.create_owner(owner)
            
            # Create Pet object with owner_id
            pet = Pet(
                name=self.name_entry.get().strip(),
                species=self.species_var.get(),
                breed=self.breed_entry.get().strip(),
                date_of_birth=self.dob_entry.get_date().strftime("%Y-%m-%d"),
                gender=self.gender_var.get(),
                color=self.color_entry.get().strip(),
                owner_id=owner_id,
                microchip_number=self.microchip_entry.get().strip(),
                registration_date=datetime.now().strftime("%Y-%m-%d"),
                notes=self.notes_entry.get("1.0", "end-1c").strip()
            )
            
            # Save to database
            pet_id = self.db.create_pet(pet)
            
            messagebox.showinfo(
                "Success",
                f"Pet '{pet.name}' added successfully!\nPet ID: {pet_id}"
            )
            
            # Refresh parent window if callback provided
            if self.callback:
                self.callback()
            
            # Close window
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error saving pet: {str(e)}")
