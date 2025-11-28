# Main Application and Dashboard for Pet Clinic Vaccination Record System


import customtkinter as ctk
from database import DatabaseManager
from report_generator import ReportGenerator
from typing import Optional
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os


# Import GUI windows
from gui_add_pet import AddPetWindow
from gui_update_pet import UpdatePetWindow
from gui_vaccination_records import VaccinationRecordsWindow
from gui_reports import ReportsWindow


class PetClinicApp(ctk.CTk):
    # Main Application class for Pet Clinic System
    def __init__(self):
        # nitialize main application
        super().__init__()
        
        # Database and Report Generator
        self.db = DatabaseManager()
        self.report_gen = ReportGenerator()
        
        # Window configuration
        self.title("Pet Clinic Vaccination Record System")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # Initialize color palette
        self._update_colors()
        
        # Initialize UI
        self._setup_ui()
        self._load_dashboard_data()
    
    def _update_colors(self):
        # Update color palette based on current appearance mode
        mode = ctk.get_appearance_mode()
        
        if mode == "Dark":
            self.colors = {
                'primary': '#10B981',      # Emerald green
                'secondary': '#3B82F6',    # Blue
                'success': '#22C55E',      # Green
                'warning': '#F59E0B',      # Amber
                'danger': '#EF4444',       # Red
                'info': '#06B6D4',         # Cyan
                'dark': '#1F2937',         # Dark gray
                'light': '#111827',        # dark background
                'card_bg': '#1F2937',      # Dark gray
                'text_primary': '#F9FAFB', # white
                'text_secondary': '#D1D5DB', # Light gray
                'border': '#374151'        # Dark border
            }
        else:  # Light mode
            self.colors = {
                'primary': '#10B981',      # Emerald green
                'secondary': '#3B82F6',    # Blue
                'success': '#22C55E',      # Green
                'warning': '#F59E0B',      # Amber
                'danger': '#EF4444',       # Red
                'info': '#06B6D4',         # Cyan
                'dark': '#1F2937',         # Dark gray
                'light': '#F3F4F6',        # Light gray
                'card_bg': '#FFFFFF',      # White
                'text_primary': '#111827', # black
                'text_secondary': '#6B7280', # Gray
                'border': '#E5E7EB'        # Light border
            }
    
    def _setup_ui(self):
        # Setup main user interface
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self._create_sidebar()
        
        # Main content area
        self._create_main_content()
    
    def _create_sidebar(self):
        # Create navigation sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.colors['dark'])
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🐾 Pet Clinic",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard",
            command=self._show_dashboard,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=self.colors['primary'],
            hover_color=self.colors['success'],
            corner_radius=8
        )
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.add_pet_btn = ctk.CTkButton(
            self.sidebar,
            text="➕ Add Pet",
            command=self._open_add_pet,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=self.colors['primary'],
            border_width=2,
            border_color=self.colors['primary'],
            corner_radius=8
        )
        self.add_pet_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.update_pet_btn = ctk.CTkButton(
            self.sidebar,
            text="✏️ Update Pet",
            command=self._open_update_pet,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=self.colors['primary'],
            border_width=2,
            border_color=self.colors['primary'],
            corner_radius=8
        )
        self.update_pet_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.vaccination_btn = ctk.CTkButton(
            self.sidebar,
            text="💉 Vaccinations",
            command=self._open_vaccinations,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=self.colors['primary'],
            border_width=2,
            border_color=self.colors['primary'],
            corner_radius=8
        )
        self.vaccination_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.reports_btn = ctk.CTkButton(
            self.sidebar,
            text="📄 Reports",
            command=self._open_reports,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=self.colors['primary'],
            border_width=2,
            border_color=self.colors['primary'],
            corner_radius=8
        )
        self.reports_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Appearance mode
        self.appearance_label = ctk.CTkLabel(
            self.sidebar,
            text="Appearance:",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        )
        self.appearance_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            command=self._change_appearance_mode,
            fg_color=self.colors['primary'],
            button_color=self.colors['success'],
            button_hover_color=self.colors['primary']
        )
        self.appearance_mode.grid(row=12, column=0, padx=20, pady=10)
        self.appearance_mode.set("Light")
    
    def _create_main_content(self):
        # Create main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.colors['light'])
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Dashboard content
        self._create_dashboard()
    
    def _create_dashboard(self):
        # Create dashboard view
        # Update main frame background color
        self.main_frame.configure(fg_color=self.colors['light'])
        
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors['text_primary']
        )
        header.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="w")
        
        # Stats container
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Pets Card
        self.pets_card = self._create_stat_card(
            stats_frame,
            "Total Pets",
            "0",
            "🐕",
            self.colors['secondary']
        )
        self.pets_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Total Vaccinations Card
        self.vacc_card = self._create_stat_card(
            stats_frame,
            "Total Vaccinations",
            "0",
            "💉",
            self.colors['success']
        )
        self.vacc_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Upcoming Vaccinations Card
        self.upcoming_card = self._create_stat_card(
            stats_frame,
            "Upcoming (30 days)",
            "0",
            "⏰",
            self.colors['warning']
        )
        self.upcoming_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Recent Activity
        activity_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['card_bg'], corner_radius=12, border_width=1, border_color=self.colors['border'])
        activity_frame.grid(row=2, column=0, padx=30, pady=(0, 20), sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        activity_label = ctk.CTkLabel(
            activity_frame,
            text="Recent Pets",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        activity_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Scrollable frame for recent pets
        self.recent_pets_frame = ctk.CTkScrollableFrame(activity_frame, height=300, fg_color="transparent")
        self.recent_pets_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        activity_frame.grid_columnconfigure(0, weight=1)
        activity_frame.grid_rowconfigure(1, weight=1)
        
        # Quick Actions
        quick_actions_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors['card_bg'], corner_radius=12, border_width=1, border_color=self.colors['border'])
        quick_actions_frame.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="ew")
        
        quick_label = ctk.CTkLabel(
            quick_actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        quick_label.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")
        
        # Quick action buttons
        btn_frame = ctk.CTkFrame(quick_actions_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        ctk.CTkButton(
            btn_frame,
            text="➕ Add New Pet",
            command=self._open_add_pet,
            height=35,
            fg_color=self.colors['primary'],
            hover_color=self.colors['success'],
            corner_radius=8
        ).grid(row=0, column=0, padx=5, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💉 Add Vaccination",
            command=self._open_vaccinations,
            height=35,
            fg_color=self.colors['info'],
            hover_color=self.colors['secondary'],
            corner_radius=8
        ).grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📄 Generate Report",
            command=self._open_reports,
            height=35,
            fg_color=self.colors['warning'],
            hover_color="#D97706",
            corner_radius=8
        ).grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self._load_dashboard_data,
            height=35,
            fg_color="transparent",
            hover_color=self.colors['light'],
            border_width=2,
            border_color=self.colors['text_secondary'],
            text_color=self.colors['text_secondary'],
            corner_radius=8
        ).grid(row=0, column=3, padx=5, pady=5)
    
    def _create_stat_card(self, parent, title: str, value: str, icon: str, color: str):
        # Create a statistics card
        card = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=12, border_width=1, border_color=self.colors['border'])
        card.grid_columnconfigure(0, weight=1)
        
        # Icon and value
        value_label = ctk.CTkLabel(
            card,
            text=f"{icon} {value}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=color
        )
        value_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary']
        )
        title_label.grid(row=1, column=0, padx=20, pady=(5, 20))
        
        # Store labels for updating
        card.value_label = value_label
        card.icon = icon
        card.color = color
        
        return card
    
    def _load_dashboard_data(self):
        # Load and display dashboard data
        try:
            # Get statistics
            pet_count = self.db.get_pet_count()
            vacc_count = self.db.get_vaccination_count()
            upcoming = self.db.get_upcoming_vaccinations(30)
            
            # Update stat cards
            self.pets_card.value_label.configure(text=f"{self.pets_card.icon} {pet_count}")
            self.vacc_card.value_label.configure(text=f"{self.vacc_card.icon} {vacc_count}")
            self.upcoming_card.value_label.configure(text=f"{self.upcoming_card.icon} {len(upcoming)}")
            
            # Load recent pets
            self._load_recent_pets()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading dashboard data: {str(e)}")
    
    def _load_recent_pets(self):
        # Load recent pets into dashboard
        for widget in self.recent_pets_frame.winfo_children():
            widget.destroy()
        
        try:
            pets = self.db.read_all_pets()[:10]  # Get first 10 pets
            
            if not pets:
                no_pets_label = ctk.CTkLabel(
                    self.recent_pets_frame,
                    text="No pets registered yet. Click 'Add Pet' to get started!",
                    font=ctk.CTkFont(size=14),
                    text_color=self.colors['text_secondary']
                )
                no_pets_label.pack(pady=20)
                return
            
            for pet in pets:
                pet_frame = ctk.CTkFrame(self.recent_pets_frame, fg_color=self.colors['light'], corner_radius=8)
                pet_frame.pack(fill="x", padx=5, pady=5)
                
                info_text = f"{pet.name} ({pet.species}) - Owner: {pet.owner_name}"
                pet_label = ctk.CTkLabel(
                    pet_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=12),
                    anchor="w",
                    text_color=self.colors['text_primary']
                )
                pet_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
                
                view_btn = ctk.CTkButton(
                    pet_frame,
                    text="View",
                    width=80,
                    height=28,
                    command=lambda p=pet: self._view_pet_details(p),
                    fg_color=self.colors['secondary'],
                    hover_color=self.colors['primary'],
                    corner_radius=6
                )
                view_btn.pack(side="right", padx=10, pady=5)
        
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.recent_pets_frame,
                text=f"Error loading pets: {str(e)}",
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def _view_pet_details(self, pet):
        # View pet details and generate report
        try:
            vaccinations = self.db.read_vaccinations_by_pet(pet.pet_id)
            filepath = self.report_gen.generate_pet_report(pet, vaccinations)
            
            messagebox.showinfo(
                "Report Generated",
                f"Pet report generated successfully!\n\nSaved to: {filepath}"
            )
            
            # Open the PDF
            os.startfile(filepath)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")
    
    def _show_dashboard(self):
        # Show dashboard view
        self._create_dashboard()
        self._load_dashboard_data()
    
    def _open_add_pet(self):
        # Open Add Pet window
        AddPetWindow(self, self.db, self._load_dashboard_data)
    
    def _open_update_pet(self):
        # Open Update Pet window
        UpdatePetWindow(self, self.db, self._load_dashboard_data)
    
    def _open_vaccinations(self):
        # Open Vaccination Records window
        VaccinationRecordsWindow(self, self.db, self._load_dashboard_data)
    
    def _open_reports(self):
        # Open Reports window
        ReportsWindow(self, self.db, self.report_gen)
    
    def _change_appearance_mode(self, new_mode: str):
        # Change application appearance mode
        ctk.set_appearance_mode(new_mode.lower())
        self._update_colors()
        self._show_dashboard()
    
    def run(self):
        # Run the application
        self.mainloop()
    
    def on_closing(self):
        # Handle application closing
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = PetClinicApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.run()
