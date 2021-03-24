"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app,db
from flask import render_template, flash, request, redirect, url_for,send_from_directory
from .forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Kyle Watson")

@app.route('/property', methods=["GET", "POST"])
def add_property():
    form=PropertyForm()
    if request.method=='POST' and form.validate_on_submit():
        title = request.form['title']
        NumBedrooms=request.form['NumBedrooms']
        NumBathrooms=request.form['NumBathrooms']
        location=request.form['location']
        price= request.form['price']
        propertyType = request.form['houseType']
        description=request.form['description']
        fileName= save_photos(form.photo.data) 
        _property = Property(title, description, NumBedrooms, NumBathrooms, price, propertyType, location,fileName)
        db.session.add(_property)
        db.session.commit()
        return redirect(url_for('display_properties'))
    return render_template('add_property.html',form=form)

@app.route('/properties', methods=["GET"])
def display_properties():
    allProperties=db.session.query(Property).all()
    return render_template('display_properties.html',properties=allProperties)


@app.route('/property/<propertyid>', methods=["GET"])
def display_property(propertyid):
    _property = db.session.query(Property).filter(Property.id == propertyid).first()
    return render_template('display_property.html', _property=_property)

@app.route('/get_image/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

def save_photos(photo):
    fileName = secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    return fileName
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
