# import pandas as pd
# from django.core.management.base import BaseCommand
# from gallery.models import Gallery

# class Command(BaseCommand):
#     help = 'Import gallery data from Excel file using Lat/Long from Excel'

#     def handle(self, *args, **kwargs):
#         file_path = "media/gallery_data.xlsx"

#         # Delete old data
#         Gallery.objects.all().delete()
#         self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries."))

#         # Read Excel
#         df = pd.read_excel(file_path)

#         for _, row in df.iterrows():
#             name = str(row.get("Gallery Name", "")).strip()
#             if not name or name.lower() == "nan":
#                 continue  # Skip blank names

#             address = str(row.get("Address", "")).strip()
#             area = str(row.get("Gallery Area", "")).strip()
#             state = str(row.get("State", "")).strip()
#             postcode = str(row.get("Postcode", "")).strip()
#             contact_number = str(row.get("Contact number", "")).strip()
#             opening_hours = str(row.get("Opening Hours in full", "")).strip()
#             days_closed = str(row.get("Days closed", "")).strip()
#             overview = str(row.get("Gallery Overview", "")).strip()
#             website = str(row.get("Website", "")).strip()

#             # ✅ Read Lat/Long from Excel directly
#             lat = row.get("Lat") or row.get("Latitude")
#             lng = row.get("Long") or row.get("Longitude")

#             # Convert to float if valid
#             try:
#                 lat = float(lat) if pd.notna(lat) else None
#                 lng = float(lng) if pd.notna(lng) else None
#             except ValueError:
#                 lat, lng = None, None

#             # Create gallery in DB
#             try:
#                 Gallery.objects.create(
#                     user_id=1,  # default admin or first user
#                     name=name,
#                     website=website if website.lower() != "nan" else None,
#                     address=address if address.lower() != "nan" else None,
#                     area=area if area.lower() != "nan" else None,
#                     state=state if state.lower() != "nan" else None,
#                     postcode=postcode if postcode.lower() != "nan" else None,
#                     contact_number=contact_number if contact_number.lower() != "nan" else None,
#                     opening_hours=opening_hours if opening_hours.lower() != "nan" else None,
#                     days_closed=days_closed if days_closed.lower() != "nan" else None,
#                     overview=overview if overview.lower() != "nan" else None,
#                     lat=lat,
#                     long=lng
#                 )
#                 self.stdout.write(self.style.SUCCESS(f"✅ Imported: {name}"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"❌ Error importing '{name}': {e}"))


# import pandas as pd
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from gallery.models import Gallery

# class Command(BaseCommand):
#     help = 'Import gallery data from Excel file into the updated Gallery model'

#     def handle(self, *args, **kwargs):
#         file_path = "media/gallery.xlsx"

#         # Ensure a default user exists
#         default_user, created = User.objects.get_or_create(
#             username='admin',
#             defaults={'email': 'admin@example.com', 'password': 'pbkdf2_sha256$260000$randomsalt$hash'}  # Set a default password
#         )
#         if created:
#             default_user.set_password('admin123')  # Set a usable password
#             default_user.save()
#             self.stdout.write(self.style.SUCCESS(f"✅ Created default user: {default_user.username}"))

#         # Delete old gallery data
#         Gallery.objects.all().delete()
#         self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries."))

#         # Read Excel
#         try:
#             df = pd.read_excel(file_path)
#             self.stdout.write(f"Excel columns: {list(df.columns)}")
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
#             return

#         consecutive_empty = 0
#         max_consecutive_empty = 100
#         imported_count = 0
#         total_rows = len(df)

#         for index, row in df.iterrows():
#             try:
#                 name = str(row.get("Gallery Name", "")).strip()
#                 if not name or name.lower() == "nan" or name in [
#                     'Greater Sydney', 'Central Coast', 'Northern Rivers', 'Southern Highlands',
#                     'South Coast', 'Blue Mountains', 'Greater NSW'
#                 ]:  # Skip region headers
#                     self.stdout.write(self.style.WARNING(f"⚠ Skipped: Blank or invalid name in row {index} ('{name}')"))
#                     consecutive_empty += 1
#                     if consecutive_empty >= max_consecutive_empty:
#                         self.stdout.write(self.style.WARNING(f"⚠ Stopping import after {max_consecutive_empty} consecutive empty rows"))
#                         break
#                     continue
#                 consecutive_empty = 0

