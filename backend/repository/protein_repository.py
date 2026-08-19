from repository.repository import Repository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database import models

class ProteinRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search_proteins(self, query: str, limit: int) -> list[models.Protein]:
        stmt = (
            select(models.Protein)
            .where(
                (models.Protein.name.ilike(f"%{query}%"))
                | (models.Protein.gene_symbol.ilike(f"%{query}%"))
                | (models.Protein.id.ilike(f"%{query}%"))
            )
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_protein(self, protein_id: str) -> models.Protein | None:
        stmt = select(models.Protein).where(models.Protein.id == protein_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_isoforms_with_features(self, protein_id: str) -> list[models.Isoform]:
        # selectinload = fetch isoforms, then ONE extra query per relationship,
        stmt = (
            select(models.Isoform)
            .where(models.Isoform.protein_id == protein_id)
            .options(
                selectinload(models.Isoform.domains),
                selectinload(models.Isoform.variants),
                selectinload(models.Isoform.peptides),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_protein_expressions_with_samples(self, protein_id):
        stmt = (
            select(models.ProteinExpression)
            .where(models.ProteinExpression.protein_id == protein_id)
            .options(
                selectinload(models.ProteinExpression.sample)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_protein_interactions(self, protein_id):
        stmt = (
            select(models.Interaction)
            # Fetch interactions where the protein is either protein_a or protein_b
            .where(
                (models.Interaction.protein_a_id == protein_id)
                | (models.Interaction.protein_b_id == protein_id)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())