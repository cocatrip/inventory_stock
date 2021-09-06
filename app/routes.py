from flask import flash, request, render_template, url_for, redirect
from app import app
import requests
import json
import re

@app.route('/')
@app.route('/home')
def home():
    url = "http://192.168.100.102:7000/products"
    response = requests.get(url)
    products = json.loads(response.text)
    return render_template('index.html', products=products, home="active")

@app.route('/sell', methods=["GET","POST"])
def sell():
    url = "http://192.168.100.102:7000/products"
    response = requests.get(url)
    products = json.loads(response.text)
    if request.method == "POST":
        code = request.form["code"]
        url = f"http://192.168.100.102:7000/products/{code}"
        response = requests.get(url)
        product = json.loads(response.text)
        print(product)

        quantity = request.form["quantity"]
        stock = product['stock'] - int(quantity)

        payload={'stock': stock}
        response = requests.request("PUT", url, data=payload)
        return redirect(url_for('sell', success=0))
    else:
        return render_template('sell.html', products=products, sell="active")

@app.route('/product/<int:code>')
def product(code):
    url = "http://192.168.100.102:7000/products"
    response = requests.get(url)
    products = json.loads(response.text)
    url = f"http://192.168.100.102:7000/products/{code}"
    response = requests.get(url)
    product = json.loads(response.text)
    return render_template('product.html', products=products, product=product)

@app.route('/product/edit/<int:code>', methods=["GET","POST"])
def product_edit(code):
    url = "http://192.168.100.102:7000/products"
    response = requests.get(url)
    products = json.loads(response.text)
    url = f"http://192.168.100.102:7000/products/{code}"
    response = requests.get(url)
    product = json.loads(response.text)
    if request.method == "POST":
        stock = request.form["stock"]
        payload={'stock': stock}
        response = requests.request("PUT", url, data=payload)
        return redirect(url_for('product', code=code))
    else:
        return render_template('product_edit.html',
                                products=products,
                                product=product)
