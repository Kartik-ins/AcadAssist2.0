from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QCalendarWidget, QPushButton, 
                            QLineEdit, QMessageBox, QHBoxLayout, QSpinBox, QFrame)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDateTime, QTime
import requests
from datetime import datetime, timedelta
import pytz

class SchedulePage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
       
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 0, 0)
        main_layout.setSpacing(10)
        
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0D47A1;")
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        app_label = QLabel("AcadAssist")
        app_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        app_label.setStyleSheet("color: white;")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Your Academic Assistant")
        subtitle.setFont(QFont("Arial", 16))
        subtitle.setStyleSheet("color: #90CAF9;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_label = QLabel("Schedule Management")
        feature_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        feature_label.setStyleSheet("color: white; margin-top: 30px;")
        feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        feature_desc = QLabel("Organize your deadlines and\nreceive timely reminders")
        feature_desc.setFont(QFont("Arial", 12))
        feature_desc.setStyleSheet("color: #90CAF9;")
        feature_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        left_layout.addStretch()
        left_layout.addWidget(app_label)
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(40)
        left_layout.addWidget(feature_label)
        left_layout.addWidget(feature_desc)
        left_layout.addStretch()
        
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        
        schedule_container = QFrame()
        schedule_container.setMaximumWidth(600)
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Schedule Management")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumHeight(300)
        
        deadline_label = QLabel("Deadline Description:")
        deadline_label.setFont(QFont("Arial", 12))
        self.deadline_input = QLineEdit()
        self.deadline_input.setPlaceholderText("Enter deadline description")
        self.deadline_input.setMinimumHeight(40)
        
        deadline_time_layout = QHBoxLayout()
        deadline_time_label = QLabel("Deadline Time (IST):")
        deadline_time_label.setFont(QFont("Arial", 12))
        self.deadline_hour = QSpinBox()
        self.deadline_hour.setRange(0, 23)
        self.deadline_hour.setValue(12)
        self.deadline_hour.setMinimumHeight(35)
        self.deadline_hour.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 20px; height: 20px; }")
        self.deadline_minute = QSpinBox()
        self.deadline_minute.setRange(0, 59)
        self.deadline_minute.setValue(0)
        self.deadline_minute.setMinimumHeight(35)
        self.deadline_minute.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 20px; height: 20px; }")
        deadline_time_layout.addWidget(deadline_time_label)
        deadline_time_layout.addWidget(self.deadline_hour)
        deadline_time_layout.addWidget(QLabel(":"))
        deadline_time_layout.addWidget(self.deadline_minute)
        
        reminder_time_layout = QHBoxLayout()
        reminder_time_label = QLabel("Reminder Time (IST):")
        reminder_time_label.setFont(QFont("Arial", 12))
        self.reminder_hour = QSpinBox()
        self.reminder_hour.setRange(0, 23)
        self.reminder_hour.setValue(9)
        self.reminder_hour.setMinimumHeight(35)
        self.reminder_hour.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 20px; height: 20px; }")
        self.reminder_minute = QSpinBox()
        self.reminder_minute.setRange(0, 59)
        self.reminder_minute.setValue(0)
        self.reminder_minute.setMinimumHeight(35)
        self.reminder_minute.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 20px; height: 20px; }")
        reminder_days_label = QLabel("Days before:")
        reminder_days_label.setFont(QFont("Arial", 12))
        self.reminder_days = QSpinBox()
        self.reminder_days.setRange(0, 30)
        self.reminder_days.setValue(1)
        self.reminder_days.setMinimumHeight(35)
        self.reminder_days.setStyleSheet("QSpinBox::up-button, QSpinBox::down-button { width: 20px; height: 20px; }")
        reminder_time_layout.addWidget(reminder_time_label)
        reminder_time_layout.addWidget(self.reminder_hour)
        reminder_time_layout.addWidget(QLabel(":"))
        reminder_time_layout.addWidget(self.reminder_minute)
        reminder_time_layout.addWidget(reminder_days_label)
        reminder_time_layout.addWidget(self.reminder_days)
        
        self.save_button = QPushButton("Save Deadline")
        self.save_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.save_button.setMinimumHeight(50)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_deadline)
        
        schedule_layout.addWidget(title)
        schedule_layout.addSpacing(20)
        schedule_layout.addWidget(self.calendar)
        schedule_layout.addSpacing(20)
        schedule_layout.addWidget(deadline_label)
        schedule_layout.addWidget(self.deadline_input)
        schedule_layout.addSpacing(10)
        schedule_layout.addLayout(deadline_time_layout)
        schedule_layout.addSpacing(10)
        schedule_layout.addLayout(reminder_time_layout)
        schedule_layout.addSpacing(20)
        schedule_layout.addWidget(self.save_button)
        
        right_layout.addStretch()
        right_layout.addWidget(schedule_container)
        right_layout.addStretch()
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  
    
    def convert_to_utc(self, local_datetime):
        """Convert local IST datetime to UTC"""
        ist = pytz.timezone('Asia/Kolkata')
        utc = pytz.UTC
        
        local_dt = ist.localize(local_datetime)
        utc_dt = local_dt.astimezone(utc)
        return utc_dt
    
    def save_deadline(self):
        selected_date = self.calendar.selectedDate()
        deadline_text = self.deadline_input.text()
        
        if not deadline_text:
            QMessageBox.warning(self, "Error", "Please enter a deadline description")
            return
            
        # Create deadline time in IST
        deadline_time_ist = datetime(
            selected_date.year(),
            selected_date.month(),
            selected_date.day(),
            self.deadline_hour.value(),
            self.deadline_minute.value()
        )
        
        # Convert to UTC
        deadline_time_utc = self.convert_to_utc(deadline_time_ist)
        deadline_str = deadline_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
        print(f"Deadline (IST): {deadline_time_ist}")
        print(f"Deadline (UTC): {deadline_time_utc}")
        
        # Calculate reminder time in IST
        reminder_days = self.reminder_days.value()
        reminder_time_ist = datetime(
            selected_date.year(),
            selected_date.month(),
            selected_date.day(),
            self.reminder_hour.value(),
            self.reminder_minute.value()
        ) - timedelta(days=reminder_days)
        
        # Convert to UTC
        reminder_time_utc = self.convert_to_utc(reminder_time_ist)
        reminder_str = reminder_time_utc.strftime("%Y-%m-%dT%H:%M:%S")
        print(f"Reminder (IST): {reminder_time_ist}")
        print(f"Reminder (UTC): {reminder_time_utc}")
        
        # Send email reminder using Mailjet API
        self.send_reminder_email(deadline_text, deadline_str, reminder_str)
        
        QMessageBox.information(self, "Success", f"Deadline saved for {deadline_time_ist.strftime('%Y-%m-%d %H:%M:%S')} IST")
        
    def send_reminder_email(self, task_name, deadline, reminder_time):
        print("\n=== Starting Email Reminder Process ===")
        
        # Mailjet API credentials
        API_KEY = 'db722316dc59f2215f167af4871d61c5'
        API_SECRET = '68b0add277af5ded50d107895d3c59b3'
        MJ_APIKEY_PUBLIC = API_KEY
        MJ_APIKEY_PRIVATE = API_SECRET
        
        # Get user details from parent
        user_email = self.parent.user_email.strip()
        print(f"User Email: {user_email}")
        user_name = "User"  
        print(f"Task Name: {task_name}")
        print(f"Deadline (UTC): {deadline}")
        print(f"Reminder Time (UTC): {reminder_time}")
        
        print("\nStep 1: Getting/Creating Contacts List")
        list_name = "Deadline Reminders"
        response = requests.get(
            "https://api.mailjet.com/v3/REST/contactslist",
            auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE)
        )
        print(f"Get Lists Response: {response.status_code}")
        print(f"Get Lists Response Text: {response.text}")
        
        contacts_list_id = None
        for lst in response.json().get("Data", []):
            if lst["Name"] == list_name:
                contacts_list_id = lst["ID"]
                print(f"Found existing list with ID: {contacts_list_id}")
                break
                
        if not contacts_list_id:
            print("Creating new contacts list")
            response = requests.post(
                "https://api.mailjet.com/v3/REST/contactslist",
                auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE),
                json={"Name": list_name}
            )
            print(f"Create List Response: {response.status_code}")
            print(f"Create List Response Text: {response.text}")
            contacts_list_id = response.json()["Data"][0]["ID"]
            print(f"Created new list with ID: {contacts_list_id}")
        
        print("\nStep 2: Adding User to Contacts List")
        contact_data = {
            "Email": user_email,
            "Name": user_name,
            "Properties": {
                "task": task_name,
                "deadline": deadline
            }
        }
        print(f"Contact Data: {contact_data}")
        
        response = requests.post(
            f"https://api.mailjet.com/v3/REST/contactslist/{contacts_list_id}/managecontact",
            auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE),
            json={"Email": user_email, "Name": user_name, "Action": "addnoforce"}
        )
        print(f"Add Contact Response: {response.status_code}")
        print(f"Add Contact Response Text: {response.text}")
        
        print("\nStep 3: Creating Campaign Draft")
        draft_data = {
            "Locale": "en_US",
            "Sender": "Task Reminder",
            "SenderEmail": "acadassistant8@gmail.com",
            "Subject": f"⏰ Reminder: {task_name} deadline approaching",
            "ContactsListID": contacts_list_id,
            "Title": f"Deadline: {task_name}"
        }
        print(f"Draft Data: {draft_data}")
        
        response = requests.post(
            "https://api.mailjet.com/v3/REST/campaigndraft",
            auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE),
            json=draft_data
        )
        print(f"Create Draft Response: {response.status_code}")
        print(f"Create Draft Response Text: {response.text}")
        
        try:
            draft_id = response.json()["Data"][0]["ID"]
            print(f"Created draft with ID: {draft_id}")
        except Exception as e:
            print(f"Error getting draft ID: {e}")
            QMessageBox.warning(self, "Error", f"Failed to create campaign draft: {response.text}")
            return
        
        print("\nStep 4: Adding Email Content")
        content_data = {
            "Html-part": f"""
                <h3>Hi {user_name},</h3>
                <p>Your task <strong>{task_name}</strong> is due soon!</p>
                <p>Deadline: {deadline}</p>
            """,
            "Text-part": f"Hi {user_name},\n\nYour task '{task_name}' is due soon!\nDeadline: {deadline}"
        }
        print(f"Content Data: {content_data}")
        
        response = requests.post(
            f"https://api.mailjet.com/v3/REST/campaigndraft/{draft_id}/detailcontent",
            auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE),
            json=content_data
        )
        print(f"Add Content Response: {response.status_code}")
        print(f"Add Content Response Text: {response.text}")
        
        print("\nStep 5: Scheduling Email")
        schedule_data = {"Date": reminder_time}
        print(f"Schedule Data: {schedule_data}")
        
        response = requests.post(
            f"https://api.mailjet.com/v3/REST/campaigndraft/{draft_id}/schedule",
            auth=(MJ_APIKEY_PUBLIC, MJ_APIKEY_PRIVATE),
            json=schedule_data
        )
        print(f"Schedule Response: {response.status_code}")
        print(f"Schedule Response Text: {response.text}")
        
        if response.status_code == 201:
            print(f"✅ Reminder scheduled for {reminder_time} UTC!")
            QMessageBox.information(self, "Success", f"Reminder scheduled for {reminder_time} UTC!")
        else:
            print(f"Failed to schedule: {response.text}")
            QMessageBox.warning(self, "Error", f"Failed to schedule reminder: {response.text}")
        
        print("=== Email Reminder Process Complete ===\n")