#                 # Map Excel columns to model fields
#                 address = str(row.get("Address", "")).strip()
#                 area = str(row.get("Gallery Area", "")).strip()
#                 suburb = str(row.get("Suburb", "")).strip()
#                 state = str(row.get("State", "")).strip()
#                 postcode = str(row.get("Postcode", "")).strip()
#                 contact_number = str(row.get("Contact number", "")).strip()
#                 opening_hours_full = str(row.get("Opening Hours in full", "")).strip()
#                 opening_hours_breakdown = str(row.get("Opening Hours (broken down by day in menu)", "")).strip()
#                 days_closed = str(row.get("Days closed", "")).strip()
#                 closed_for_holidays = str(row.get("Closed for holidays", "")).strip()
#                 overview = str(row.get("Gallery Overview", "")).strip()
#                 website = str(row.get("Website", "")).strip()
#                 instagram = str(row.get("Instagram", "")).strip()
#                 facebook = str(row.get("Facebook", "")).strip()
#                 art_artist = str(row.get("Art Artist", "")).strip()
#                 art_title = str(row.get("Art Title", "")).strip()
#                 art_price = str(row.get("Art Price", "")).strip()
#                 serial_no = str(row.get("S No. (As per Map)", "")).strip()
#                 paid_until = str(row.get("Paid Until", "")).strip()
#                 gallery_active = str(row.get("Gallery Active", "")).strip()
#                 password_login = str(row.get("Password Login", "")).strip()
#                 email_signin = str(row.get("Email Signin", "")).strip()

#                 # Handle Lat/Long
#                 lat = row.get("Lat") or row.get("Latitude")
#                 long = row.get("Long") or row.get("Longitude")
#                 try:
#                     lat = float(lat) if pd.notna(lat) else None
#                     long = float(long) if pd.notna(long) else None
#                 except (ValueError, TypeError):
#                     lat, long = None, None

#                 # Convert "nan" strings to None for optional fields
#                 fields = {
#                     'website': website if website.lower() != "nan" else None,
#                     'address': address if address.lower() != "nan" else None,
#                     'area': area if area.lower() != "nan" else None,
#                     'suburb': suburb if suburb.lower() != "nan" else None,
#                     'state': state if state.lower() != "nan" else None,
#                     'postcode': postcode if postcode.lower() != "nan" else None,
#                     'contact_number': contact_number if contact_number.lower() != "nan" else None,
#                     'opening_hours_full': opening_hours_full if opening_hours_full.lower() != "nan" else None,
#                     'opening_hours_breakdown': opening_hours_breakdown if opening_hours_breakdown.lower() != "nan" else None,
#                     'days_closed': days_closed if days_closed.lower() != "nan" else None,
#                     'closed_for_holidays': closed_for_holidays if closed_for_holidays.lower() != "nan" else None,
#                     'overview': overview if overview.lower() != "nan" else None,
#                     'instagram': instagram if instagram.lower() != "nan" else None,
#                     'facebook': facebook if facebook.lower() != "nan" else None,
#                     'art_artist': art_artist if art_artist.lower() != "nan" else None,
#                     'art_title': art_title if art_title.lower() != "nan" else None,
#                     'art_price': art_price if art_price.lower() != "nan" else None,
#                     'serial_no': serial_no if serial_no.lower() != "nan" else None,
#                     'paid_until': paid_until if paid_until.lower() != "nan" else None,
#                     'gallery_active': gallery_active if gallery_active.lower() != "nan" else None,
#                     'password_login': password_login if password_login.lower() != "nan" else None,
#                     'email_signin': email_signin if email_signin.lower() != "nan" else None,
#                     'lat': lat,
#                     'long': long,
#                 }

#                 # Create gallery in DB
#                 try:
#                     Gallery.objects.create(
#                         user=default_user,  # Use the default user
#                         name=name,
#                         **fields
#                     )
#                     imported_count += 1
#                     self.stdout.write(self.style.SUCCESS(f"✅ Imported: {name}"))
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"❌ Error importing '{name}': {e}"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"❌ Error processing row {index}: {e}"))
#                 continue

