CREATE TABLE protein (
	id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	gene_symbol VARCHAR NOT NULL, 
	subcellular_location VARCHAR, 
	chromosome VARCHAR, 
	canonical_length INTEGER NOT NULL, 
	description VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE sample (
	id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	sample_class VARCHAR, 
	indication VARCHAR, 
	sample_type VARCHAR, 
	dataset_name VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE interaction (
	id VARCHAR NOT NULL, 
	protein_a_id VARCHAR NOT NULL, 
	protein_b_id VARCHAR NOT NULL, 
	interaction_label VARCHAR, 
	confidence_score FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(protein_a_id) REFERENCES protein (id), 
	FOREIGN KEY(protein_b_id) REFERENCES protein (id)
);

CREATE TABLE isoform (
	id VARCHAR NOT NULL, 
	protein_id VARCHAR NOT NULL, 
	name VARCHAR NOT NULL, 
	length INTEGER NOT NULL, 
	accession VARCHAR NOT NULL, 
	start_position INTEGER NOT NULL, 
	end_position INTEGER NOT NULL, 
	notes VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(protein_id) REFERENCES protein (id), 
	UNIQUE (accession)
);

CREATE TABLE protein_expression (
	protein_id VARCHAR NOT NULL, 
	sample_id VARCHAR NOT NULL, 
	abundance_score FLOAT NOT NULL, 
	confidence_score FLOAT, 
	observed BOOLEAN NOT NULL, 
	PRIMARY KEY (protein_id, sample_id), 
	FOREIGN KEY(protein_id) REFERENCES protein (id), 
	FOREIGN KEY(sample_id) REFERENCES sample (id)
);

CREATE TABLE domain (
	id VARCHAR NOT NULL, 
	isoform_id VARCHAR NOT NULL, 
	feature_name VARCHAR NOT NULL, 
	start_position INTEGER NOT NULL, 
	end_position INTEGER NOT NULL, 
	feature_type VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(isoform_id) REFERENCES isoform (id)
);

CREATE TABLE peptide (
	id VARCHAR NOT NULL, 
	isoform_id VARCHAR NOT NULL, 
	label VARCHAR NOT NULL, 
	start_position INTEGER NOT NULL, 
	end_position INTEGER NOT NULL, 
	specificity VARCHAR, 
	quality_score FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(isoform_id) REFERENCES isoform (id)
);

CREATE TABLE variant (
	id VARCHAR NOT NULL, 
	isoform_id VARCHAR NOT NULL, 
	variant_type VARCHAR NOT NULL, 
	position INTEGER NOT NULL, 
	label VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(isoform_id) REFERENCES isoform (id)
);

