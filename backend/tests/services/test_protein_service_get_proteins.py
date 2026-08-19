import pytest
from api.schemas import ProteinSearchResponse
from tests.fakes import FakeProteinRepository
from services.protein_service import ProteinService
from database import models

class TestSearchProteins:
    @pytest.fixture
    def protein_repo(self):
        return FakeProteinRepository(
            proteins={
                "Protein1": models.Protein(id="Protein1", name="Protein1Name", gene_symbol="P0111"),
                "Protein2": models.Protein(id="Protein2", name="Protein2Name", gene_symbol="P0222", description = "description for Protein 2"),
            }
        )

    @pytest.fixture
    def protein_service(self, protein_repo):
        return ProteinService(protein_repo)
    
    @pytest.mark.asyncio
    async def test_short_query_returns_no_results(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_proteins("P", limit=10)
        
        # Assert
        assert result == []
        assert protein_repo.calls == []
    
    @pytest.mark.asyncio
    async def test_query_matches_no_proteins(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_proteins("QRS", limit=10)
        
        # Assert
        assert result == []
        assert protein_repo.calls == [("search_proteins", ("QRS", 10), {})]
    
    @pytest.mark.asyncio
    async def test_query_matches_one_protein(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_proteins("Protein1", limit=10)
        
        # Assert
        assert result == [
            ProteinSearchResponse(
                protein_id="Protein1",
                protein_name="Protein1Name",
                gene_symbol="P0111",
                description=None,
            )
        ]
        assert protein_repo.calls == [("search_proteins", ("Protein1", 10), {})]
    
    @pytest.mark.asyncio
    async def test_query_matches_multiple_proteins(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_proteins("Prot", limit=10)
        
        # Assert
        assert result == [
            ProteinSearchResponse(
                protein_id="Protein1",
                protein_name="Protein1Name",
                gene_symbol="P0111",
                description=None,
            ),
            ProteinSearchResponse(
                protein_id="Protein2",
                protein_name="Protein2Name",
                gene_symbol="P0222",
                description="description for Protein 2",
            )
        ]
        assert protein_repo.calls == [("search_proteins", ("Prot", 10), {})]