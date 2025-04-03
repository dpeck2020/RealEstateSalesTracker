import csv
import json
import logging
import re
import os
from datetime import datetime

from app import create_app, db
from app.models import Property, PropertyImage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions for Cleaning Data ---
def clean_price(price_str):
    "Removes $, commas and converts to int. Returns None if invalid." 
    if not price_str:
        return None
    try:
        return int(re.sub(r'[$,]', '', price_str))
    except (ValueError, TypeError):
        return None

def parse_date(date_str):
    "Parses date string like 'MAR 26, 2025' into a date object. Returns None if invalid." 
    if not date_str:
        return None
    try:
        # Assuming format like 'MON DD, YYYY' (e.g., MAR 26, 2025)
        return datetime.strptime(date_str.strip(), '%b %d, %Y').date()
    except (ValueError, TypeError):
        logging.warning(f"Could not parse date: {date_str}")
        return None

def extract_sqft(sqft_str):
    "Extracts square footage number. Returns None if not found."
    if not sqft_str:
        return None
    match = re.search(r'^([\d,]+)\s*sqft', sqft_str.strip(), re.IGNORECASE)
    if match:
        try:
            return int(re.sub(r',', '', match.group(1)))
        except (ValueError, TypeError):
            return None
    return None

def extract_lot_size_acres(lot_str):
    "Extracts lot size in acres from strings like '(on 0.30 acres)'. Returns None if not found."
    if not lot_str:
        return None
    match = re.search(r'\(on\s+([\d.]+)\s+acres?\)', lot_str.strip(), re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except (ValueError, TypeError):
            return None
    return None

def extract_beds(bed_str):
    "Extracts number of bedrooms from '2bd'. Returns None if invalid."
    if not bed_str:
        return None
    match = re.match(r'(\d+)\s*bd', bed_str.strip(), re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except (ValueError, TypeError):
            return None
    return None

def extract_baths(bath_str):
    "Extracts number of bathrooms from '2ba' or '1.5ba'. Returns None if invalid."
    if not bath_str:
        return None
    match = re.match(r'([\d.]+)\s*ba', bath_str.strip(), re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except (ValueError, TypeError):
            return None
    return None

# --- Main Loading Function ---
def load_trulia_csv(csv_filepath):
    app = create_app()
    with app.app_context():
        logging.info(f"Starting CSV load from: {csv_filepath}")
        
        try:
            with open(csv_filepath, mode='r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader) # Skip header row
                logging.info(f"CSV Header: {header}")
                
                count = 0
                added_count = 0
                skipped_count = 0
                
                for row in reader:
                    count += 1
                    if len(row) < 14: # Ensure row has enough columns based on analysis
                        logging.warning(f"Row {count}: Insufficient columns ({len(row)}), skipping.")
                        skipped_count += 1
                        continue
                        
                    # --- Extract and Clean Data --- 
                    try:
                        address_json_str = row[0]
                        address_data = json.loads(address_json_str).get('address', {})
                        geo_data = json.loads(address_json_str).get('geo', {})
                        
                        street = address_data.get('streetAddress')
                        city = address_data.get('addressLocality')
                        state = address_data.get('addressRegion')
                        zip_code = address_data.get('postalCode')
                        
                        trulia_url = row[1]
                        image_url = row[2] # Primary image URL
                        
                        sale_status = row[4]
                        if sale_status.strip().upper() != 'SOLD':
                            logging.debug(f"Row {count}: Skipping non-SOLD property ({sale_status})")
                            skipped_count += 1
                            continue
                            
                        sale_date_str = row[5]
                        sale_price_str = row[6] # Corrected index for price
                        beds_str = row[9]
                        baths_str = row[11]
                        sqft_lot_str = row[13]
                        
                        latitude = geo_data.get('latitude')
                        longitude = geo_data.get('longitude')
                        
                        # Clean extracted data
                        sale_price = clean_price(sale_price_str)
                        sale_date = parse_date(sale_date_str)
                        bedrooms = extract_beds(beds_str)
                        bathrooms = extract_baths(baths_str)
                        square_footage = extract_sqft(sqft_lot_str)
                        lot_size = extract_lot_size_acres(sqft_lot_str)
                        
                        # Basic validation
                        if not all([street, city, state, zip_code, sale_price, sale_date]):
                            logging.warning(f"Row {count}: Missing essential data (Address, Price, or Date), skipping.")
                            skipped_count += 1
                            continue
                            
                        # --- Check for Duplicates (Optional but Recommended) ---
                        # Simple check based on address, could be more robust
                        existing_prop = db.session.execute(
                            db.select(Property).filter_by(street=street, city=city, zip_code=zip_code)
                        ).scalar_one_or_none()
                        
                        if existing_prop:
                            logging.debug(f"Row {count}: Property already exists at {street}, {city}, skipping.")
                            skipped_count += 1
                            continue
                            
                        # --- Create DB Objects --- 
                        new_property = Property(
                            street=street,
                            city=city,
                            state=state,
                            zip_code=zip_code,
                            sale_price=sale_price,
                            sale_date=sale_date,
                            square_footage=square_footage,
                            lot_size=lot_size,
                            trulia_url=trulia_url,
                            latitude=latitude,
                            longitude=longitude,
                            bedrooms=bedrooms,
                            bathrooms=bathrooms
                        )
                        
                        # Add image if URL is valid
                        if image_url and image_url.startswith('http'): # Basic check
                            new_image = PropertyImage(url=image_url, property=new_property)
                            db.session.add(new_image)
                        else:
                            logging.debug(f"Row {count}: Invalid or missing image URL: {image_url}")
                            
                        db.session.add(new_property)
                        added_count += 1
                        
                        # Commit in batches for performance
                        if added_count % 100 == 0:
                            db.session.commit()
                            logging.info(f"Committed batch of 100 properties. Total added: {added_count}")

                    except json.JSONDecodeError as e:
                        logging.error(f"Row {count}: Error decoding JSON in column 1: '{address_json_str[:100]}...'. Error: {e}, skipping row.")
                        skipped_count += 1
                    except Exception as e:
                        logging.error(f"Row {count}: Unexpected error processing row: {e}", exc_info=True)
                        skipped_count += 1
                        db.session.rollback() # Rollback potential partial add for this row
                        
            # Final commit for any remaining properties
            db.session.commit()
            logging.info(f"CSV loading finished.")
            logging.info(f"Total rows processed: {count}")
            logging.info(f"Properties added: {added_count}")
            logging.info(f"Rows skipped (errors, duplicates, or not SOLD): {skipped_count}")

        except FileNotFoundError:
            logging.error(f"Error: CSV file not found at {csv_filepath}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during CSV loading: {e}", exc_info=True)
            db.session.rollback() # Rollback any potential changes from the failed run

# --- Script Execution ---
if __name__ == "__main__":
    # Assumes the script is run from the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Construct the path relative to the project root
    default_csv_path = os.path.join(project_root, 'trulia1.csv') 
    
    csv_to_load = default_csv_path # Or get path from command-line arguments
    
    if os.path.exists(csv_to_load):
        load_trulia_csv(csv_to_load)
    else:
        logging.error(f"CSV file specified does not exist: {csv_to_load}")