#         self.stdout.write(self.style.SUCCESS(f"Processed {total_rows} rows, imported {imported_count} galleries"))

# import pandas as pd
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from gallery.models import Gallery

# class Command(BaseCommand):
#     help = 'Import gallery data from Excel file into the updated Gallery model'

#     def handle(self, *args, **kwargs):
#         file_path = "media/gallery.xlsx"

#         # Ensure a default user exists
#         default_user, created = User.objects.get_or_create(
#             username='admin',
#             defaults={'email': 'admin@example.com', 'password': 'pbkdf2_sha256$260000$randomsalt$hash'}
#         )
#         if created:
#             default_user.set_password('admin123')
#             default_user.save()
#             self.stdout.write(self.style.SUCCESS(f"✅ Created default user: {default_user.username}"))

#         # Delete old gallery data
#         Gallery.objects.all().delete()
#         self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries."))

#         # Read Excel with dtype to treat Postcode as string
#         try:
#             df = pd.read_excel(file_path, dtype={"Postcode": str})
#             self.stdout.write(f"Excel columns: {list(df.columns)}")
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
#             return

#         consecutive_empty = 0
#         max_consecutive_empty = 100
#         imported_count = 0
#         total_rows = len(df)

#         for index, row in df.iterrows():
#             try:
#                 name = str(row.get("Gallery Name", "")).strip()
#                 if not name or name.lower() == "nan" or name in [
#                     'Greater Sydney', 'Central Coast', 'Northern Rivers', 'Southern Highlands',
#                     'South Coast', 'Blue Mountains', 'Greater NSW'
#                 ]:
#                     self.stdout.write(self.style.WARNING(f"⚠ Skipped: Blank or invalid name in row {index} ('{name}')"))
#                     consecutive_empty += 1
#                     if consecutive_empty >= max_consecutive_empty:
#                         self.stdout.write(self.style.WARNING(f"⚠ Stopping import after {max_consecutive_empty} consecutive empty rows"))
#                         break
#                     continue
#                 consecutive_empty = 0

#                 # Map Excel columns to model fields
#                 address = str(row.get("Address", "")).strip()
#                 area = str(row.get("Gallery Area", "")).strip()
#                 suburb = str(row.get("Suburb", "")).strip()
#                 state = str(row.get("State", "")).strip()
#                 # Clean postcode to remove .0
#                 postcode = str(row.get("Postcode", "")).strip()
#                 if postcode.lower() == "nan" or not postcode:
#                     postcode = None
#                 elif '.' in postcode:
#                     try:
#                         postcode = str(int(float(postcode)))  # Convert 2000.0 to "2000"
#                     except (ValueError, TypeError):
#                         postcode = None
#                 contact_number = str(row.get("Contact number", "")).strip()
#                 opening_hours_full = str(row.get("Opening Hours in full", "")).strip()
#                 opening_hours_breakdown = str(row.get("Opening Hours (broken down by day in menu)", "")).strip()
#                 days_closed = str(row.get("Days closed", "")).strip()
#                 closed_for_holidays = str(row.get("Closed for holidays", "")).strip()
#                 overview = str(row.get("Gallery Overview", "")).strip()
#                 website = str(row.get("Website", "")).strip()
#                 instagram = str(row.get("Instagram", "")).strip()
#                 facebook = str(row.get("Facebook", "")).strip()
#                 art_artist = str(row.get("Art Artist", "")).strip()
#                 art_title = str(row.get("Art Title", "")).strip()
#                 art_price = str(row.get("Art Price", "")).strip()
#                 serial_no = str(row.get("S No. (As per Map)", "")).strip()
#                 paid_until = str(row.get("Paid Until", "")).strip()
#                 gallery_active = str(row.get("Gallery Active", "")).strip()
#                 password_login = str(row.get("Password Login", "")).strip()
#                 email_signin = str(row.get("Email Signin", "")).strip()

#                 # Handle Lat/Long
#                 lat = row.get("Lat") or row.get("Latitude")
#                 long = row.get("Long") or row.get("Longitude")
#                 try:
#                     lat = float(lat) if pd.notna(lat) else None
#                     long = float(long) if pd.notna(long) else None
#                 except (ValueError, TypeError):
#                     lat, long = None, None

