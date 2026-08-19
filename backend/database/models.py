from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Protein(Base):
    __tablename__ = "protein"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    gene_symbol = Column(String, nullable=False)
    subcellular_location = Column(String, nullable=True)
    chromosome = Column(String, nullable=True)
    canonical_length = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    __table_args__ = (
        Index("idx_protein_gene_symbol", "gene_symbol"),  # Search by gene symbol
    )
    isoforms = relationship("Isoform", back_populates="protein")
    protein_expressions = relationship("ProteinExpression", back_populates="protein")
    protein_interactions_a = relationship("Interaction", foreign_keys="[Interaction.protein_a_id]", back_populates="protein_a")
    protein_interactions_b = relationship("Interaction", foreign_keys="[Interaction.protein_b_id]", back_populates="protein_b")


class Isoform(Base):
    __tablename__ = "isoform"
    
    id = Column(String, primary_key=True)
    protein_id = Column(String, ForeignKey("protein.id"), nullable=False)
    name = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    accession = Column(String, nullable=False, unique=True)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    
    protein = relationship("Protein", back_populates="isoforms")
    __table_args__ = (
        Index("idx_isoform_protein_id", "protein_id"),  # For JOINs
    )
    domains = relationship("Domain", back_populates="isoform")
    peptides = relationship("Peptide", back_populates="isoform")
    variants = relationship("Variant", back_populates="isoform")
    
class Domain(Base):
    __tablename__ = "domain"
    
    id = Column(String, primary_key=True)
    isoform_id = Column(String, ForeignKey("isoform.id"), nullable=False)
    feature_name = Column(String, nullable=False)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    feature_type = Column(String, nullable=True)
    
    isoform = relationship("Isoform", back_populates="domains")
    __table_args__ = (
        Index("idx_domain_isoform_id", "isoform_id"),  # For JOINs
    )

class Peptide(Base):
    __tablename__ = "peptide"
    
    id = Column(String, primary_key=True)
    isoform_id = Column(String, ForeignKey("isoform.id"), nullable=False)
    label = Column(String, nullable=False)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    specificity = Column(String, nullable=True)
    quality_score = Column(Float, nullable=True)
    
    isoform = relationship("Isoform", back_populates="peptides")
    __table_args__ = (
        Index("idx_peptide_isoform_id", "isoform_id"),  # For JOINs
    )

class Sample(Base):
    __tablename__ = "sample"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    sample_class = Column(String, nullable=True)
    indication = Column(String, nullable=True)
    sample_type = Column(String, nullable=True)
    dataset_name = Column(String, nullable=False)
    
    __table_args__ = (
        Index("idx_sample_name", "name"),  # Search by sample name
        Index("idx_sample_dataset_name", "dataset_name"),  # Search by dataset name
    )
    protein_expressions = relationship("ProteinExpression", back_populates="sample")

class Interaction(Base):
    __tablename__ = "interaction"
    
    id = Column(String, primary_key=True)
    protein_a_id = Column(String, ForeignKey("protein.id"), nullable=False)
    protein_b_id = Column(String, ForeignKey("protein.id"), nullable=False)
    interaction_label = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    protein_a = relationship("Protein", foreign_keys=[protein_a_id], back_populates="protein_interactions_a")
    protein_b = relationship("Protein", foreign_keys=[protein_b_id], back_populates="protein_interactions_b")

    __table_args__ = (
        Index("idx_interaction_protein_a_id", "protein_a_id"),  # For JOINs
        Index("idx_interaction_protein_b_id", "protein_b_id"),  # For JOINs
    )

class ProteinExpression(Base):
    __tablename__ = "protein_expression"
    
    protein_id = Column(String, ForeignKey("protein.id"), primary_key=True, nullable=False)
    sample_id = Column(String, ForeignKey("sample.id"), primary_key=True, nullable=False)
    abundance_score = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=True)
    observed = Column(Boolean, nullable=False, default=False)
    
    
    protein = relationship("Protein", back_populates="protein_expressions")
    sample = relationship("Sample", back_populates="protein_expressions")
    
class Variant(Base):
    __tablename__ = "variant"
    
    id = Column(String, primary_key=True)
    isoform_id = Column(String, ForeignKey("isoform.id"), nullable=False)
    variant_type = Column(String, nullable=False)
    position = Column(Integer, nullable=False)
    label = Column(String, nullable=True)

    isoform = relationship("Isoform", back_populates="variants")
    
    __table_args__ = (
        Index("idx_variant_isoform_id", "isoform_id"),  # For JOINs
    )