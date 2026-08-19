import pytest
from api.schemas import ProteinDetails
from tests.fakes import FakeProteinRepository
from services.protein_service import ProteinService
from exceptions import AppError
from database import models

class TestGetProteinDetails:
    @pytest.fixture
    def protein_repo(self):
        return FakeProteinRepository(
            proteins={
                "Protein1": models.Protein(id="Protein1", name="Protein1Name", gene_symbol="P0111", subcellular_location = "cytoplasm"),
            }
        )

    @pytest.fixture
    def protein_service(self, protein_repo):
        return ProteinService(protein_repo)
    
    @pytest.mark.asyncio
    async def test_protein_does_not_exist(self, protein_service):
        # Arrange & Act
        with pytest.raises(AppError) as excinfo:
            result = await protein_service.get_protein_details("Protein999")
        # Assert on exception details
        assert excinfo.value.status_code == 404
        assert excinfo.value.title == "Protein Not Found"
    
    @pytest.mark.asyncio
    async def test_return_protein_details(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_details("Protein1")
        
        # Assert
        assert result == ProteinDetails(
            protein_id="Protein1",
            protein_name="Protein1Name",
            gene_symbol="P0111",
            description=None,
            subcellular_location = "cytoplasm")
        
        assert protein_repo.calls == [("get_protein", ("Protein1",), {})]
    