#                 # Convert "nan" strings to None for optional fields
#                 fields = {
#                     'website': website if website.lower() != "nan" else None,
#                     'address': address if address.lower() != "nan" else None,
#                     'area': area if area.lower() != "nan" else None,
#                     'suburb': suburb if suburb.lower() != "nan" else None,
#                     'state': state if state.lower() != "nan" else None,
#                     'postcode': postcode,
#                     'contact_number': contact_number if contact_number.lower() != "nan" else None,
#                     'opening_hours_full': opening_hours_full if opening_hours_full.lower() != "nan" else None,
#                     'opening_hours_breakdown': opening_hours_breakdown if opening_hours_breakdown.lower() != "nan" else None,
#                     'days_closed': days_closed if days_closed.lower() != "nan" else None,
#                     'closed_for_holidays': closed_for_holidays if closed_for_holidays.lower() != "nan" else None,
#                     'overview': overview if overview.lower() != "nan" else None,
#                     'instagram': instagram if instagram.lower() != "nan" else None,
#                     'facebook': facebook if facebook.lower() != "nan" else None,
#                     'art_artist': art_artist if art_artist.lower() != "nan" else None,
#                     'art_title': art_title if art_title.lower() != "nan" else None,
#                     'art_price': art_price if art_price.lower() != "nan" else None,
#                     'serial_no': serial_no if serial_no.lower() != "nan" else None,
#                     'paid_until': paid_until if paid_until.lower() != "nan" else None,
#                     'gallery_active': gallery_active if gallery_active.lower() != "nan" else None,
#                     'password_login': password_login if password_login.lower() != "nan" else None,
#                     'email_signin': email_signin if email_signin.lower() != "nan" else None,
#                     'lat': lat,
#                     'long': long,
#                 }

#                 # Create gallery in DB
#                 try:
#                     Gallery.objects.create(
#                         user=default_user,
#                         name=name,
#                         **fields
#                     )
#                     imported_count += 1
#                     self.stdout.write(self.style.SUCCESS(f"✅ Imported: {name}"))
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"❌ Error importing '{name}': {e}"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"❌ Error processing row {index}: {e}"))
#                 continue

#         self.stdout.write(self.style.SUCCESS(f"Processed {total_rows} rows, imported {imported_count} galleries"))

# import pandas as pd
# import re
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from gallery.models import Gallery, GalleryImage, Exhibition
# import os
# from django.core.files import File
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Import gallery data from Excel file into the updated Gallery model'

#     def handle(self, *args, **kwargs):
#         file_path = "media/gallery.xlsx"

#         # Ensure a default user exists
#         default_user, created = User.objects.get_or_create(
#             username='admin',
#             defaults={'email': 'admin@example.com', 'password': 'pbkdf2_sha256$260000$randomsalt$hash'}
#         )
#         if created:
#             default_user.set_password('admin123')
#             default_user.save()
#             self.stdout.write(self.style.SUCCESS(f"✅ Created default user: {default_user.username}"))

#         # Delete old data
#         Gallery.objects.all().delete()
#         Exhibition.objects.all().delete()
#         self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries and exhibitions."))

#         # Read Excel with dtype to treat Postcode and S No. as strings
#         try:
#             df = pd.read_excel(file_path, dtype={"Postcode": str, "S No. (As per Map)": str})
#             self.stdout.write(f"Excel columns: {list(df.columns)}")
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
#             return

#         consecutive_empty = 0
#         max_consecutive_empty = 100
#         imported_count = 0
#         total_rows = len(df)

#         for index, row in df.iterrows():
#             try:
#                 name = str(row.get("Gallery Name", "")).strip()
#                 if not name or name.lower() == "nan" or name in [
#                     'Greater Sydney', 'Central Coast', 'Northern Rivers', 'Southern Highlands',
#                     'South Coast', 'Blue Mountains', 'Greater NSW'
#                 ]:
#                     self.stdout.write(self.style.WARNING(f"⚠ Skipped: Blank or invalid name in row {index} ('{name}')"))
#                     consecutive_empty += 1
#                     if consecutive_empty >= max_consecutive_empty:
#                         self.stdout.write(self.style.WARNING(f"⚠ Stopping import after {max_consecutive_empty} consecutive empty rows"))
#                         break
#                     continue
#                 consecutive_empty = 0

