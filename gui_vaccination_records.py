"""
Vaccination Records Window for Pet Clinic Vaccination Record System
Manages vaccination records with add, view, update, and delete operations
"""

import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
from models import Pet, Vaccination, VaccineType
from database import DatabaseManager
from datetime import datetime, timedelta
from prettytable import PrettyTable

class VaccinationRecordsWindow(ctk.CTkToplevel):
    """
    Vaccination Records Window class
    Manages all vaccination-related operations
    """
    def __init__(self, parent, db: DatabaseManager, callback=None):
        # Initialize Vaccination Records window
        super().__init__(parent)
        
        self.db = db
        self.callback = callback
        self.selected_pet = None
        
        # Window configuration
        self.title("Vaccination Records Management")
        self.geometry("1100x750")
        
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
            text="Vaccination Records",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Pet selection section
        pet_frame = ctk.CTkFrame(main_frame)
        pet_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        pet_label = ctk.CTkLabel(
            pet_frame,
            text="Select Pet:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        pet_label.pack(side="left", padx=10, pady=10)
        
        # Load pet names
        self.pet_dict = {}
        pets = self.db.read_all_pets()
        pet_names = []
        for pet in pets:
            display_name = f"{pet.name} (ID: {pet.pet_id}) - {pet.species}"
            pet_names.append(display_name)
            self.pet_dict[display_name] = pet
        
        self.pet_var = ctk.StringVar(value="Select a pet...")
        self.pet_menu = ctk.CTkOptionMenu(
            pet_frame,
            variable=self.pet_var,
            values=pet_names if pet_names else ["No pets available"],
            command=self._on_pet_selected,
            width=400
        )
        self.pet_menu.pack(side="left", padx=5, pady=10)
        
        # Add vaccination button
        add_vacc_btn = ctk.CTkButton(
            pet_frame,
            text="➕ Add Vaccination",
            command=self._show_add_vaccination_form,
            width=150
        )
        add_vacc_btn.pack(side="left", padx=10, pady=10)
        
        # Vaccination list section
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        list_label = ctk.CTkLabel(
            list_frame,
            text="Vaccination History:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Scrollable vaccination list
        self.vacc_list_frame = ctk.CTkScrollableFrame(list_frame)
        self.vacc_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Initial message
        self._show_no_selection_message()
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=self.destroy,
            width=150,
            fg_color="gray"
        )
        close_btn.pack(pady=(10, 0))
    
    def _show_no_selection_message(self):
        # Show message when no pet is selected
        for widget in self.vacc_list_frame.winfo_children():
            widget.destroy()
        
        msg = ctk.CTkLabel(
            self.vacc_list_frame,
            text="Please select a pet to view vaccination records",
            text_color="gray",
            font=ctk.CTkFont(size=14)
        )
        msg.pack(pady=50)
    
    def _on_pet_selected(self, selection):
        # Handle pet selection
        if selection in self.pet_dict:
            self.selected_pet = self.pet_dict[selection]
            self._load_vaccinations()
    
    def _load_vaccinations(self):
        # Load vaccinations for selected pet
        if not self.selected_pet:
            return
        
        # Clear existing
        for widget in self.vacc_list_frame.winfo_children():
            widget.destroy()
        
        try:
            vaccinations = self.db.read_vaccinations_by_pet(self.selected_pet.pet_id)
            
            if not vaccinations:
                no_vacc = ctk.CTkLabel(
                    self.vacc_list_frame,
                    text=f"No vaccination records for {self.selected_pet.name}",
                    text_color="gray"
                )
                no_vacc.pack(pady=20)
                return
            
            # Display vaccinations
            for vacc in vaccinations:
                self._create_vaccination_card(vacc)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error loading vaccinations: {str(e)}")
    
    def _create_vaccination_card(self, vacc: Vaccination):
        # Create a card for displaying vaccination information
        card = ctk.CTkFrame(self.vacc_list_frame)
        card.pack(fill="x", padx=5, pady=5)
        
        # Left side - info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Vaccine name
        vaccine = self.db.read_vaccine_type(vacc.vaccine_id)
        vaccine_name = vaccine.vaccine_name if vaccine else "Unknown"
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"💉 {vaccine_name}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        # Date info
        date_info = f"Administered: {vacc.vaccination_date}"
        if vacc.next_due_date:
            date_info += f" | Next Due: {vacc.next_due_date}"
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=date_info,
            font=ctk.CTkFont(size=11)
        )
        date_label.pack(anchor="w")
        
        # Additional info
        if vacc.veterinarian_name or vacc.dose_number:
            extra_info = []
            if vacc.veterinarian_name:
                extra_info.append(f"Vet: {vacc.veterinarian_name}")
            if vacc.dose_number:
                extra_info.append(f"Dose #{vacc.dose_number}")
            
            extra_label = ctk.CTkLabel(
                info_frame,
                text=" | ".join(extra_info),
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            extra_label.pack(anchor="w")
        
        # Right side - buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=10, pady=10)
        
        view_btn = ctk.CTkButton(
            btn_frame,
            text="View Details",
            width=100,
            height=28,
            command=lambda v=vacc: self._view_vaccination_details(v)
        )
        view_btn.pack(side="left", padx=3)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=80,
            height=28,
            fg_color="red",
            hover_color="darkred",
            command=lambda v=vacc: self._delete_vaccination(v)
        )
        delete_btn.pack(side="left", padx=3)
    
    def _view_vaccination_details(self, vacc: Vaccination):
        # Show detailed vaccination information
        vaccine = self.db.read_vaccine_type(vacc.vaccine_id)
        vaccine_name = vaccine.vaccine_name if vaccine else "Unknown"
        manufacturer = vaccine.manufacturer if vaccine else "N/A"
        
        details = f"""
Vaccination Details:

Vaccine: {vaccine_name}
Vaccination Date: {vacc.vaccination_date}
Next Due Date: {vacc.next_due_date or 'N/A'}
Dose Number: {vacc.dose_number}

Veterinarian: {vacc.veterinarian_name or 'N/A'}
Batch Number: {vacc.batch_number or 'N/A'}
Manufacturer: {manufacturer}
Site Administered: {vacc.site_administered or 'N/A'}

Adverse Reactions: {vacc.adverse_reactions or 'None reported'}

Notes: {vacc.notes or 'No additional notes'}
        """
        
        messagebox.showinfo("Vaccination Details", details.strip())
    
    def _delete_vaccination(self, vacc: Vaccination):
        # Delete vaccination record
        vaccine = self.db.read_vaccine_type(vacc.vaccine_id)
        vaccine_name = vaccine.vaccine_name if vaccine else "Unknown"
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the vaccination record for '{vaccine_name}'?"
        )
        
        if not confirm:
            return
        
        try:
            success = self.db.delete_vaccination(vacc.vaccination_id)
            
            if success:
                messagebox.showinfo("Success", "Vaccination record deleted successfully!")
                self._load_vaccinations()
                
                if self.callback:
                    self.callback()
            else:
                messagebox.showerror("Error", "Failed to delete vaccination record")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting vaccination: {str(e)}")
    
    def _show_add_vaccination_form(self):
        # Show form to add new vaccination
        if not self.selected_pet:
            messagebox.showwarning("No Pet Selected", "Please select a pet first")
            return
        
        # Create new window for adding vaccination
        add_window = ctk.CTkToplevel(self)
        add_window.title("Add Vaccination Record")
        add_window.geometry("600x650")
        add_window.transient(self)
        add_window.grab_set()
        
        # Form
        form_frame = ctk.CTkScrollableFrame(add_window)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            form_frame,
            text=f"Add Vaccination for {self.selected_pet.name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        row = 1
        
        # Vaccine name
        ctk.CTkLabel(form_frame, text="Vaccine Name: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        
        vaccine_var = ctk.StringVar()
        vaccine_combo = ctk.CTkComboBox(form_frame, variable=vaccine_var, width=300, state="normal")
        
        # Load vaccine types
        self.vaccine_map = {}
        try:
            vaccines = self.db.read_all_vaccine_types()
            if vaccines:
                vaccine_combo.configure(values=[v.vaccine_name for v in vaccines])
                self.vaccine_map = {v.vaccine_name: v.vaccine_id for v in vaccines}
            else:
                vaccine_combo.configure(values=[""])
        except Exception as e:
            vaccine_combo.configure(values=[""])
        
        vaccine_combo.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Vaccination Date: *").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        vacc_date_entry = DateEntry(
            form_frame,
            width=40,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        vacc_date_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Next Due Date:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        next_due_entry = DateEntry(
            form_frame,
            width=40,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        # Set default to 1 year from vaccination date
        next_due_entry.set_date(datetime.now() + timedelta(days=365))
        next_due_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Veterinarian:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        vet_entry = ctk.CTkEntry(form_frame, width=300)
        vet_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Batch Number:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        batch_entry = ctk.CTkEntry(form_frame, width=300)
        batch_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Dose Number:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        dose_entry = ctk.CTkEntry(form_frame, width=300)
        dose_entry.insert(0, "1")
        dose_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Site Administered:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        site_entry = ctk.CTkEntry(form_frame, width=300)
        site_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Adverse Reactions:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        reactions_entry = ctk.CTkTextbox(form_frame, width=300, height=60)
        reactions_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        ctk.CTkLabel(form_frame, text="Notes:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
        notes_entry = ctk.CTkTextbox(form_frame, width=300, height=80)
        notes_entry.grid(row=row, column=1, pady=5, padx=5, sticky="w")
        
        row += 1
        required_label = ctk.CTkLabel(
            form_frame,
            text="* Required fields",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        required_label.grid(row=row, column=0, columnspan=2, pady=(10, 5))
        
        # Save function
        def save_vaccination():
            vaccine_name = vaccine_var.get().strip()
            if not vaccine_name or vaccine_name in ["Add new vaccine type", "Error loading vaccines"]:
                messagebox.showerror("Error", "Please select or enter a valid vaccine name")
                return
            
            vaccine_id = self.vaccine_map.get(vaccine_name)
            
            # If vaccine doesn't exist in map, create it as a new vaccine type
            if not vaccine_id:
                try:
                    new_vaccine = VaccineType(vaccine_name=vaccine_name, manufacturer="")
                    vaccine_id = self.db.create_vaccine_type(new_vaccine)
                except Exception as e:
                    messagebox.showerror("Error", f"Error creating vaccine type: {str(e)}")
                    return
            
            try:
                dose_num = int(dose_entry.get().strip() or "1")
            except ValueError:
                messagebox.showerror("Error", "Dose number must be a valid integer")
                return
            
            try:
                vacc = Vaccination(
                    pet_id=self.selected_pet.pet_id,
                    vaccine_id=vaccine_id,
                    vaccination_date=vacc_date_entry.get_date().strftime("%Y-%m-%d"),
                    next_due_date=next_due_entry.get_date().strftime("%Y-%m-%d"),
                    veterinarian_name=vet_entry.get().strip(),
                    batch_number=batch_entry.get().strip(),
                    dose_number=dose_num,
                    site_administered=site_entry.get().strip(),
                    adverse_reactions=reactions_entry.get("1.0", "end-1c").strip(),
                    notes=notes_entry.get("1.0", "end-1c").strip()
                )
                
                vacc_id = self.db.create_vaccination(vacc)
                
                messagebox.showinfo("Success", f"Vaccination record added successfully!\nID: {vacc_id}")
                
                add_window.destroy()
                self._load_vaccinations()
                
                if self.callback:
                    self.callback()
            
            except Exception as e:
                messagebox.showerror("Error", f"Error saving vaccination: {str(e)}")
        
        # Buttons
        row += 1
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=(15, 10))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Vaccination",
            command=save_vaccination,
            width=150,
            height=35,
            font=ctk.CTkFont(weight="bold")
        )
        save_btn.grid(row=0, column=0, padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=add_window.destroy,
            width=150,
            height=35,
            fg_color="gray"
        )
        cancel_btn.grid(row=0, column=1, padx=5)
