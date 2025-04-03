from flask import render_template, request
from app import db
from app.models import Property
from . import main_bp

@main_bp.route('/')
@main_bp.route('/index')
def index():
    # Basic pagination (e.g., 10 properties per page)
    page = request.args.get('page', 1, type=int)
    select_query = db.select(Property).order_by(Property.sale_date.desc())
    pagination = db.paginate(select_query, page=page, per_page=10, error_out=False)
    properties = pagination.items
    return render_template('index.html', title='Sold Properties', properties=properties, pagination=pagination)

# Add more routes here as needed (e.g., for property details)
