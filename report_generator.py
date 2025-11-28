# Report Generator for Pet Clinic Vaccination Record System


from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List
from models import Pet, Vaccination
import os


class ReportGenerator:
    # Report Generator class for creating PDF reports
    def __init__(self, output_folder: str = "reports"):
        """Initialize report generator"""
        self.output_folder = output_folder
        self._ensure_output_folder()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _ensure_output_folder(self):
        # Create output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def _setup_custom_styles(self):
        # Setup custom paragraph styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50')
        )
    
    def generate_pet_report(self, pet: Pet, vaccinations: List[Vaccination]) -> str:
        # Generate comprehensive pet report with vaccination history
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pet_report_{pet.name.replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph(f"Pet Medical Record", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Pet Information Section
        pet_heading = Paragraph("Pet Information", self.heading_style)
        story.append(pet_heading)
        
        pet_data = [
            ['Pet ID:', str(pet.pet_id), 'Name:', pet.name],
            ['Species:', pet.species, 'Breed:', pet.breed or 'N/A'],
            ['Date of Birth:', pet.date_of_birth or 'N/A', 'Gender:', pet.gender or 'N/A'],
            ['Color:', pet.color or 'N/A', 'Pet ID:', pet.microchip_number or 'N/A'],
        ]
        
        pet_table = Table(pet_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
        pet_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(pet_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Owner Information Section
        owner_heading = Paragraph("Owner Information", self.heading_style)
        story.append(owner_heading)
        
        owner_data = [
            ['Owner Name:', pet.owner_name],
            ['Phone:', pet.owner_phone],
            ['Email:', pet.owner_email or 'N/A'],
            ['Address:', pet.owner_address or 'N/A'],
        ]
        
        owner_table = Table(owner_data, colWidths=[1.5*inch, 5*inch])
        owner_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(owner_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Vaccination History Section
        vacc_heading = Paragraph("Vaccination History", self.heading_style)
        story.append(vacc_heading)
        
        if vaccinations:
            vacc_data = [['Date', 'Vaccine', 'Next Due', 'Veterinarian', 'Dose']]
            for vacc in vaccinations:
                vacc_data.append([
                    vacc.vaccination_date,
                    vacc.vaccine_name,
                    vacc.next_due_date or 'N/A',
                    vacc.veterinarian_name or 'N/A',
                    str(vacc.dose_number)
                ])
            
            vacc_table = Table(vacc_data, colWidths=[1*inch, 2*inch, 1*inch, 1.5*inch, 0.7*inch])
            vacc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
            ]))
            story.append(vacc_table)
        else:
            no_vacc = Paragraph("No vaccination records found.", self.normal_style)
            story.append(no_vacc)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Notes Section
        if pet.notes:
            notes_heading = Paragraph("Additional Notes", self.heading_style)
            story.append(notes_heading)
            notes = Paragraph(pet.notes, self.normal_style)
            story.append(notes)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle('Footer', parent=self.normal_style, fontSize=8, textColor=colors.grey)
        )
        story.append(footer)
        
        doc.build(story)
        return filepath
    
    def generate_all_pets_report(self, pets: List[Pet]) -> str:
        # Generate report of all pets
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_pets_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("All Pets Report", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        summary = Paragraph(f"Total Pets: {len(pets)}", self.heading_style)
        story.append(summary)
        story.append(Spacer(1, 0.2*inch))
        
        # Pets Table
        if pets:
            pet_data = [['ID', 'Name', 'Species', 'Breed', 'Owner', 'Phone']]
            for pet in pets:
                pet_data.append([
                    str(pet.pet_id),
                    pet.name,
                    pet.species,
                    pet.breed or 'N/A',
                    pet.owner_name,
                    pet.owner_phone
                ])
            
            pet_table = Table(pet_data, colWidths=[0.5*inch, 1.3*inch, 1*inch, 1.2*inch, 1.5*inch, 1.2*inch])
            pet_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
            ]))
            story.append(pet_table)
        else:
            no_pets = Paragraph("No pets found.", self.normal_style)
            story.append(no_pets)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle('Footer', parent=self.normal_style, fontSize=8, textColor=colors.grey)
        )
        story.append(footer)
        
        doc.build(story)
        return filepath
    
    def generate_vaccination_schedule_report(self, upcoming_vaccinations: List[tuple]) -> str:
        # Generate report of upcoming vaccinations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vaccination_schedule_{timestamp}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title = Paragraph("Upcoming Vaccination Schedule", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        summary = Paragraph(f"Total Upcoming Vaccinations: {len(upcoming_vaccinations)}", self.heading_style)
        story.append(summary)
        story.append(Spacer(1, 0.2*inch))
        
        # Vaccinations Table
        if upcoming_vaccinations:
            vacc_data = [['Pet Name', 'Vaccine', 'Due Date', 'Owner', 'Phone']]
            for vacc in upcoming_vaccinations:
                vacc_data.append([
                    vacc[0],  # pet_name
                    vacc[1],  # vaccine_name
                    vacc[2],  # next_due_date
                    vacc[3],  # owner_name
                    vacc[4]   # owner_phone
                ])
            
            vacc_table = Table(vacc_data, colWidths=[1.5*inch, 1.8*inch, 1*inch, 1.5*inch, 1.2*inch])
            vacc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FEF9E7')]),
            ]))
            story.append(vacc_table)
        else:
            no_vacc = Paragraph("No upcoming vaccinations.", self.normal_style)
            story.append(no_vacc)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ParagraphStyle('Footer', parent=self.normal_style, fontSize=8, textColor=colors.grey)
        )
        story.append(footer)
        
        doc.build(story)
        return filepath
