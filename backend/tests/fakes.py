from repository.repository import Repository
from database import models

class FakeProteinRepository(Repository):
    def __init__(self, proteins = None, isoforms = None, protein_expressions = None, interactions = None):
        self._proteins = proteins or {}
        self._isoforms = isoforms or {}
        self._protein_expressions = protein_expressions or {}
        self._interactions = interactions or {}
        self.calls: list[tuple[str, tuple, dict]] = []  # (method_name, args, kwargs)
    
    async def search_proteins(self, query: str, limit: int) -> list[models.Protein]:
        self.calls.append(("search_proteins", (query, limit), {}))
        return [p for p in self._proteins.values() if query.lower() in p.name.lower()][:limit]
    
    async def get_protein(self, protein_id: str) -> models.Protein:
        self.calls.append(("get_protein", (protein_id,), {}))
        return self._proteins.get(protein_id, None)
    
    async def get_isoforms_with_features(self, protein_id: str) -> list[models.Isoform]:
        self.calls.append(("get_isoforms_with_features", (protein_id,), {}))
        return self._isoforms.get(protein_id,[])
    
    async def get_protein_expressions_with_samples(self, protein_id: str) -> list[models.ProteinExpression]:
        self.calls.append(("get_protein_expressions_with_samples", (protein_id,), {}))
        return self._protein_expressions.get(protein_id, []) 
    
    async def get_protein_interactions(self, protein_id: str) -> list[models.Interaction]:
        self.calls.append(("get_protein_interactions", (protein_id,), {}))
        return self._interactions.get(protein_id, [])