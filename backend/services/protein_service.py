from api.schemas import ProteinInteractionDetails, ProteinSearchResponse, FeatureMap, IsoformMap,DomainMap, VariantMap, PeptideMap, SampleDetails, ProteinExpressionSample,  ProteinDetails
from repository.repository import Repository
from exceptions import AppError

class ProteinService:
    def __init__(self, protein_repository: Repository):
        self.repo = protein_repository

    async def get_proteins(self, query, limit):
        # If query is less than 2 characters, return an empty list
        if len(query) < 2:
            return []
        # Fetch proteins matching the query from the repository
        protein_models = await self.repo.search_proteins(query, limit)
        # Convert the list of Protein models to a list of ProteinSearchResponse schemas
        # Limit the number of results to the specified limit
        return [
            ProteinSearchResponse(
                protein_id=protein_model.id,
                protein_name=protein_model.name,
                gene_symbol=protein_model.gene_symbol,
                description=protein_model.description
            )
            for protein_model in protein_models
        ]

    async def get_feature_map(self, protein_id):
        # Check if the protein exists, if not raise an exception
        protein = await self.repo.get_protein(protein_id)
        if protein is None:
            raise AppError(status_code=404, title="Protein Not Found", detail=f"Protein with ID '{protein_id}' not found.")
        
        # Fetch isoforms with their associated features (domains, variants, peptides)
        isoform_models = await self.repo.get_isoforms_with_features(protein_id)
        
        # Consider raising an exception if no isoforms are found for the protein
        if not isoform_models:
            raise AppError(status_code=404, title="Isoforms Not Found", detail=f"No isoforms found for protein with ID '{protein_id}'.")
        
        # Construct the FeatureMap response
        return  FeatureMap(
                protein_id=protein_id,
                isoforms=[
                    IsoformMap(
                        isoform_id=isoform_model.id,
                        isoform_name=isoform_model.name,
                        start_pos=isoform_model.start_position,
                        end_pos=isoform_model.end_position,
                        domains=[
                            DomainMap(
                                domain_id=domain_model.id,
                                feature_name=domain_model.feature_name,
                                start_pos=domain_model.start_position,
                                end_pos=domain_model.end_position,
                                feature_type=domain_model.feature_type
                            )
                            for domain_model in isoform_model.domains
                        ],
                        variants=[
                            VariantMap(
                                variant_id=variant_model.id,
                                variant_label=variant_model.label,
                                position=variant_model.position,
                                variant_type=variant_model.variant_type
                            )
                            for variant_model in isoform_model.variants
                        ],
                        peptides=[
                            PeptideMap(
                                peptide_id=peptide_model.id,
                                peptide_label=peptide_model.label,
                                start_pos=peptide_model.start_position,
                                end_pos=peptide_model.end_position
                            )
                            for peptide_model in isoform_model.peptides
                        ]
                    )
                    for isoform_model in isoform_models
                ]
            )
        
    async def get_protein_expressions(self, protein_id):
        # Check if the protein exists, if not raise an exception
        protein = await self.repo.get_protein(protein_id)
        if protein is None:
            raise AppError(status_code=404, title="Protein Not Found", detail=f"Protein with ID '{protein_id}' not found.")
        
        protein_expression_models = await self.repo.get_protein_expressions_with_samples(protein_id)
        
        return [
            ProteinExpressionSample(
                            protein_id=protein_expression_model.protein_id,
                            sample_detail = SampleDetails(
                                sample_id = protein_expression_model.sample.id,
                                sample_name = protein_expression_model.sample.name,
                                sample_class = protein_expression_model.sample.sample_class
                            ),
                            abundance_score = protein_expression_model.abundance_score,
                            observed = protein_expression_model.observed
                        )
                        for protein_expression_model in protein_expression_models
                        ]
    
    async def get_protein_interactions(self, protein_id):
        # Check if the protein exists, if not raise an exception
        protein = await self.repo.get_protein(protein_id)
        if protein is None:
            raise AppError(status_code=404, title="Protein Not Found", detail=f"Protein with ID '{protein_id}' not found.")
        
        protein_interaction_models = await self.repo.get_protein_interactions(protein_id)
        protein_interaction_details = []
        for model in protein_interaction_models:
            # Figure out which is the interactor protein
            interactor_protein_id = model.protein_a_id if model.protein_a_id != protein_id else model.protein_b_id
            protein_interaction_details.append(
                ProteinInteractionDetails(
                                interaction_id=model.id,
                                interactor_protein=await self.get_protein_details(interactor_protein_id),
                                interaction_label=model.interaction_label,
                                confidence_score=model.confidence_score
                            )
            )
        return protein_interaction_details
    
    async def get_protein_details(self, protein_id):
        protein_model = await self.repo.get_protein(protein_id)
        if protein_model is None:
            raise AppError(status_code=404, title="Protein Not Found", detail=f"Protein with ID '{protein_id}' not found.")
        return ProteinDetails(
            protein_id=protein_model.id,
            protein_name=protein_model.name,
            gene_symbol=protein_model.gene_symbol,
            description=protein_model.description,
            subcellular_location=protein_model.subcellular_location
        )