import pytest

from app import create_app

from app.models.database import Database

@pytest.fixture
def test_client():
    """Tells Flask that app is in test mode
    """

    app = create_app('TESTING')
    # db_connect  = Database()
    test_client = app.test_client()

    context = app.app_context()
    context.push()


    yield test_client

    context.pop()
    # Database.empty_tables()

