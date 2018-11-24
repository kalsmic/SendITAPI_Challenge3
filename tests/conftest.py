import pytest

from app import create_app

from app.models.database import Database
# @pytest.fixture
@pytest.fixture(scope='module')
def test_client():
    """Tells Flask that app is in test mode
    """

    app = create_app('TESTING')
    db = Database()
    db.create_tables()
    db.cursor.execute(open("test_data.sql", "r").read())

    test_client = app.test_client()

    context = app.app_context()
    context.push()

    yield test_client
    # db.empty_tables()



    context.pop()


