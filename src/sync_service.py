import os
import json
from pyairtable import Api
from datetime import datetime
from dotenv import load_dotenv

# Load env variables (API keys)
load_dotenv()

class SubscriberSync:
    def __init__(self, json_file="subscribers.json"):
        # We look for these keys in your .env file
        self.api_key = os.getenv("AIRTABLE_API_KEY")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.table_id = os.getenv("AIRTABLE_TABLE_ID")
        self.json_file = json_file
        
    def sync(self):
        """Pulls from Airtable and updates local JSON without duplicates"""
        print(f"☁️  Connecting to Airtable Base: {self.base_id}...")
        
        try:
            # 1. Fetch Cloud Data
            api = Api(self.api_key)
            table = api.table(self.base_id, self.table_id)
            cloud_records = table.all()
        except Exception as e:
            print(f"❌ Error connecting to Airtable: {e}")
            return

        # 2. Load Local Data
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                local_data = json.load(f)
        else:
            local_data = []
            
        # Create a set of existing emails for fast lookup (lowercase to avoid Duplicates)
        existing_emails = {entry['email'].lower() for entry in local_data}
        new_count = 0
        
        # 3. Merge Cloud Data into Local
        for record in cloud_records:
            fields = record['fields']
            # Note: 'Email' and 'Name' must match your Airtable Column Headers exactly!
            email = fields.get('Email') 
            name = fields.get('Name', 'Subscriber')
            
            if email and email.lower() not in existing_emails:
                new_subscriber = {
                    "email": email,
                    "name": name,
                    "subscribed_at": datetime.now().isoformat(),
                    "active": True,
                    "source": "airtable"
                }
                local_data.append(new_subscriber)
                existing_emails.add(email.lower())
                new_count += 1
                print(f"   + Found new subscriber: {email}")

        # 4. Save updates
        if new_count > 0:
            with open(self.json_file, 'w') as f:
                json.dump(local_data, f, indent=2)
            print(f"✅ Synced! Added {new_count} new subscribers.")
        else:
            print("✓ Local list is already up to date.")

if __name__ == "__main__":
    # This allows you to run 'python src/sync_service.py' directly
    syncer = SubscriberSync()
    syncer.sync()