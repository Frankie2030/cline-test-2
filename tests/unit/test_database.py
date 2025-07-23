from src.database.models import User
from src.utils.password import hash_password
import pytest

class TestDatabaseOperations:
    def test_user_creation(self, test_db):
        """Test creating and retrieving a user"""
        hashed_password = hash_password("testpass")
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hashed_password
        )
        test_db.add(test_user)
        test_db.commit()
        
        # Retrieve user
        db_user = test_db.query(User).filter(User.username == "testuser").first()
        assert db_user is not None
        assert db_user.email == "test@example.com"
        assert db_user.username == "testuser"

    def test_unique_constraints(self, test_db):
        """Test username and email uniqueness constraints"""
        # Create first user
        user1 = User(
            username="user1",
            email="user1@example.com",
            hashed_password=hash_password("pass1")
        )
        test_db.add(user1)
        test_db.commit()

        # Try to create user with same username
        user2 = User(
            username="user1",  # duplicate username
            email="user2@example.com",
            hashed_password=hash_password("pass2")
        )
        test_db.add(user2)
        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()

        # Try to create user with same email
        user3 = User(
            username="user3",
            email="user1@example.com",  # duplicate email
            hashed_password=hash_password("pass3")
        )
        test_db.add(user3)
        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()

    def test_user_update(self, test_db):
        """Test updating user information"""
        user = User(
            username="update_test",
            email="update@example.com",
            hashed_password=hash_password("original")
        )
        test_db.add(user)
        test_db.commit()

        # Update user
        user.email = "updated@example.com"
        test_db.commit()

        # Verify update
        updated_user = test_db.query(User).filter(User.username == "update_test").first()
        assert updated_user.email == "updated@example.com"

    def test_user_deletion(self, test_db):
        """Test deleting a user"""
        user = User(
            username="delete_test",
            email="delete@example.com",
            hashed_password=hash_password("todelete")
        )
        test_db.add(user)
        test_db.commit()

        # Delete user
        test_db.delete(user)
        test_db.commit()

        # Verify deletion
        deleted_user = test_db.query(User).filter(User.username == "delete_test").first()
        assert deleted_user is None

    @pytest.mark.parametrize("username,email", [
        ("", "test@example.com"),  # empty username
        ("testuser", ""),  # empty email
        ("a"*256, "test@example.com"),  # too long username
        ("testuser", "a"*256),  # too long email
    ])
    def test_invalid_inputs(self, test_db, username, email):
        """Test various invalid inputs"""
        user = User(
            username=username,
            email=email,
            hashed_password=hash_password("testpass")
        )
        test_db.add(user)
        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()
