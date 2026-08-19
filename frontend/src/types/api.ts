export interface ProteinSearchResponse {
    protein_id: string;
    protein_name: string;
    gene_symbol: string;
    description: string | null;
}

export interface DomainMap {
    domain_id: string;
    feature_name: string;
    start_pos: number;
    end_pos: number;
    feature_type: string | null;
}

export interface VariantMap {
    variant_id: string;
    variant_label: string | null;
    position: number;
    variant_type: string; 
}

export interface PeptideMap {
    peptide_id: string;
    peptide_label: string;
    start_pos: number;
    end_pos: number;
}

export interface IsoformMap {
    isoform_id: string;
    isoform_name: string;
    start_pos: number;
    end_pos: number;
    domains: DomainMap[];
    variants: VariantMap[];
    peptides: PeptideMap[];
}

export interface FeatureMap {
    protein_id: string;
    isoforms: IsoformMap[];
}

export interface SampleDetails {
    sample_id: string,
    sample_name: string,
    sample_class: string
}

export interface ProteinExpressionSample {
    protein_id: string,
    sample_detail: SampleDetails,
    abundance_score: number,
    observed: boolean
}

export interface ProteinDetails {
    protein_id: string;
    protein_name: string;
    gene_symbol: string;
    description: string | null;
    subcellular_location: string | null;
}

export interface ProteinInteractionDetails {
    interaction_id: string;
    interactor_protein: ProteinDetails;
    interaction_label: string | null;
    confidence_score: number | null;
}