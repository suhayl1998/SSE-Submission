import pytest
from api.schemas import ProteinExpressionSample, SampleDetails
from tests.fakes import FakeProteinRepository
from services.protein_service import ProteinService
from database import models
from exceptions import AppError

class TestGetProteinExpressions:
    @pytest.fixture
    def protein_repo(self):
        return FakeProteinRepository(
            proteins={
                "Protein1": models.Protein(id="Protein1", name="Protein1Name", gene_symbol="P0111"),
                "Protein2": models.Protein(id="Protein2", name="Protein2Name", gene_symbol="P0222"),
                "Protein3": models.Protein(id="Protein3", name="Protein3Name", gene_symbol="P0333")
            },
            protein_expressions={
                # Protein1 with no Expression data
                "Protein1": [],
                
                # Protein2 with 1 sample of Expression data
                "Protein2": [
                    models.ProteinExpression(protein_id="Protein2",
                                             sample_id="Sample1_1",
                                             abundance_score=25,
                                             observed=1,
                                             sample=models.Sample(id="Sample1_1", name="Normal Sample 1_1", sample_class="Normal"))
                ],
                
                # Protein3 with 2 samples of expression data
                "Protein3": [
                    models.ProteinExpression(protein_id="Protein3",
                                             sample_id="Sample1_1",
                                             abundance_score=10,
                                             observed=1,
                                             sample=models.Sample(id="Sample1_1", name="Normal Sample 1_1", sample_class="Normal")),
                    models.ProteinExpression(protein_id="Protein3",
                                             sample_id="Sample2_1",
                                             abundance_score=0.3,
                                             observed=0,
                                             sample=models.Sample(id="Sample2_1", name="Cancer Sample 2_1", sample_class="Cancer"))
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
            result = await protein_service.get_protein_expressions("Protein999")
        # Assert on exception details
        assert excinfo.value.status_code == 404
        assert excinfo.value.title == "Protein Not Found"
    
    @pytest.mark.asyncio
    async def test_protein_with_no_expression_data(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_expressions("Protein1")
        
        # Assert
        assert result == []
        assert protein_repo.calls == [("get_protein", ("Protein1",), {}), ("get_protein_expressions_with_samples", ("Protein1",), {})]
    
    @pytest.mark.asyncio
    async def test_protein_with_one_expression_result(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_expressions("Protein2")
        
        # Assert
        assert result == [
            ProteinExpressionSample(
                protein_id="Protein2",
                sample_detail=SampleDetails(sample_id="Sample1_1", sample_name="Normal Sample 1_1", sample_class="Normal"),
                abundance_score=25,
                observed=1
            )
        ]
        assert protein_repo.calls == [("get_protein", ("Protein2",), {}), ("get_protein_expressions_with_samples", ("Protein2",), {})]

    
    @pytest.mark.asyncio
    async def test_protein_with_multiple_expression_result(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_protein_expressions("Protein3")
        
        # Assert
        assert result == [
            ProteinExpressionSample(
                protein_id="Protein3",
                sample_detail=SampleDetails(sample_id="Sample1_1", sample_name="Normal Sample 1_1", sample_class="Normal"),
                abundance_score=10,
                observed=1
            ),
            ProteinExpressionSample(
                protein_id="Protein3",
                sample_detail=SampleDetails(sample_id="Sample2_1", sample_name="Cancer Sample 2_1", sample_class="Cancer"),
                abundance_score=0.3,
                observed=0
            )
        ]
        assert protein_repo.calls == [("get_protein", ("Protein3",), {}), ("get_protein_expressions_with_samples", ("Protein3",), {})]