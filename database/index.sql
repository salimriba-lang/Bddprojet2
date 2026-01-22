CREATE INDEX idx_exam_date ON examens(date_exam);
CREATE INDEX idx_module_formation ON modules(formation_id);
CREATE INDEX idx_etudiant_formation ON etudiants(formation_id);
CREATE INDEX idx_inscription_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_salle_type ON salles(type);
