from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    dr = DataRequired()
    #####
    cafe = StringField('Cafe name', validators=[dr])
    location = URLField("Location URL", validators=[dr, URL()])
    open = StringField("Open Time", validators=[dr])
    close = StringField("Close Time", validators=[dr])
    coffee = SelectField("Coffee", validators=[dr], choices=[x*"☕" for x in range(1,6)])
    wifi = SelectField("Wifi", validators=[dr], choices=[x*"💪" for x in range(1,6)])
    power = SelectField("Power", validators=[dr], choices=[x*"🔌" for x in range(1,6)])
    submit = SubmitField('Submit', validators=[dr])

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline="\n", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([form.cafe.data, form.location.data, form.open.data, form.close.data, form.coffee.data,
                                 form.wifi.data, form.power.data])
            return redirect(url_for("add_cafe"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
