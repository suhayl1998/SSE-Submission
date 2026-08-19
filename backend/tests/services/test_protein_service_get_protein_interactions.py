import pytest
from api.schemas import ProteinInteractionDetails, ProteinDetails
from tests.fakes import FakeProteinRepository
from services.protein_service import ProteinService
from database import models
from exceptions import AppError

class TestGetProteinInteractions:
    def create_protein(self, num: int) -> models.Protein:
        return models.Protein(id=f"Protein{num}", name=f"Protein{num}Name", gene_symbol=f"P0{num}{num}{num}")
    
    @pytest.fixture
    def protein_repo(self):
        return FakeProteinRepository(
            proteins={
                "Protein1": self.create_protein(1),
                "Protein2": self.create_protein(2),
                "Protein3": self.create_protein(3),
                "Protein4": self.create_protein(4),
                "Protein5": self.create_protein(5),
                "Protein6": self.create_protein(6)
            },
            interactions={
                # Protein1 with no Interaction data
                "Protein1": [],
                
                # Protein2 with 1 interaction
                "Protein2": [
                    models.Interaction(id="INT1", protein_a_id = "Protein2", protein_a = self.create_protein(2), protein_b=self.create_protein(4), protein_b_id = "Protein4", confidence_score=0.8)
                ],
                
                # Protein3 with 3 interactions
                "Protein3": [
                    models.Interaction(id="INT2", protein_a_id = "Protein3", protein_a = self.create_protein(3), protein_b=self.create_protein(4), protein_b_id = "Protein4", confidence_score=0.4),
                    models.Interaction(id="INT3", protein_a_id = "Protein5", protein_a = self.create_protein(5), protein_b=self.create_protein(3), protein_b_id = "Protein3", confidence_score=0.3),
                    models.Interaction(id="INT4", protein_a_id = "Protein6", protein_a = self.create_protein(6), protein_b=self.create_protein(3), protein_b_id = "Protein3", confidence_score=0.2)
                ],
            }
        )

    @pytest.fixture
    def protein_service(self, protein_repo):
        return ProteinService(protein_repo)
    
    @pytest.mark.asyncio
    async def test_protein_does_not_exist(self, protein_service):
        # Arrange & Act
        with pytest.raises(AppError) as excinfo:
            result = await protein_service.get_protein_interactions("Protein999")
        # Assert on exception details
        assert excinfo.value.status_code == 404
        assert excinfo.value.title == "Protein Not Found"
    
    @pytest.mark.asyncio
    async def test_protein_with_interactions(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_interactions("Protein1")
        
        # Assert
        assert result == []
        assert protein_repo.calls == [("get_protein", ("Protein1",), {}), ("get_protein_interactions", ("Protein1",), {})]
    
    @pytest.mark.asyncio
    async def test_protein_with_one_interaction(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_interactions("Protein2")
        
        # Assert
        assert result == [
            ProteinInteractionDetails(
                interaction_id="INT1",
                interactor_protein=ProteinDetails(protein_id="Protein4", protein_name="Protein4Name", gene_symbol="P0444"),
                interaction_label=None,
                confidence_score=0.8
            )
        ]
        assert protein_repo.calls == [("get_protein", ("Protein2",), {}), ("get_protein_interactions", ("Protein2",), {}), ("get_protein", ("Protein4",), {})]

    
    @pytest.mark.asyncio
    async def test_protein_with_multiple_expression_result(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_interactions("Protein3")
        
        # Assert
        assert result == [
            ProteinInteractionDetails(
                interaction_id="INT2",
                interactor_protein=ProteinDetails(protein_id="Protein4", protein_name="Protein4Name", gene_symbol="P0444"),
                interaction_label=None,
                confidence_score=0.4
            ),
            ProteinInteractionDetails(
                interaction_id="INT3",
                interactor_protein=ProteinDetails(protein_id="Protein5", protein_name="Protein5Name", gene_symbol="P0555"),
                interaction_label=None,
                confidence_score=0.3
            ),
            ProteinInteractionDetails(
                interaction_id="INT4",
                interactor_protein=ProteinDetails(protein_id="Protein6", protein_name="Protein6Name", gene_symbol="P0666"),
                interaction_label=None,
                confidence_score=0.2
            ),
        ]
        assert protein_repo.calls == [("get_protein", ("Protein3",), {}), ("get_protein_interactions", ("Protein3",), {}),
                                      ("get_protein", ("Protein4",), {}), ("get_protein", ("Protein5",), {}), ("get_protein", ("Protein6",), {})]