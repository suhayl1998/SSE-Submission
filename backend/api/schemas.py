from pydantic import BaseModel
from typing import List, Optional

class ProteinSearchResponse(BaseModel):
    protein_id: str
    protein_name: str
    gene_symbol: str
    description: Optional[str] = None

class DomainMap(BaseModel):
    domain_id: str
    feature_name: str
    start_pos: int
    end_pos: int
    feature_type: Optional[str] = None

class VariantMap(BaseModel):
    variant_id: str
    variant_label: Optional[str] = None
    position: int
    variant_type: str

class PeptideMap(BaseModel):
    peptide_id: str
    peptide_label: str
    start_pos: int
    end_pos: int

class IsoformMap(BaseModel):
    isoform_id: str
    isoform_name: str
    start_pos: int
    end_pos: int
    domains: List[DomainMap]
    variants: List[VariantMap]
    peptides: List[PeptideMap]

class FeatureMap(BaseModel):
    protein_id: str
    isoforms : List[IsoformMap]
    
class SampleDetails(BaseModel):
    sample_id : str
    sample_name : str
    sample_class : str

class ProteinExpressionSample(BaseModel):
    protein_id : str
    sample_detail : SampleDetails
    abundance_score : float
    observed : bool

class ProteinDetails(BaseModel):
    protein_id: str
    protein_name: str
    gene_symbol: str
    description: Optional[str] = None
    subcellular_location: Optional[str] = None

class ProteinInteractionDetails(BaseModel):
    interaction_id: str
    interactor_protein: ProteinDetails
    interaction_label: Optional[str] = None
    confidence_score: Optional[float] = None