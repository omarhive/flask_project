from flask import Flask, render_template, session, redirect, url_for, request
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'secret123'

# Sample product data
PRODUCTS = [
    {
        'id': 'p1',
        'title': 'Echo Show Dot (5th Gen)',
        'description': 'Smart speaker with Bigger sound, Motion Detection, Temperature Sensor, Alexa and Bluetooth| Black',
        'price': 5100,
        'inventory': 5,
        'image': 'echodot.jpg'
    },
    {
        'id': 'p2',
        'title': 'Echo Show 5',
        'description': 'Smart display with 2x the bass and clearer sound, Charcoal',
        'price': 7000,
        'inventory': 5,
        'image': 'show5.jpg'
    },
    {
        'id': 'p3',
        'title': 'Echo Show 8',
        'description': 'Smart speaker with 8" HD screen, stereo sound & hands-free entertainment with Alexa (Black)',
        'price': 11500,
        'inventory': 2,
        'image': 'show8.jpg'
    },
    {
        'id': 'p4',
        'title': 'Echo Pop',
        'description': 'Smart speaker with Alexa and Bluetooth| Loud sound, balanced bass, crisp vocals| Black',
        'price': 3700,
        'inventory': 5,
        'image': 'echopop.jpg'
    },
    {
        'id': 'p5',
        'title': 'Echo Show 10',
        'description': 'Premium smart speaker with 10.1" HD screen, 13 MP camera, Bluetooth and Alexa (Black)',
        'price': 24500,
        'inventory': 1,
        'image': 'show10.jpg'
    }
]

@app.route('/')
def home():
    return render_template('home.html', products=PRODUCTS)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if not product or quantity < 1:
        return redirect(url_for('home'))

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = {}
    for pid in request.form:
        qty = int(request.form[pid])
        if qty > 0:
            cart[pid] = qty
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        cart = session.get('cart', {})
        order_id = str(uuid4())[:8]
        order = {
            'id': order_id,
            'name': name,
            'address': address,
            'items': cart.copy()
        }
        orders = session.get('orders', [])
        orders.append(order)
        session['orders'] = orders
        session.pop('cart', None)
        return redirect(url_for('orders'))
    return render_template('checkout.html')

@app.route('/orders')
def orders():
    orders = session.get('orders', [])
    detailed_orders = []
    for order in orders:
        items = []
        for pid, qty in order['items'].items():
            product = next((p for p in PRODUCTS if p['id'] == pid), None)
            if product:
                items.append({'product': product, 'quantity': qty})
        detailed_orders.append({
            'id': order['id'],
            'name': order['name'],
            'address': order['address'],
            'items': items
        })
    return render_template('orders.html', orders=detailed_orders)


if __name__=='__main__':
    app.run(debug=True)