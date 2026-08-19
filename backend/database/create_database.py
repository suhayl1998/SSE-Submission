import os
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import sqlite
from sqlalchemy.schema import CreateTable
from models import Base, Protein, Isoform, Domain, Peptide, Variant, Sample, ProteinExpression, Interaction
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data")
DB_FILE = os.path.join(SCRIPT_DIR, "proteins.db")

def init_db():
    # Drop the existing database (if exists) and create a new one
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("✓ Existing database removed")
        
    engine = create_engine("sqlite:///" + DB_FILE)
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")
    
    Session = sessionmaker(bind=engine)
    with Session() as session:
        print("Loading data into the database...")
        load_proteins(session)
        load_isoforms(session)
        load_domains(session)
        load_peptides(session)
        load_variants(session)
        load_samples(session)
        load_protein_expressions(session)
        load_interactions(session)
        session.commit()
        print("✓ Data loaded successfully")
        validate_counts(session)
        validate_joins(session)
    

"""Convert each csv file to list of dicts, then build objects"""

def load_proteins(session):
    df = pd.read_csv(f"{DATA_PATH}/proteins.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    proteins = [
        Protein(
            id=row["protein_id"],
            name=row["protein_name"],
            gene_symbol=row["gene_symbol"],
            subcellular_location=row["subcellular_location"],
            chromosome=row["chromosome"],
            canonical_length=row["canonical_length_aa"],
            description=row["description"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(proteins)

def load_isoforms(session):
    df = pd.read_csv(f"{DATA_PATH}/isoforms.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    isoforms = [
        Isoform(
            id=row["isoform_id"],
            protein_id=row["protein_id"],
            name=row["isoform_name"],
            length=row["length_aa"],
            accession=row["accession"],
            start_position=row["start_aa"],
            end_position=row["end_aa"],
            notes=row["notes"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(isoforms)

def load_domains(session):
    df = pd.read_csv(f"{DATA_PATH}/domains.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    domains = [
        Domain(
            id=row["domain_id"],
            isoform_id=row["isoform_id"],
            feature_name=row["feature_name"],
            start_position=row["start_aa"],
            end_position=row["end_aa"],
            feature_type=row["feature_type"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(domains)

def load_peptides(session):
    df = pd.read_csv(f"{DATA_PATH}/peptides.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    peptides = [
        Peptide(
            id=row["peptide_id"],
            isoform_id=row["isoform_id"],
            label=row["peptide_label"],
            start_position=row["start_aa"],
            end_position=row["end_aa"],
            specificity=row["specificity"],
            quality_score=row["quality_score"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(peptides)

def load_variants(session):
    df = pd.read_csv(f"{DATA_PATH}/variants.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    variants = [
        Variant(
            id=row["variant_id"],
            isoform_id=row["isoform_id"],
            variant_type=row["variant_type"],
            position=row["position_aa"],
            label=row["label"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(variants)

def load_samples(session):
    df = pd.read_csv(f"{DATA_PATH}/samples.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    samples = [
        Sample(
            id=row["sample_id"],
            name=row["sample_name"],
            sample_class=row["sample_class"],
            indication=row["indication"],
            sample_type=row["sample_type"],
            dataset_name=row["dataset_name"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(samples)

def load_protein_expressions(session):
    df = pd.read_csv(f"{DATA_PATH}/protein_expression.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    protein_expressions = [
        ProteinExpression(
            protein_id=row["protein_id"],
            sample_id=row["sample_id"],
            abundance_score=row["abundance_score"],
            confidence_score=row["confidence_score"],
            observed=row["observed"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(protein_expressions)

def load_interactions(session):
    df = pd.read_csv(f"{DATA_PATH}/interactions.csv")
    df = df.where(pd.notnull(df), None)  # convert all NaN cells to None
    interactions = [
        Interaction(
            id=row["interaction_id"],
            protein_a_id=row["protein_id_a"],
            protein_b_id=row["protein_id_b"],
            interaction_label=row["interaction_label"],
            confidence_score=row["confidence"]
        )
        for row in df.to_dict('records')
    ]
    session.add_all(interactions)

def validate_counts(session):
    counts = {
        "proteins": session.scalar(select(func.count()).select_from(Protein)),
        "isoforms": session.scalar(select(func.count()).select_from(Isoform)),
        "domains": session.scalar(select(func.count()).select_from(Domain)),
        "peptides": session.scalar(select(func.count()).select_from(Peptide)),
        "variants": session.scalar(select(func.count()).select_from(Variant)),
        "samples": session.scalar(select(func.count()).select_from(Sample)),
        "protein_expressions": session.scalar(select(func.count()).select_from(ProteinExpression)),
        "interactions": session.scalar(select(func.count()).select_from(Interaction)),
    }
    print("\nRow counts:")
    for table, count in counts.items():
        print(f"  {table}: {count}")

def validate_joins(session):
        # feature map path: isoforms → domains/peptides/variants
    isoform = session.query(Isoform).first()
    print(f"Feature map join: isoform '{isoform.id}' → {len(isoform.domains)} domains")
    print(f"Feature map join: isoform '{isoform.id}' → {len(isoform.variants)} variants")
    print(f"Feature map join: isoform '{isoform.id}' → {len(isoform.peptides)} peptides")

    # expression path: protein_expression → samples
    expression = session.query(ProteinExpression).first()
    print(f"Expression join: sample '{expression.sample.name}' (class: {expression.sample.sample_class})")

    # interaction path: interactions → proteins (both sides)
    interaction = session.query(Interaction).first()
    print(f"Interaction join: {interaction.protein_a.name} ↔ {interaction.protein_b.name}")

"""
Generate schema as SQL for documentation - not used to create schema
"""
def export_schema_sql(output_path: str):
    with open(output_path, "w") as f:
        for table in Base.metadata.sorted_tables:
            ddl = str(CreateTable(table).compile(dialect=sqlite.dialect()))
            f.write(ddl.strip() + ";\n\n")
    print(f"✓ Schema exported to {output_path}")

if __name__ == "__main__":
    init_db()
    # export_schema_sql(os.path.join(SCRIPT_DIR, "schema.sql"))  
    