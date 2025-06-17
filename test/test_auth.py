from fastapi.testclient import TestClient
from app.main import app
from test.test_database import override_get_db , override_get_current_user ,TestingSessionLocal
from app.services.user import get_db
from app.core.security import get_current_user ,hash_password
import pytest
from app.schemas.user import User


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_fake_user():
    db = TestingSessionLocal()
    user = User(
        id="1",
        name="karim",
        role="admin",
        email="karimgmarad252@gmail.com",
        password=hash_password("123")  
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()

def test_login_user(test_fake_user):
    
    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "karimgmarad252@gmail.com",
            "password": "123"
        }
    )
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert "access_token" in data
    
    
    
def test_create_user () :
    response = client.post(
        "/api/v1/users/user",
        json={
            "id" : "1",
            "name" : "karim",
            "role": "admin",
            "email" : "karimAZ@gmail.com",
            "password" :hash_password("886")
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data
    
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "karimAZ@gmail.com").first()
    
    if user :
        db.delete(user)
        db.commit()    
    
def test_update_user (test_fake_user):
    response = client.put(
        "/api/v1/users/user/1",
        json={
            "name" : "ali",
            "email" : "ali@gmail.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    
    
def test_delete_user (test_fake_user) :
    response = client.delete(
        "/api/v1/users/user/1",
    )
    
    assert response.status_code == 200
    
    

print("man we ned to try hard to ac")