#                 # Map Excel columns to model fields
#                 address = str(row.get("Address", "")).strip()
#                 area = str(row.get("Gallery Area", "")).strip()
#                 suburb = str(row.get("Suburb", "")).strip()
#                 state = str(row.get("State", "")).strip()
#                 # Clean postcode
#                 postcode = str(row.get("Postcode", "")).strip()
#                 if postcode.lower() == "nan" or not postcode:
#                     postcode = None
#                 elif '.' in postcode:
#                     try:
#                         postcode = str(int(float(postcode)))
#                     except (ValueError, TypeError):
#                         postcode = None
#                 contact_number = str(row.get("Contact number", "")).strip()
#                 # Clean opening_hours_full to remove "open", colons, and spaces
#                 opening_hours_full = str(row.get("Opening Hours in full", "")).strip()
#                 if opening_hours_full.lower() != "nan":
#                     # Remove "open", colons, and spaces
#                     opening_hours_full = re.sub(r'\bopen\b|[ :]','', opening_hours_full, flags=re.IGNORECASE).strip()
#                 else:
#                     opening_hours_full = None
#                 opening_hours_breakdown = str(row.get("Opening Hours (broken down by day in menu)", "")).strip()
#                 days_closed = str(row.get("Days closed", "")).strip()
#                 closed_for_holidays = str(row.get("Closed for holidays", "")).strip()
#                 overview = str(row.get("Gallery Overview", "")).strip()
#                 website = str(row.get("Website", "")).strip()
#                 instagram = str(row.get("Instagram", "")).strip()
#                 facebook = str(row.get("Facebook", "")).strip()
#                 art_artist = str(row.get("Art Artist", "")).strip()
#                 art_title = str(row.get("Art Title", "")).strip()
#                 art_price = str(row.get("Art Price", "")).strip()
#                 # Clean serial_no
#                 serial_no = str(row.get("S No. (As per Map)", "")).strip()
#                 if serial_no.lower() == "nan" or not serial_no:
#                     serial_no = None
#                 elif '.' in serial_no:
#                     try:
#                         serial_no = str(int(float(serial_no)))
#                     except (ValueError, TypeError):
#                         serial_no = None
#                 paid_until = str(row.get("Paid Until", "")).strip()
#                 gallery_active = str(row.get("Gallery Active", "")).strip()
#                 password_login = str(row.get("Password Login", "")).strip()
#                 email_signin = str(row.get("Email Signin", "")).strip()

#                 # Handle Lat/Long
#                 lat = row.get("Lat") or row.get("Latitude")
#                 long = row.get("Long") or row.get("Longitude")
#                 try:
#                     lat = float(lat) if pd.notna(lat) else None
#                     long = float(long) if pd.notna(long) else None
#                 except (ValueError, TypeError):
#                     lat, long = None, None

#                 # Handle exhibition data (adjust column names as needed)
#                 exhibition_title = str(row.get("Exhibition Title", "")).strip()
#                 exhibition_artist = str(row.get("Exhibition Artist", "")).strip()
#                 exhibition_start_date = str(row.get("Start Date", "")).strip()
#                 exhibition_end_date = str(row.get("End Date", "")).strip()
#                 exhibition_description = str(row.get("Exhibition Description", "")).strip()

