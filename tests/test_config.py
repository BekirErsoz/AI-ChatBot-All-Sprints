from api.config import settings
def test_config():
    assert settings.admin_username=="admin"
