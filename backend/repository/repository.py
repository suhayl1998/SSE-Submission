from abc import ABC, abstractmethod
from database import models

class Repository(ABC):
    @abstractmethod
    async def search_proteins(self, query: str, limit: int) -> list[models.Protein]: ...
    
    @abstractmethod
    async def get_protein(self, protein_id: str) -> models.Protein | None: ...

    @abstractmethod
    async def get_isoforms_with_features(self, protein_id: str) -> list[models.Isoform]: ...
    
    @abstractmethod
    async def get_protein_expressions_with_samples(self, protein_id) -> list[models.ProteinExpression]: ...
    
    @abstractmethod
    async def get_protein_interactions(self, protein_id) -> list[models.Interaction]: ...