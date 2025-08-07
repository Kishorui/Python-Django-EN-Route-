import pandas as pd
from django.core.management.base import BaseCommand
from gallery.models import Gallery

class Command(BaseCommand):
    help = 'Import gallery data from Excel file using Lat/Long from Excel'

    def handle(self, *args, **kwargs):
        file_path = "media/gallery_data.xlsx"

        # Delete old data
        Gallery.objects.all().delete()
        self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries."))

        # Read Excel
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            name = str(row.get("Gallery Name", "")).strip()
            if not name or name.lower() == "nan":
                continue  # Skip blank names

            address = str(row.get("Address", "")).strip()
            area = str(row.get("Gallery Area", "")).strip()
            state = str(row.get("State", "")).strip()
            postcode = str(row.get("Postcode", "")).strip()
            contact_number = str(row.get("Contact number", "")).strip()
            opening_hours = str(row.get("Opening Hours in full", "")).strip()
            days_closed = str(row.get("Days closed", "")).strip()
            overview = str(row.get("Gallery Overview", "")).strip()
            website = str(row.get("Website", "")).strip()

            # ✅ Read Lat/Long from Excel directly
            lat = row.get("Lat") or row.get("Latitude")
            lng = row.get("Long") or row.get("Longitude")

            # Convert to float if valid
            try:
                lat = float(lat) if pd.notna(lat) else None
                lng = float(lng) if pd.notna(lng) else None
            except ValueError:
                lat, lng = None, None

            # Create gallery in DB
            try:
                Gallery.objects.create(
                    user_id=1,  # default admin or first user
                    name=name,
                    website=website if website.lower() != "nan" else None,
                    address=address if address.lower() != "nan" else None,
                    area=area if area.lower() != "nan" else None,
                    state=state if state.lower() != "nan" else None,
                    postcode=postcode if postcode.lower() != "nan" else None,
                    contact_number=contact_number if contact_number.lower() != "nan" else None,
                    opening_hours=opening_hours if opening_hours.lower() != "nan" else None,
                    days_closed=days_closed if days_closed.lower() != "nan" else None,
                    overview=overview if overview.lower() != "nan" else None,
                    lat=lat,
                    long=lng
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Imported: {name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error importing '{name}': {e}"))
