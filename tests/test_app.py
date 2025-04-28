import pytest
from app import app, db, movie

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

# Test homepage loads successfully
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"My Top 10 Movies" in response.data  # Adjust according to your HTML text

def test_add_page_loads(client):
    response = client.get('/add')
    assert response.status_code == 200
    assert b"Enter Movie Name" in response.data  # This is the label on your AddMovieForm

# Test submitting the Add Movie Form
def test_add_movie_form_submission(client):
    # First simulate POST request with a form submission
    response = client.post('/add', data={'name': 'Inception'}, follow_redirects=True)
    
    # Now check if the response contains list of movies (search results)
    assert response.status_code == 200
    assert b"Inception" in response.data or b"Search Results" in response.data