#                 # Convert "nan" strings to None for optional fields
#                 fields = {
#                     'website': website if website.lower() != "nan" else None,
#                     'address': address if address.lower() != "nan" else None,
#                     'area': area if area.lower() != "nan" else None,
#                     'suburb': suburb if suburb.lower() != "nan" else None,
#                     'state': state if state.lower() != "nan" else None,
#                     'postcode': postcode,
#                     'contact_number': contact_number if contact_number.lower() != "nan" else None,
#                     'opening_hours_full': opening_hours_full if opening_hours_full else None,
#                     'opening_hours_breakdown': opening_hours_breakdown if opening_hours_breakdown.lower() != "nan" else None,
#                     'days_closed': days_closed if days_closed.lower() != "nan" else None,
#                     'closed_for_holidays': closed_for_holidays if closed_for_holidays.lower() != "nan" else None,
#                     'overview': overview if overview.lower() != "nan" else None,
#                     'instagram': instagram if instagram.lower() != "nan" else None,
#                     'facebook': facebook if facebook.lower() != "nan" else None,
#                     'art_artist': art_artist if art_artist.lower() != "nan" else None,
#                     'art_title': art_title if art_title.lower() != "nan" else None,
#                     'art_price': art_price if art_price.lower() != "nan" else None,
#                     'serial_no': serial_no,
#                     'paid_until': paid_until if paid_until.lower() != "nan" else None,
#                     'gallery_active': gallery_active if gallery_active.lower() != "nan" else None,
#                     'password_login': password_login if password_login.lower() != "nan" else None,
#                     'email_signin': email_signin if email_signin.lower() != "nan" else None,
#                     'lat': lat,
#                     'long': long,
#                 }

#                 # Create gallery
#                 try:
#                     gallery = Gallery.objects.create(
#                         user=default_user,
#                         name=name,
#                         **fields
#                     )
#                     imported_count += 1
#                     self.stdout.write(self.style.SUCCESS(f"✅ Imported: {name}"))

#                     # Create exhibition if data exists
#                     if exhibition_title and exhibition_title.lower() != "nan":
#                         try:
#                             start_date = datetime.strptime(exhibition_start_date, '%Y-%m-%d').date() if exhibition_start_date and exhibition_start_date.lower() != "nan" else None
#                             end_date = datetime.strptime(exhibition_end_date, '%Y-%m-%d').date() if exhibition_end_date and exhibition_end_date.lower() != "nan" else None
#                             if start_date and end_date:
#                                 Exhibition.objects.create(
#                                     gallery=gallery,
#                                     title=exhibition_title,
#                                     artist=exhibition_artist if exhibition_artist.lower() != "nan" else "",
#                                     start_date=start_date,
#                                     end_date=end_date,
#                                     description=exhibition_description if exhibition_description.lower() != "nan" else ""
#                                 )
#                                 self.stdout.write(self.style.SUCCESS(f"✅ Added exhibition: {exhibition_title} for {name}"))
#                         except ValueError as e:
#                             self.stdout.write(self.style.ERROR(f"❌ Error adding exhibition for {name}: Invalid date format ({e})"))
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"❌ Error importing '{name}': {e}"))
#             except Exception as e:
#                 self.stdout.write(self.style.ERROR(f"❌ Error processing row {index}: {e}"))
#                 continue

#         self.stdout.write(self.style.SUCCESS(f"Processed {total_rows} rows, imported {imported_count} galleries"))


# import_galleries.py (updated)
import pandas as pd
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gallery.models import Gallery, GalleryImage, Exhibition, Artist
import os
from django.core.files import File
from datetime import datetime

