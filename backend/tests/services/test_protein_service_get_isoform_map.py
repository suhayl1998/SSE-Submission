import pytest
from api.schemas import DomainMap, VariantMap, PeptideMap, IsoformMap, FeatureMap
from tests.fakes import FakeProteinRepository
from services.protein_service import ProteinService
from database import models
from exceptions import AppError

class TestGetIsoformMap: 
    def create_isoform(self, id: str, protein_id: str, domains: models.Domain, peptides: models.Peptide, variants: models.Variant):
        return models.Isoform(id=id, protein_id=protein_id, name=f"ISOFORM{id}",
                              start_position=1, end_position=999,
                              peptides=peptides, domains=domains,variants=variants)
    
    def create_peptide(self, id: int, start_position: int, end_position: int, isoform_id: str):
        return models.Peptide(id=f"PEP{id}", label=f"PEPTIDE {id}", start_position=start_position, end_position=end_position, isoform_id=isoform_id)
        
    def create_domain(self, id: int, start_position: int, end_position: int, isoform_id: str):
        return models.Domain(id=f"D{id}", feature_name=f"Domain {id}", start_position=start_position, end_position=end_position, feature_type="Domain", isoform_id=isoform_id)
    
    def create_variant(self, id: int, position: int, isoform_id: str):
        return models.Variant(id=f"V{id}", variant_type="Variant", position=position, label=f"Variant 1", isoform_id=isoform_id)
                              
    @pytest.fixture
    def protein_repo(self):
        return FakeProteinRepository(
            proteins={
                "Protein1": models.Protein(id="Protein1", name="Protein1Name", gene_symbol="P0111"),
                "Protein2": models.Protein(id="Protein2", name="Protein2Name", gene_symbol="P0222"),
                "Protein3": models.Protein(id="Protein3", name="Protein3Name", gene_symbol="P0333")
            },
            isoforms={
                # Protein1 with no isoform data
                "Protein1": [],
                
                # Protein2 with isoforms
                "Protein2": [
                    self.create_isoform(id="1", protein_id="Protein2", 
                                        domains=[], 
                                        peptides=[self.create_peptide(1, 2, 10, "1"), self.create_peptide(3, 25, 70,"1")],
                                        variants=[self.create_variant(1, 45, "1")]),
                    self.create_isoform(id="2", protein_id="Protein2", 
                                        domains=[self.create_domain(1, 50, 100, "2"), self.create_domain(2, 150, 200, "2")], 
                                        peptides=[self.create_peptide(4, 2, 10, "2"), self.create_peptide(5, 25, 70, "2")],
                                        variants=[])

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
            result = await protein_service.get_feature_map("Protein999")
        # Assert on exception details
        assert excinfo.value.status_code == 404
        assert excinfo.value.title == "Protein Not Found"
    
    @pytest.mark.asyncio
    async def test_protein_with_no_isoforms(self, protein_service, protein_repo):
        # Arrange & Act
        with pytest.raises(AppError) as excinfo:
            result = await protein_service.get_feature_map("Protein1")
        # Assert on exception details
        assert excinfo.value.status_code == 404
        assert excinfo.value.title == "Isoforms Not Found"
    
    @pytest.mark.asyncio
    async def test_protein_with_isoforms(self, protein_service, protein_repo):
        # Arrange & Act
        result = await protein_service.get_feature_map("Protein2")
        
        # Assert
        assert result == FeatureMap(
                protein_id="Protein2",
                isoforms=[
                    IsoformMap(
                        isoform_id="1",
                        isoform_name="ISOFORM1",
                        start_pos=1,
                        end_pos=999,
                        domains=[],
                        peptides=[
                            PeptideMap(peptide_id="PEP1", peptide_label="PEPTIDE 1", start_pos=2, end_pos=10),
                            PeptideMap(peptide_id="PEP3", peptide_label="PEPTIDE 3", start_pos=25, end_pos=70),
                        ],
                        variants=[
                            VariantMap(variant_id="V1", variant_label="Variant 1", position=45, variant_type="Variant"),
                        ],
                    ),
                    IsoformMap(
                        isoform_id="2",
                        isoform_name="ISOFORM2",
                        start_pos=1,
                        end_pos=999,
                        domains=[
                            DomainMap(domain_id="D1", feature_name="Domain 1", start_pos=50, end_pos=100, feature_type="Domain"),
                            DomainMap(domain_id="D2", feature_name="Domain 2", start_pos=150, end_pos=200, feature_type="Domain"),
                        ],
                        peptides=[
                            PeptideMap(peptide_id="PEP4", peptide_label="PEPTIDE 4", start_pos=2, end_pos=10),
                            PeptideMap(peptide_id="PEP5", peptide_label="PEPTIDE 5", start_pos=25, end_pos=70),
                        ],
                        variants=[],
                    ),
                ],
        )
        assert protein_repo.calls == [("get_protein", ("Protein2",), {}), ("get_isoforms_with_features", ("Protein2",), {})]