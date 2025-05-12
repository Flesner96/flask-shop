def test_home_redirects_if_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302  # redirect to login
    assert '/login' in response.headers['Location']


def test_login_success(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    assert b'Dashboard' in response.data


def test_add_product_page_requires_login(client):
    response = client.get('/add_product')
    assert response.status_code == 302  # should redirect to login
    assert '/login' in response.headers['Location']


def test_404_page(client):
    response = client.get('/nonexistentpage')
    assert response.status_code == 404


def test_add_product(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True

    response = client.post('/add_product', data={
        'name': 'Test Product',
        'description': 'Test Description',
        'price': '9.99',
        'rating': '4.5'
    }, follow_redirects=True)

    assert b'Product added successfully' in response.data