class Command(BaseCommand):
    help = 'Import gallery data from Excel file into the Gallery model'

    def handle(self, *args, **kwargs):
        file_path = "media/Enroute-db.xlsx"

        # Ensure a default user exists
        default_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'password': 'pbkdf2_sha256$260000$randomsalt$hash'}
        )
        if created:
            default_user.set_password('admin123')
            default_user.save()
            self.stdout.write(self.style.SUCCESS(f"✅ Created default user: {default_user.username}"))

        # Delete old data
        Gallery.objects.all().delete()
        Exhibition.objects.all().delete()
        Artist.objects.all().delete()
        self.stdout.write(self.style.WARNING("⚠ Deleted all old galleries, exhibitions, and artists."))

        # Check if file exists
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        # Read Excel with dtype to treat Postcode as string
        try:
            df = pd.read_excel(file_path, dtype={"Postcode": str})
            self.stdout.write(f"Excel columns: {list(df.columns)}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
            return

        consecutive_empty = 0
        max_consecutive_empty = 100
        imported_count = 0
        total_rows = len(df)

        for index, row in df.iterrows():
            try:
                name = str(row.get("Gallery Name", "")).strip()
                if not name or name.lower() == "nan" or name in [
                    'Greater Sydney', 'Central Coast', 'Northern Rivers', 'Southern Highlands',
                    'South Coast', 'Blue Mountains', 'Greater NSW'
                ]:
                    self.stdout.write(self.style.WARNING(f"⚠ Skipped: Blank or invalid name in row {index+2} ('{name}')"))
                    consecutive_empty += 1
                    if consecutive_empty >= max_consecutive_empty:
                        self.stdout.write(self.style.WARNING(f"⚠ Stopping import after {max_consecutive_empty} consecutive empty rows"))
                        break
                    continue
                consecutive_empty = 0

                # Map Excel columns to model fields
                address = str(row.get("Address", "")).strip()
                area = str(row.get("Gallery Area", "")).strip()
                suburb = str(row.get("Suburb", "")).strip()
                state = str(row.get("State", "")).strip()
                postcode = str(row.get("Postcode", "")).strip()
                if postcode.lower() == "nan" or not postcode:
                    postcode = None
                elif '.' in postcode:
                    try:
                        postcode = str(int(float(postcode)))
                    except (ValueError, TypeError):
                        postcode = None
                contact_number = str(row.get("Contact number", "")).strip()
                opening_hours_full = str(row.get("Opening Hours in full", "")).strip()
                opening_hours_breakdown = str(row.get("Opening Hours (broken down by day in menu)", "")).strip()
                days_closed = str(row.get("Days closed", "")).strip()
                closed_for_holidays = str(row.get("Closed for holidays", "")).strip()
                overview = str(row.get("Gallery Overview", "")).strip()
                website = str(row.get("Website", "")).strip()
                instagram = str(row.get("Instagram", "")).strip()
                facebook = str(row.get("Facebook", "")).strip()
                art_artist = str(row.get("Art Artist", "")).strip()
                art_title = str(row.get("Art Title", "")).strip()
                art_price = str(row.get("Art Price", "")).strip()
                paid_until = str(row.get("Paid Until", "")).strip()
                gallery_active = str(row.get("Gallery Active", "")).strip()
                password_login = str(row.get("Password Login", "")).strip()
                email_signin = str(row.get("Email Signin", "")).strip()
                self.stdout.write(f"Row {index+2} - {name}: email_signin='{email_signin}', paid_until='{paid_until}', gallery_active='{gallery_active}'")

                # Handle Lat/Long
                lat = row.get("Lat") or row.get("Latitude")
                long = row.get("Long") or row.get("Longitude")
                try:
                    lat = float(lat) if pd.notna(lat) else None
                    long = float(long) if pd.notna(long) else None
                except (ValueError, TypeError):
                    lat, long = None, None

                # Handle paid_until
                paid_until_date = None
                if paid_until and paid_until.lower() != "nan":
                    try:
                        paid_until_date = datetime.strptime(paid_until, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f"⚠ Row {index+2} - Invalid paid_until date format: {paid_until}"))

                # Handle gallery_active
                gallery_active_bool = True
                if gallery_active and gallery_active.lower() != "nan":
                    gallery_active_bool = gallery_active.lower() in ['y', 'yes', 'true', '1']

                # Handle exhibition data
                exhibition_title = str(row.get("Exhibition Title", "")).strip()
                exhibition_artist = str(row.get("Exhibition Artist", "")).strip()
                exhibition_start_date = str(row.get("Start Date", "")).strip()
                exhibition_end_date = str(row.get("End Date", "")).strip()
                exhibition_description = str(row.get("Exhibition Description", "")).strip()
                self.stdout.write(f"Row {index+2} - {name}: exhibition_title='{exhibition_title}', exhibition_artists='{exhibition_artist}'")

                # Convert "nan" strings to None for optional fields
                fields = {
                    'website': website if website.lower() != "nan" else None,
                    'address': address if address.lower() != "nan" else None,
                    'area': area if area.lower() != "nan" else None,
                    'suburb': suburb if suburb.lower() != "nan" else None,
                    'state': state if state.lower() != "nan" else None,
                    'postcode': postcode,
                    'contact_number': contact_number if contact_number.lower() != "nan" else None,
                    'opening_hours_full': opening_hours_full if opening_hours_full.lower() != "nan" else None,
                    'opening_hours_breakdown': opening_hours_breakdown if opening_hours_breakdown.lower() != "nan" else None,
                    'days_closed': days_closed if days_closed.lower() != "nan" else None,
                    'closed_for_holidays': closed_for_holidays if closed_for_holidays.lower() != "nan" else None,
                    'overview': overview if overview.lower() != "nan" else None,
                    'instagram': instagram if instagram.lower() != "nan" else None,
                    'facebook': facebook if facebook.lower() != "nan" else None,
                    'art_artist': art_artist if art_artist.lower() != "nan" else None,
                    'art_title': art_title if art_title.lower() != "nan" else None,
                    'art_price': art_price if art_price.lower() != "nan" else None,
                    'paid_until': paid_until_date,
                    'gallery_active': gallery_active_bool,
                    'password_login': password_login if password_login.lower() != "nan" else None,
                    'email_signin': email_signin if email_signin.lower() != "nan" else None,
                    'lat': lat,
                    'long': long,
                }

                # Create gallery
                try:
                    gallery = Gallery.objects.create(
                        user=default_user,
                        name=name,
                        **fields
                    )
                    imported_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Row {index+2} - Imported: {name} (email_signin: {gallery.email_signin}, paid_until: {gallery.paid_until}, gallery_active: {gallery.gallery_active})"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"❌ Row {index+2} - Error importing '{name}': {e}"))
                    continue

                # Create exhibition if data exists
                if exhibition_title and exhibition_title.lower() != "nan":
                    try:
                        start_date = datetime.strptime(exhibition_start_date, '%Y-%m-%d').date() if exhibition_start_date and exhibition_start_date.lower() != "nan" else None
                        end_date = datetime.strptime(exhibition_end_date, '%Y-%m-%d').date() if exhibition_end_date and exhibition_end_date.lower() != "nan" else None
                        if start_date and end_date:
                            exhibition = Exhibition.objects.create(
                                gallery=gallery,
                                title=exhibition_title,
                                description=exhibition_description if exhibition_description.lower() != "nan" else ""
                            )
                            # Debug: Log all artists in DB and for this exhibition
                            self.stdout.write(f"Row {index+2} - All artists in DB: {[str(a) for a in Artist.objects.all()]}")
                            self.stdout.write(f"Row {index+2} - Before clearing, {exhibition_title} artists: {[str(a) for a in exhibition.artists.all()]}")
                            # Clear existing artists
                            exhibition.artists.clear()
                            self.stdout.write(f"Row {index+2} - After clearing, {exhibition_title} artists: {[str(a) for a in exhibition.artists.all()]}")
                            # Parse and assign artists
                            if exhibition_artist and exhibition_artist.lower() != "nan":
                                artist_names = [name.strip() for name in exhibition_artist.split(',')]
                                self.stdout.write(f"Row {index+2} - Processing artists: {artist_names}")
                                for name in artist_names:
                                    if name:
                                        parts = name.split()
                                        if len(parts) >= 2:
                                            first_name = parts[0]
                                            last_name = ' '.join(parts[1:])
                                        else:
                                            first_name = name
                                            last_name = ''
                                        artist, created = Artist.objects.get_or_create(
                                            first_name=first_name,
                                            last_name=last_name
                                        )
                                        exhibition.artists.add(artist)
                                        self.stdout.write(self.style.SUCCESS(f"✅ Row {index+2} - Added artist: {artist} to {exhibition_title} (ID: {exhibition.id}, Created: {created})"))
                            else:
                                self.stdout.write(f"Row {index+2} - No artists provided for {exhibition_title}")
                            self.stdout.write(self.style.SUCCESS(f"✅ Row {index+2} - Added exhibition: {exhibition_title} for {name} (ID: {exhibition.id}, start_date: {start_date}, end_date: {end_date})"))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"❌ Row {index+2} - Error adding exhibition for {name}: Invalid date format ({e})"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Row {index+2} - Error adding exhibition for {name}: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Row {index+2} - Error processing row: {e}"))
                continue

        self.stdout.write(self.style.SUCCESS(f"Processed {total_rows} rows, imported {imported_count} galleries"))