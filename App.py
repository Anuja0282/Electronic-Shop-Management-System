import cx_Oracle
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# from module import Customersdetails, AvailableProducts

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@localhost:1521/xe'
db = SQLAlchemy(app)


class AvailableProducts(db.Model):
    p_brand = db.Column(db.String(20), unique=False, nullable=False)
    p_id = db.Column(db.Integer(), primary_key=True)
    p_name = db.Column(db.String(20), unique=True, nullable=False)
    p_quantity = db.Column(db.Integer(), unique=False, nullable=False)
    p_price = db.Column(db.Integer(), unique=False, nullable=False)


@app.route('/productInfo', methods=['GET', 'POST'])
def ProductInfo():
    if request.method == 'POST':
        'add entry to db'
        p_brand = request.form.get('p_brand')
        p_id = request.form.get('p_id')
        p_name = request.form.get('p_name')
        p_quantity = request.form.get('p_quantity')
        p_price = request.form.get('p_price')

        entry = AvailableProducts(p_brand=p_brand, p_id=p_id, p_name=p_name, p_quantity=p_quantity, p_price=p_price)

        db.session.add(entry)
        db.create_all()
        db.session.commit()

    return render_template('add.html')


class Customersdetails(db.Model):
    c_id = db.Column(db.Integer(), primary_key=True)
    c_name = db.Column(db.String(20), unique=False, nullable=False)
    c_email = db.Column(db.String(30), unique=False, nullable=False)
    c_qty = db.Column(db.Integer(), unique=False, nullable=False)
    pr_id = db.Column(db.Integer(), nullable=False)


@app.route('/custInfo', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        c_id = request.form.get('c_id')
        c_name = request.form.get('c_name')
        c_email = request.form.get('c_email')
        pr_id = request.form.get('pr_id')
        c_qty = request.form.get("c_qty")

        try:
            obj = AvailableProducts.query.filter_by(p_id=pr_id).first()
        except cx_Oracle.Error:
            available = 0
            return render_template('successp.html', available=available)
        except AttributeError:
            available = 0
            return render_template('successp.html', available=available)

        try:
            if int(obj.p_quantity) < int(c_qty):
                available = -1
                return render_template('successp.html', available=available)
            else:
                available = 1

                C_entry = Customersdetails(c_id=c_id, c_name=c_name, c_email=c_email, pr_id=pr_id, c_qty=c_qty)

                db.create_all()
                updateProduct(pr_id, c_qty)
                db.session.add(C_entry)
                db.session.commit()
            return render_template('successp.html', available=available)

        except AttributeError:
            available = 0
            return render_template('successp.html', available=available)


    return render_template('Buy.html')


def updateProduct(pr_id, c_qty):
    obj = AvailableProducts.query.filter_by(p_id=pr_id).first()
    x = int(obj.p_quantity) - int(c_qty)

    ap = AvailableProducts.query.get(pr_id)
    db.session.delete(ap)
    db.session.commit()
    entry = AvailableProducts(p_brand=obj.p_brand, p_id=obj.p_id, p_name=obj.p_name, p_quantity=x, p_price=obj.p_price)
    db.session.add(entry)
    db.session.commit()


@app.route('/Viewproducts')
def Viewproducts():
    return render_template('p_details2.html', AvailableProducts=AvailableProducts.query.all())


@app.route('/ViewCust')
def viewCustomers():
    return render_template('c_details2.html', Customersdetails=Customersdetails.query.all())


@app.route('/deleteprod', methods=['GET', 'POST'])
def deleteproducts():
    if request.method == 'POST':
        'add delete to db'

        p = request.form.get('p_id')
        ap = AvailableProducts.query.get(p)
        db.session.delete(ap)
        db.session.commit()
    else:
        return render_template('Delete_prd.html')
    return render_template('Delete_prd.html')


@app.route('/searchprod', methods=['GET', 'POST'])
def searchproduct():
    if request.method == 'POST':
        'search to db'

        p = request.form.get('p_id')
    else:
        return render_template('search_p.html')
    return render_template('p_details2.html', AvailableProducts=AvailableProducts.query.filter_by(p_id=p))


@app.route('/searchcust', methods=['GET', 'POST'])
def searchcustomer():
    if request.method == 'POST':
        'search to db'

        cid = request.form.get('c_id')
    else:
        return render_template('search_c.html')
    return render_template('c_details2.html', Customersdetails=Customersdetails.query.filter_by(c_id=cid))


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('main2.html')


@app.route("/product", methods=['GET', 'POST'])
def product():
    return render_template('Product2.html')


@app.route("/customer", methods=['GET', 'POST'])
def cust():
    return render_template('Customer.html')


if __name__ == '__main__':
    app.run(debug=True)
