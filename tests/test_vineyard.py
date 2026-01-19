import pytest
from unittest.mock import AsyncMock, Mock
from app.repositories.vineyard_repository import VineyardRepository
from app.services.vineyard_service import VineyardService
from app.schemas.vineyard import VineyardAreaResponse, VineyardVigorResponse, WinePredictionResponse
from app.models.wine_prediction import WinePrediction

class TestVineyardRepository:
    @pytest.mark.asyncio
    async def test_get_vineyard_area_found(self, mocker):
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_result.fetchone.return_value = ("Test Vineyard", 10.5)
        mock_db.execute.return_value = mock_result

        repo = VineyardRepository(mock_db)
        result = await repo.get_vineyard_area("00e885e1-617f-4f97-99a6-ad4e59d30d55")

        assert result == ("Test Vineyard", 10.5)
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_vineyard_area_not_found(self, mocker):
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_result.fetchone.return_value = None
        mock_db.execute.return_value = mock_result

        repo = VineyardRepository(mock_db)
        result = await repo.get_vineyard_area("11111111-2222-3333-4444-555555555555")

        assert result is None

class TestVineyardService:
    @pytest.mark.asyncio
    async def test_get_vineyard_area_success(self, mocker):
        mock_repo = AsyncMock()
        mock_repo.get_vineyard_area.return_value = ("Test Vineyard", 10.5)
        mock_db = AsyncMock()

        service = VineyardService(mock_db)
        service.repository = mock_repo

        result = await service.get_vineyard_area("test-code")

        assert isinstance(result, VineyardAreaResponse)
        assert result.name == "Test Vineyard"
        assert result.hectares == 10.5

    @pytest.mark.asyncio
    async def test_get_vineyard_area_not_found(self, mocker):
        mock_repo = AsyncMock()
        mock_repo.get_vineyard_area.return_value = None
        mock_db = AsyncMock()

        service = VineyardService(mock_db)
        service.repository = mock_repo

        with pytest.raises(Exception):  # HTTPException
            await service.get_vineyard_area("invalid-code")

class TestVineyardRouter:
    @pytest.mark.asyncio
    async def test_get_area_endpoint(self, mocker):
        from fastapi.testclient import TestClient
        from app.main import app

        mock_service = AsyncMock()
        mock_service.get_vineyard_area.return_value = VineyardAreaResponse(name="Test", hectares=10.5)

        # Mock the service in the router
        mocker.patch('app.routers.vineyard.VineyardService', return_value=mock_service)

        client = TestClient(app)
        response = client.get("/vineyards/area?code=test-code")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test"
        assert data["hectares"] == 10.5