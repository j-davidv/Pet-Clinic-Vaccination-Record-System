""" Reports Window for Pet Clinic Vaccination Record System
    Generates various PDF reports using ReportLab """

import customtkinter as ctk
from tkinter import messagebox
from database import DatabaseManager
from report_generator import ReportGenerator
import os

# Reports Window class
class ReportsWindow(ctk.CTkToplevel):
    def __init__(self, parent, db: DatabaseManager, report_gen: ReportGenerator):
        super().__init__(parent)
        
        self.db = db
        self.report_gen = report_gen
        
        # Window configuration
        self.title("Generate Reports")
        self.geometry("700x600")
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
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="📄 Generate Reports",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Report types
        self._create_report_card(
            main_frame,
            "Individual Pet Report",
            "Generate a comprehensive report for a specific pet including all vaccination history",
            "🐕",
            self._generate_pet_report
        )
        
        self._create_report_card(
            main_frame,
            "All Pets Report",
            "Generate a summary report of all registered pets in the system",
            "📋",
            self._generate_all_pets_report
        )
        
        self._create_report_card(
            main_frame,
            "Vaccination Schedule",
            "Generate a report of upcoming vaccinations due in the next 30 days",
            "📅",
            self._generate_vaccination_schedule
        )
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            command=self.destroy,
            width=200,
            height=40,
            fg_color="gray",
            font=ctk.CTkFont(size=14)
        )
        close_btn.pack(pady=(20, 0))
    
    def _create_report_card(self, parent, title: str, description: str, icon: str, command):
        # Create a report option card
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", pady=10)
        
        # Content frame
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Icon and title
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 5))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left")
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=500,
            justify="left"
        )
        desc_label.pack(fill="x", pady=(0, 10))
        
        # Generate button
        generate_btn = ctk.CTkButton(
            content_frame,
            text="Generate Report",
            command=command,
            width=180,
            height=35
        )
        generate_btn.pack(anchor="e")
    
    def _generate_pet_report(self):
        # Generate individual pet report
        # Get all pets
        pets = self.db.read_all_pets()
        
        if not pets:
            messagebox.showwarning("No Pets", "No pets found in the system")
            return
        
        # Create selection window
        select_window = ctk.CTkToplevel(self)
        select_window.title("Select Pet")
        select_window.geometry("500x400")
        select_window.transient(self)
        select_window.grab_set()
        
        # Title
        title = ctk.CTkLabel(
            select_window,
            text="Select Pet for Report",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=20)
        
        # Pet list
        list_frame = ctk.CTkScrollableFrame(select_window, height=250)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for pet in pets:
            pet_frame = ctk.CTkFrame(list_frame)
            pet_frame.pack(fill="x", padx=5, pady=3)
            
            info = f"{pet.name} (ID: {pet.pet_id}) - {pet.species}"
            if pet.breed:
                info += f" - {pet.breed}"
            
            pet_label = ctk.CTkLabel(
                pet_frame,
                text=info,
                anchor="w"
            )
            pet_label.pack(side="left", padx=10, pady=8, fill="x", expand=True)
            
            select_btn = ctk.CTkButton(
                pet_frame,
                text="Generate",
                width=100,
                command=lambda p=pet: self._do_generate_pet_report(p, select_window)
            )
            select_btn.pack(side="right", padx=10, pady=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            select_window,
            text="Cancel",
            command=select_window.destroy,
            fg_color="gray"
        )
        cancel_btn.pack(pady=(0, 20))
    
    def _do_generate_pet_report(self, pet, window):
        # Generate report for selected pet
        try:
            vaccinations = self.db.read_vaccinations_by_pet(pet.pet_id)
            filepath = self.report_gen.generate_pet_report(pet, vaccinations, self.db)
            
            window.destroy()
            
            messagebox.showinfo(
                "Report Generated",
                f"Pet report for '{pet.name}' generated successfully!\n\n"
                f"Saved to: {filepath}"
            )
            
            # Open the PDF
            try:
                os.startfile(filepath)
            except:
                pass  # If opening fails, just show the message
        
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def _generate_all_pets_report(self):
        # Generate report of all pets
        try:
            pets = self.db.read_all_pets()
            
            if not pets:
                messagebox.showwarning("No Pets", "No pets found in the system")
                return
            
            filepath = self.report_gen.generate_all_pets_report(pets, self.db)
            
            messagebox.showinfo(
                "Report Generated",
                f"All pets report generated successfully!\n\n"
                f"Total pets: {len(pets)}\n"
                f"Saved to: {filepath}"
            )
            
            # Open the PDF
            try:
                os.startfile(filepath)
            except:
                pass
        
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def _generate_vaccination_schedule(self):
        # Generate vaccination schedule report
        try:
            upcoming = self.db.get_upcoming_vaccinations(30)
            
            if not upcoming:
                messagebox.showinfo(
                    "No Upcoming Vaccinations",
                    "No vaccinations due in the next 30 days"
                )
                return
            
            filepath = self.report_gen.generate_vaccination_schedule_report(upcoming)
            
            messagebox.showinfo(
                "Report Generated",
                f"Vaccination schedule report generated successfully!\n\n"
                f"Upcoming vaccinations: {len(upcoming)}\n"
                f"Saved to: {filepath}"
            )
            
            # Open the PDF
            try:
                os.startfile(filepath)
            except:
                pass
        
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
