// =======================
// NODES
// =======================

// --- Create Freshwater Fish ---
LOAD CSV WITH HEADERS FROM 'file:///species.csv' AS speciesRow
WITH speciesRow
WHERE speciesRow.Fresh = '1'
MERGE (fwf:FreshwaterFish {species: speciesRow.Species})
  ON CREATE SET 
    fwf.family = speciesRow.Family,
    fwf.genus = speciesRow.Genus,
    fwf.commonName = speciesRow.FBname,
    fwf.famCode = speciesRow.FamCode;

// --- Create Saltwater Fish ---
LOAD CSV WITH HEADERS FROM 'file:///species.csv' AS speciesRow
WITH speciesRow
WHERE speciesRow.Saltwater = '1'
MERGE (swf:SaltwaterFish {species: speciesRow.Species})
  ON CREATE SET 
    swf.family = speciesRow.Family,
    swf.genus = speciesRow.Genus,
    swf.commonName = speciesRow.FBname,
    swf.famCode = speciesRow.FamCode;


// --- Create Family nodes ---
LOAD CSV WITH HEADERS FROM 'file:///families.csv' AS famRow
MERGE (fam:Family {FamCode: famRow.FamCode})
  ON CREATE SET 
    fam.familyName = famRow.FamilyName,
    fam.orderName = famRow.OrderName;  // optional if available

// =======================
// INDEXES & CONSTRAINTS
// =======================

// --- Freshwater Fish ---
CREATE INDEX idx_species_fresh FOR (fwf:FreshwaterFish) ON (fwf.species);
CREATE INDEX idx_commonName_fresh FOR (fwf:FreshwaterFish) ON (fwf.commonName);
CREATE CONSTRAINT unique_species_fresh FOR (fwf:FreshwaterFish) REQUIRE fwf.species IS UNIQUE;

// --- Saltwater Fish ---
CREATE INDEX idx_species_salt FOR (swf:SaltwaterFish) ON (swf.species);
CREATE INDEX idx_commonName_salt FOR (swf:SaltwaterFish) ON (swf.commonName);
CREATE CONSTRAINT unique_species_salt FOR (swf:SaltwaterFish) REQUIRE swf.species IS UNIQUE;

// --- Family ---
CREATE INDEX idx_family_code FOR (fam:Family) ON (fam.FamCode);
CREATE CONSTRAINT unique_family_code FOR (fam:Family) REQUIRE fam.FamCode IS UNIQUE;

CALL db.awaitIndexes();

// =======================
// RELATIONSHIPS
// =======================

// --- Example fish-to-fish relationship ---
MATCH (fwf:FreshwaterFish {species: 'Goldfish'}), 
      (swf:SaltwaterFish {species: 'Clownfish'})
MERGE (fwf)-[:SAME_FAMILY]->(swf);

// --- Fish belongs to Family ---
LOAD CSV WITH HEADERS FROM 'file:///species.csv' AS speciesRow
WITH speciesRow
// Freshwater
WHERE speciesRow.Fresh = '1'
MATCH (fwf:FreshwaterFish {species: speciesRow.Species})
MATCH (fam:Family {FamCode: speciesRow.FamCode})
MERGE (fwf)-[:BELONGS_TO]->(fam);

LOAD CSV WITH HEADERS FROM 'file:///species.csv' AS speciesRow
WITH speciesRow
// Saltwater
WHERE speciesRow.Saltwater = '1'
MATCH (swf:SaltwaterFish {species: speciesRow.Species})
MATCH (fam:Family {FamCode: speciesRow.FamCode})
MERGE (swf)-[:BELONGS_TO]->(fam);
