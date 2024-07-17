from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from database import db
from main import app


class TestLifespan:
    def test_db_connection(self):
        # Mock db.connect and db.disconnect methods
        with (patch.object(db, 'connect', new_callable=AsyncMock) as mock_connect,
              patch.object(db, 'disconnect', new_callable=AsyncMock) as mock_disconnect):
            with TestClient(app=app, base_url="http://test") as client:
                assert client.get("/docs").status_code == 200  # Confirm the application is running

            mock_connect.assert_called_once()
            mock_disconnect.assert_called_once()
