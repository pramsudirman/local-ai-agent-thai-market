import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSubscriber:
    def __init__(self, storage_file="subscribers.json"):
        self.storage_file = storage_file
        self.load_subscribers()
    
    def load_subscribers(self):
        """Load subscribers from JSON file"""
        try:
            with open(self.storage_file, 'r') as f:
                self.subscribers = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.subscribers = []
    
    def add_subscriber(self, email, name="", preferences=None):
        """Add a new subscriber"""
        if email in [s['email'] for s in self.subscribers]:
            return False
        
        self.subscribers.append({
            "email": email,
            "name": name,
            "subscribed_at": datetime.now().isoformat(),
            "active": True
        })
        self.save_subscribers()
        return True
    
    def save_subscribers(self):
        """Save subscribers to JSON file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.subscribers, f, indent=2)
    
    def send_report(self, report_markdown, subject="Thai Digital Landscape Report"):
        """Send report to all active subscribers via Gmail SMTP"""
        
        gmail_user = os.getenv("GMAIL_USER")
        gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not gmail_user or not gmail_password:
            print("❌ ERROR: Gmail credentials not found in .env file")
            print("   Create app password: myaccount.google.com/apppasswords")
            return
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(gmail_user, gmail_password)
            
            sent_count = 0
            for subscriber in self.subscribers:
                if not subscriber.get('active', True):
                    continue
                
                try:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = f"{subject} - {datetime.now().strftime('%Y-%m-%d')}"
                    msg['From'] = gmail_user
                    msg['To'] = subscriber['email']
                    
                    # Plain text version
                    text_part = MIMEText(report_markdown, 'plain', 'utf-8')
                    msg.attach(text_part)
                    
                    # Send
                    server.send_message(msg)
                    sent_count += 1
                    print(f"✓ Sent to {subscriber['email']}")
                    
                except Exception as e:
                    print(f"✗ Failed to send to {subscriber['email']}: {e}")
            
            server.quit()
            print(f"\n📧 Report sent to {sent_count} subscribers")
            
        except Exception as e:
            print(f"❌ SMTP Error: {e}")
            print("Check your Gmail app password and network connection")