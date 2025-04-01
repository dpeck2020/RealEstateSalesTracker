# RealEstateSalesTracker\n\nA web application to scrape and display real estate sales data for Essex County, MA.\n\n## Project Goal\n\nCreate a functional tool using Python (Flask, SQLAlchemy, BeautifulSoup) and a JavaScript frontend to:\n1. Scrape recently sold properties from Realtor.com.\n2. Scrape buyer/seller information from SalemDeeds.com.\n3. Store the combined data in an SQLite database.\n4. Provide a web interface to filter and view the sales data.\n\n## Setup\n\n1. Clone the repository.\n2. Create a virtual environment: `python -m venv venv`\n3. Activate the virtual environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)\n4. Install dependencies: `pip install -r requirements.txt`\n5. Create a `.env` file for environment variables (e.g., `SECRET_KEY`).\n6. Run the application: `flask run` (or `python run.py`)\n
