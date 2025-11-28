# Update Pet Window for Pet Clinic Vaccination Record System

import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from models import Pet
from database import DatabaseManager
from datetime import datetime
import re


class UpdatePetWindow(ctk.CTkToplevel):
    # Update Pet Window class
    def __init__(self, parent, db: DatabaseManager, callback=None):
        # Initialize Update Pet window
        super().__init__(parent)
        
        self.db = db
        self.callback = callback
        self.current_pet = None
        
        # Window configuration
        self.title("Update Pet Information")
        self.geometry("900x750")
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
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="Update Pet Information",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Search section
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Pet:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        search_label.pack(side="left", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=300, placeholder_text="Search by name, species, or owner...")
        self.search_entry.pack(side="left", padx=5, pady=10)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self._search_pets,
            width=100
        )
        search_btn.pack(side="left", padx=5, pady=10)
        
        # Pet list section
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        list_label = ctk.CTkLabel(
            list_frame,
            text="Select Pet to Update:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Scrollable pet list
        self.pet_list_frame = ctk.CTkScrollableFrame(list_frame, height=150)
        self.pet_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load all pets initially
        self._load_pets()
        
        # Update form section (initially hidden)
        self.form_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.form_frame.pack_forget()  # Hide initially
    
    def _load_pets(self, pets=None):
        # Load pets into list
        # Clear existing
        for widget in self.pet_list_frame.winfo_children():
            widget.destroy()
        
        try:
            if pets is None:
                pets = self.db.read_all_pets()
            
            if not pets:
                no_pets = ctk.CTkLabel(
                    self.pet_list_frame,
                    text="No pets found",
                    text_color="gray"
                )
                no_pets.pack(pady=20)
                return
            
            for pet in pets:
                pet_frame = ctk.CTkFrame(self.pet_list_frame)
                pet_frame.pack(fill="x", padx=5, pady=3)
                
                info = f"ID: {pet.pet_id} | {pet.name} ({pet.species}) - Owner: {pet.owner_name}"
                pet_label = ctk.CTkLabel(
                    pet_frame,
                    text=info,
                    anchor="w"
                )
                pet_label.pack(side="left", padx=10, pady=8, fill="x", expand=True)
                
                select_btn = ctk.CTkButton(
                    pet_frame,
                    text="Select",
                    width=80,
                    command=lambda p=pet: self._select_pet(p)
                )
                select_btn.pack(side="right", padx=10, pady=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error loading pets: {str(e)}")
    
    def _search_pets(self):
        # Search for pets
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self._load_pets()
            return
        
        try:
            pets = self.db.search_pets(search_term)
            self._load_pets(pets)
        except Exception as e:
            messagebox.showerror("Error", f"Error searching pets: {str(e)}")
    
    def _select_pet(self, pet: Pet):
        # Select pet for updating
        self.current_pet = pet
        self._show_update_form()
    
    def _show_update_form(self):
        # Show and populate update form
        # Clear form
        for widget in self.form_frame.winfo_children():
            widget.destroy()
        
        # Show form
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        pet = self.current_pet
        
        # Form title
        form_title = ctk.CTkLabel(
            self.form_frame,
            text=f"Update: {pet.name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Pet Information
        row = 1
        ctk.CTkLabel(self.form_frame, text="Pet Name: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.name_entry.insert(0, pet.name)
        self.name_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Species: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.species_var = ctk.StringVar(value=pet.species)
        self.species_menu = ctk.CTkOptionMenu(
            self.form_frame,
            variable=self.species_var,
            values=["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Guinea Pig", "Other"],
            width=300
        )
        self.species_menu.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Breed:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.breed_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.breed_entry.insert(0, pet.breed)
        self.breed_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Date of Birth:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.dob_entry = DateEntry(
            self.form_frame,
            width=40,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        if pet.date_of_birth:
            try:
                dob_date = datetime.strptime(pet.date_of_birth, "%Y-%m-%d")
                self.dob_entry.set_date(dob_date)
            except:
                pass
        self.dob_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Gender:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.gender_var = ctk.StringVar(value=pet.gender or "Unknown")
        self.gender_menu = ctk.CTkOptionMenu(
            self.form_frame,
            variable=self.gender_var,
            values=["Male", "Female", "Unknown"],
            width=300
        )
        self.gender_menu.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Color:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.color_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.color_entry.insert(0, pet.color)
        self.color_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Pet ID:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.microchip_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.microchip_entry.insert(0, pet.microchip_number)
        self.microchip_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        # Owner Information
        row += 1
        owner_section = ctk.CTkLabel(
            self.form_frame,
            text="Owner Information",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        owner_section.grid(row=row, column=0, columnspan=2, sticky="w", pady=(15, 10))
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Owner Name: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.owner_name_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.owner_name_entry.insert(0, pet.owner_name)
        self.owner_name_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Owner Phone: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.owner_phone_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.owner_phone_entry.insert(0, pet.owner_phone)
        self.owner_phone_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Owner Email:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.owner_email_entry = ctk.CTkEntry(self.form_frame, width=300)
        self.owner_email_entry.insert(0, pet.owner_email)
        self.owner_email_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Owner Address:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.owner_address_entry = ctk.CTkTextbox(self.form_frame, width=300, height=60)
        self.owner_address_entry.insert("1.0", pet.owner_address)
        self.owner_address_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Notes:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.notes_entry = ctk.CTkTextbox(self.form_frame, width=300, height=80)
        self.notes_entry.insert("1.0", pet.notes)
        self.notes_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(self.form_frame, text="Active:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        self.active_var = ctk.BooleanVar(value=pet.is_active == 1)
        self.active_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="Pet is active",
            variable=self.active_var
        )
        self.active_checkbox.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        # Buttons
        row += 1
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.grid(row=row, column=0, columnspan=2, pady=(20, 10))
        
        update_btn = ctk.CTkButton(
            button_frame,
            text="Update Pet",
            command=self._update_pet,
            width=130,
            height=35,
            font=ctk.CTkFont(weight="bold")
        )
        update_btn.grid(row=0, column=0, padx=5)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Pet",
            command=self._delete_pet,
            width=130,
            height=35,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.grid(row=0, column=1, padx=5)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=lambda: self.form_frame.pack_forget(),
            width=130,
            height=35,
            fg_color="gray"
        )
        cancel_btn.grid(row=0, column=2, padx=5)
    
    def _update_pet(self):
        # Update pet in database
        if not self.current_pet:
            return
        
        try:
            # Update pet object
            self.current_pet.name = self.name_entry.get().strip()
            self.current_pet.species = self.species_var.get()
            self.current_pet.breed = self.breed_entry.get().strip()
            self.current_pet.date_of_birth = self.dob_entry.get_date().strftime("%Y-%m-%d")
            self.current_pet.gender = self.gender_var.get()
            self.current_pet.color = self.color_entry.get().strip()
            self.current_pet.microchip_number = self.microchip_entry.get().strip()
            self.current_pet.owner_name = self.owner_name_entry.get().strip()
            self.current_pet.owner_phone = self.owner_phone_entry.get().strip()
            self.current_pet.owner_email = self.owner_email_entry.get().strip()
            self.current_pet.owner_address = self.owner_address_entry.get("1.0", "end-1c").strip()
            self.current_pet.notes = self.notes_entry.get("1.0", "end-1c").strip()
            self.current_pet.is_active = 1 if self.active_var.get() else 0
            
            # Validate required fields
            if not self.current_pet.name:
                messagebox.showerror("Error", "Pet name is required")
                return
            
            if not self.current_pet.owner_name:
                messagebox.showerror("Error", "Owner name is required")
                return
            
            if not self.current_pet.owner_phone:
                messagebox.showerror("Error", "Owner phone is required")
                return
            
            # Update in database
            success = self.db.update_pet(self.current_pet)
            
            if success:
                messagebox.showinfo("Success", f"Pet '{self.current_pet.name}' updated successfully!")
                
                # Refresh
                if self.callback:
                    self.callback()
                
                self.form_frame.pack_forget()
                self._load_pets()
            else:
                messagebox.showerror("Error", "Failed to update pet")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error updating pet: {str(e)}")
    
    def _delete_pet(self):
        # Delete pet from database
        if not self.current_pet:
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{self.current_pet.name}'?\n\n"
            "This will also delete all vaccination records for this pet.\n"
            "This action cannot be undone!"
        )
        
        if not confirm:
            return
        
        try:
            success = self.db.delete_pet(self.current_pet.pet_id)
            
            if success:
                messagebox.showinfo("Success", f"Pet '{self.current_pet.name}' deleted successfully!")
                
                # Refresh
                if self.callback:
                    self.callback()
                
                self.form_frame.pack_forget()
                self._load_pets()
                self.current_pet = None
            else:
                messagebox.showerror("Error", "Failed to delete pet")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting pet: {str(e)}")
