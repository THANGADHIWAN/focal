-- Comprehensive LIMS Database Schema
-- This script creates all tables and enums for the LIMS system

-- Create database if it doesn't exist
-- Note: This needs to be run as a superuser or database owner
-- CREATE DATABASE lims;

-- Connect to the lims database
-- \c lims;

/* =========  Extensions  ========= */
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

/* =========  ENUM Types  ========= */
-- Priority & status around samples
DO $$ BEGIN
    CREATE TYPE sample_priority AS ENUM ('Low','Medium','High','Urgent');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE sample_status AS ENUM ('Logged_In','In_Progress','Completed','Archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Acceptance & parameters
DO $$ BEGIN
    CREATE TYPE specification_type_enum AS ENUM ('Exact','Range','Less_Than','Greater_Than');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE parameter_type_enum AS ENUM ('Numeric','Text','Boolean','DateTime');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE step_result_enum AS ENUM ('Pass','Fail','NA');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE test_status_enum AS ENUM ('Pending','In_Progress','Completed','Cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE result_status_enum AS ENUM ('Pass','Fail','OOS','Invalid');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Investigations & quality events
DO $$ BEGIN
    CREATE TYPE investigation_phase AS ENUM ('phase1_lab','phase2_qc','phase3_qa');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE deviation_severity AS ENUM ('minor','major','critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE deviation_status AS ENUM ('open','under_investigation','closed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE capa_action_type AS ENUM ('corrective','preventive','both');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE capa_status AS ENUM ('open','in_progress','closed','verified','cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE capa_task_status AS ENUM ('pending','in_progress','completed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

/* =========  Core: Users & Audit  ========= */
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name   VARCHAR(100)       NOT NULL,
    email       VARCHAR(100)       NOT NULL UNIQUE,
    role        VARCHAR(20),
    department  VARCHAR(100),
    is_active   BOOLEAN            NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP          DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_trail (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type    VARCHAR(100)    NOT NULL,
    entity_id      UUID            NOT NULL,
    action         VARCHAR(20)     NOT NULL,
    user_id        UUID            NOT NULL REFERENCES users(id),
    old_value      JSON,
    new_value      JSON,
    justification  TEXT,
    signature      VARCHAR(255),
    performed_at   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    ip_address     VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS electronic_signature (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type    VARCHAR(100)    NOT NULL,
    entity_id      UUID            NOT NULL,
    signed_by      UUID            NOT NULL REFERENCES users(id),
    signature_type VARCHAR(20)     NOT NULL,
    comments       TEXT,
    signed_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

/* =========  Storage hierarchy  ========= */
CREATE TABLE IF NOT EXISTS storage_location (
    id                SERIAL PRIMARY KEY,
    location_name     VARCHAR(100) NOT NULL,
    location_code     VARCHAR(50)  UNIQUE,
    temperature_celsius DECIMAL(5,2),
    humidity_percent  DECIMAL(5,2),
    description       TEXT
);

CREATE TABLE IF NOT EXISTS storage_room (
    id                  SERIAL PRIMARY KEY,
    room_name           VARCHAR(100) NOT NULL UNIQUE,
    floor               INT,
    building            VARCHAR(100),
    access_control      BOOLEAN      NOT NULL DEFAULT FALSE,
    temperature_range   VARCHAR(50),
    humidity_range      VARCHAR(50),
    notes               TEXT,
    storage_location_id INT REFERENCES storage_location(id)
);

CREATE TABLE IF NOT EXISTS freezer (
    id                SERIAL PRIMARY KEY,
    freezer_name      VARCHAR(100) NOT NULL,
    freezer_type      VARCHAR(100),
    storage_room_id   INT REFERENCES storage_room(id),
    temperature_range VARCHAR(50),
    notes             TEXT
);

CREATE TABLE IF NOT EXISTS box (
    id          SERIAL PRIMARY KEY,
    box_code    VARCHAR(50)  NOT NULL UNIQUE,
    box_type    VARCHAR(100),
    rack        VARCHAR(50),
    shelf       VARCHAR(50),
    drawer      VARCHAR(50),
    capacity    INT,
    freezer_id  INT REFERENCES freezer(id),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP
);

/* =========  Samples & Aliquots  ========= */
CREATE TABLE IF NOT EXISTS sample_type (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    matrix_type VARCHAR(100)
);

/* =========  Products  ========= */
CREATE TABLE IF NOT EXISTS product (
    id           SERIAL PRIMARY KEY,
    product_code VARCHAR(50)  NOT NULL UNIQUE,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    status       VARCHAR(20)  NOT NULL DEFAULT 'NOT_STARTED',
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sample (
    id                  SERIAL PRIMARY KEY,
    sample_code         VARCHAR(50)  NOT NULL UNIQUE,
    sample_name         VARCHAR(50),
    sample_type_id      INT          REFERENCES sample_type(id),
    product_id          INT          REFERENCES product(id),
    status              VARCHAR(100) NOT NULL DEFAULT 'Completed',
    box_id              INT          REFERENCES box(id),
    volume_ml           INT,
    received_date       TIMESTAMP,
    due_date            TIMESTAMP,
    priority            sample_priority NOT NULL DEFAULT 'Medium',
    quantity            DECIMAL(10,2),
    is_aliquot          BOOLEAN        NOT NULL DEFAULT FALSE,
    number_of_aliquots  INT            NOT NULL DEFAULT 0,
    created_by          VARCHAR(100),
    created_at          TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP,
    purpose             VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS aliquot (
    id                SERIAL PRIMARY KEY,
    sample_id         INT NOT NULL REFERENCES sample(id) ON DELETE CASCADE,
    aliquot_code      VARCHAR(50) NOT NULL UNIQUE,
    volume_ml         DECIMAL(10,2),
    creation_date     TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    status            sample_status NOT NULL DEFAULT 'Logged_In',
    assigned_to       UUID REFERENCES users(id),
    created_by        VARCHAR(100),
    created_at        TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    purpose           VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS inventory_slot (
    id         SERIAL PRIMARY KEY,
    slot_code  VARCHAR(50)  NOT NULL,
    is_occupied BOOLEAN     NOT NULL DEFAULT FALSE,
    aliquot_id INT,
    box_id     INT          REFERENCES box(id),
    CONSTRAINT fk_invslot_aliquot
        FOREIGN KEY (aliquot_id) REFERENCES aliquot(id) ON DELETE SET NULL,
    CONSTRAINT uq_invslot UNIQUE (box_id, slot_code)
);

CREATE TABLE IF NOT EXISTS chain_of_custody (
    id                     SERIAL PRIMARY KEY,
    aliquot_id             INT NOT NULL REFERENCES aliquot(id) ON DELETE CASCADE,
    transferred_from       VARCHAR(100) NOT NULL,
    transferred_to         VARCHAR(100) NOT NULL,
    transfer_date          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    condition_on_transfer  TEXT,
    remarks                TEXT
);

/* =========  Sample & Storage Logs  ========= */
CREATE TABLE IF NOT EXISTS sample_status_log (
    id          SERIAL PRIMARY KEY,
    sample_id   INT NOT NULL REFERENCES sample(id) ON DELETE CASCADE,
    status      VARCHAR(20) NOT NULL,
    changed_by  VARCHAR(100),
    changed_at  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    remarks     TEXT
);

CREATE TABLE IF NOT EXISTS storage_transaction_log (
    id               SERIAL PRIMARY KEY,
    sample_id        INT NOT NULL REFERENCES sample(id) ON DELETE CASCADE,
    from_location_id INT REFERENCES storage_location(id),
    to_location_id   INT REFERENCES storage_location(id),
    moved_by         VARCHAR(100),
    moved_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason           VARCHAR(255),
    remarks          TEXT
);

/* =========  Material Management  ========= */
CREATE TABLE IF NOT EXISTS material (
    id               SERIAL PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    material_type    VARCHAR(20),
    cas_number       VARCHAR(100),
    manufacturer     VARCHAR(100),
    grade            VARCHAR(100),
    unit_of_measure  VARCHAR(50),
    shelf_life_days  INT,
    is_controlled    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP
);

CREATE TABLE IF NOT EXISTS material_lot (
    id                SERIAL PRIMARY KEY,
    material_id       INT NOT NULL REFERENCES material(id) ON DELETE CASCADE,
    lot_number        VARCHAR(100) NOT NULL,
    received_date     TIMESTAMP,
    expiry_date       TIMESTAMP,
    received_quantity DECIMAL(10,2),
    current_quantity  DECIMAL(10,2),
    storage_location_id INT REFERENCES storage_location(id),
    status            VARCHAR(20) NOT NULL DEFAULT 'Available',
    remarks           TEXT,
    CONSTRAINT uq_materiallot UNIQUE (material_id, lot_number)
);

CREATE TABLE IF NOT EXISTS material_usage_log (
    id                  SERIAL PRIMARY KEY,
    material_lot_id     INT NOT NULL REFERENCES material_lot(id) ON DELETE CASCADE,
    used_by             VARCHAR(100),
    used_on             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_quantity       DECIMAL(10,2),
    purpose             VARCHAR(255),
    associated_sample_id INT REFERENCES sample(id),
    remarks             TEXT
);

CREATE TABLE IF NOT EXISTS material_inventory_adjustment (
    id              SERIAL PRIMARY KEY,
    material_lot_id INT NOT NULL REFERENCES material_lot(id) ON DELETE CASCADE,
    adjusted_by     VARCHAR(100),
    adjusted_on     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    adjustment_type VARCHAR(20),
    quantity        DECIMAL(10,2),
    reason          TEXT,
    remarks         TEXT
);

/* =========  Instruments  ========= */
CREATE TABLE IF NOT EXISTS instrument (
    id                 SERIAL PRIMARY KEY,
    name               VARCHAR(100) NOT NULL,
    instrument_type    VARCHAR(100),
    serial_number      VARCHAR(100) UNIQUE,
    manufacturer       VARCHAR(100),
    model_number       VARCHAR(100),
    purchase_date      TIMESTAMP,
    location_id        INT REFERENCES storage_location(id),
    status             VARCHAR(20) NOT NULL DEFAULT 'Active',
    qualification_status VARCHAR(20),
    maintenance_type   VARCHAR(20),
    remarks            TEXT
);

CREATE TABLE IF NOT EXISTS instrument_calibration (
    id               SERIAL PRIMARY KEY,
    instrument_id    INT NOT NULL REFERENCES instrument(id) ON DELETE CASCADE,
    calibration_date TIMESTAMP,
    calibrated_by    VARCHAR(100),
    due_date         TIMESTAMP,
    calibration_status VARCHAR(20),
    certificate_link VARCHAR(255),
    remarks          TEXT
);

CREATE TABLE IF NOT EXISTS instrument_maintenance_log (
    id               SERIAL PRIMARY KEY,
    instrument_id    INT NOT NULL REFERENCES instrument(id) ON DELETE CASCADE,
    maintenance_date TIMESTAMP,
    performed_by     VARCHAR(100),
    maintenance_type VARCHAR(20),
    description      TEXT,
    next_due_date    TIMESTAMP,
    remarks          TEXT
);

/* =========  Testing & Methods  ========= */
CREATE TABLE IF NOT EXISTS test_method (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    version     VARCHAR(20),
    description TEXT,
    validated   BOOLEAN NOT NULL DEFAULT FALSE,
    created_by  VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_parameter (
    id              SERIAL PRIMARY KEY,
    test_method_id  INT NOT NULL REFERENCES test_method(id) ON DELETE CASCADE,
    parameter_name  VARCHAR(150) NOT NULL,
    parameter_type  parameter_type_enum NOT NULL,
    unit            VARCHAR(50),
    description     TEXT,
    created_by      VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_specification (
    id                   SERIAL PRIMARY KEY,
    test_parameter_id    INT NOT NULL REFERENCES test_parameter(id) ON DELETE CASCADE,
    specification_name   VARCHAR(150) NOT NULL,
    specification_type   specification_type_enum NOT NULL,
    unit                 VARCHAR(50),
    min_value            DECIMAL(10,2),
    max_value            DECIMAL(10,2),
    description          TEXT,
    created_by           VARCHAR(100),
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at           TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_procedure (
    id                     SERIAL PRIMARY KEY,
    test_method_id         INT NOT NULL REFERENCES test_method(id) ON DELETE CASCADE,
    procedure_name         VARCHAR(150) NOT NULL,
    procedure_description  TEXT,
    steps_order            INT NOT NULL DEFAULT 1,
    created_by             VARCHAR(100),
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_step (
    id                 SERIAL PRIMARY KEY,
    test_procedure_id  INT NOT NULL REFERENCES test_procedure(id) ON DELETE CASCADE,
    step_number        INT NOT NULL,
    step_description   TEXT,
    expected_result    TEXT,
    actual_result      TEXT,
    remarks            TEXT,
    created_by         VARCHAR(100),
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_step_execution (
    id             SERIAL PRIMARY KEY,
    test_step_id   INT NOT NULL REFERENCES test_step(id) ON DELETE CASCADE,
    executed_by    VARCHAR(100),
    executed_on    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    result         step_result_enum NOT NULL,
    remarks        TEXT
);

CREATE TABLE IF NOT EXISTS test_master (
    id              SERIAL PRIMARY KEY,
    test_method_id  INT NOT NULL REFERENCES test_method(id) ON DELETE CASCADE,
    test_name       VARCHAR(150) NOT NULL,
    test_code       VARCHAR(50)  NOT NULL UNIQUE,
    description     TEXT,
    frequency       VARCHAR(50),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_by      VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test (
    id              SERIAL PRIMARY KEY,
    sample_id       INT REFERENCES sample(id),
    aliquot_id      INT REFERENCES aliquot(id),
    product_id      INT REFERENCES product(id),
    test_master_id  INT NOT NULL REFERENCES test_master(id),
    analyst_id      UUID REFERENCES users(id),
    instrument_id   INT REFERENCES instrument(id),
    scheduled_date  TIMESTAMP,
    start_date      TIMESTAMP,
    end_date        TIMESTAMP,
    status          test_status_enum NOT NULL DEFAULT 'Pending',
    remarks         TEXT
);

CREATE TABLE IF NOT EXISTS test_result (
    id                  SERIAL PRIMARY KEY,
    test_id             INT NOT NULL REFERENCES test(id) ON DELETE CASCADE,
    test_parameter_id   INT NOT NULL REFERENCES test_parameter(id),
    result_value        VARCHAR(100),
    unit                VARCHAR(50),
    specification_limit VARCHAR(100),
    result_status       result_status_enum NOT NULL,
    result_date         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks             TEXT
);

/* =========  OO S & Quality Events  ========= */
CREATE TABLE IF NOT EXISTS oos (
    id                        SERIAL PRIMARY KEY,
    sample_id                 INT REFERENCES sample(id),
    test_id                   INT REFERENCES test(id),
    instrument_id             INT REFERENCES instrument(id),
    test_method_id            INT REFERENCES test_method(id),
    result_value              FLOAT,
    specification_limit_low   FLOAT,
    specification_limit_high  FLOAT,
    unit                      VARCHAR(50),
    result_status             VARCHAR(50),
    analyst_name              VARCHAR(100),
    test_location             VARCHAR(100),
    oos_detected_at           TIMESTAMP,
    oos_flag_auto             BOOLEAN NOT NULL DEFAULT FALSE,
    oos_flag_manual           BOOLEAN NOT NULL DEFAULT FALSE,
    notification_timestamp    TIMESTAMP,
    oos_reference_number      VARCHAR(100),
    notes                     TEXT,
    created_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at                TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS oos_investigation (
    id                         SERIAL PRIMARY KEY,
    oos_id                     INT NOT NULL REFERENCES oos(id) ON DELETE CASCADE,
    phase                      investigation_phase NOT NULL DEFAULT 'phase1_lab',
    investigation_start        TIMESTAMP,
    investigator_name          VARCHAR(100),
    raw_data_reviewed_at       TIMESTAMP,
    retest_initiated_at        TIMESTAMP,
    retest_result              FLOAT,
    is_retest_passed           BOOLEAN,
    analyst_interview_at       TIMESTAMP,
    root_cause_method          VARCHAR(100),
    root_cause_description     TEXT,
    conclusion                 VARCHAR(255),
    qa_reviewer_name           VARCHAR(100),
    investigation_complete_at  TIMESTAMP,
    documents_uploaded_at      TIMESTAMP,
    capa_required              BOOLEAN NOT NULL DEFAULT FALSE,
    created_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* =========  Deviation & CAPA  ========= */
CREATE TABLE IF NOT EXISTS deviation (
    id                         SERIAL PRIMARY KEY,
    reported_by                UUID REFERENCES users(id),
    reported_at                TIMESTAMP,
    department                 VARCHAR(100),
    deviation_type             VARCHAR(100),
    severity                   deviation_severity NOT NULL,
    deviation_status           deviation_status   NOT NULL DEFAULT 'open',
    gmp_impact                 BOOLEAN,
    process_impacted           VARCHAR(100),
    related_sop_id             INT REFERENCES test_procedure(id),
    description                TEXT,
    root_cause_method          VARCHAR(100),
    root_cause_description     TEXT,
    investigation_comments     TEXT,
    deviation_reference_number VARCHAR(100),
    linked_oos_id              INT REFERENCES oos(id),
    approved_by                UUID REFERENCES users(id),
    approval_timestamp         TIMESTAMP,
    created_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS capa (
    id                       SERIAL PRIMARY KEY,
    initiated_by             UUID REFERENCES users(id),
    initiation_timestamp     TIMESTAMP,
    department               VARCHAR(100),
    root_cause_method        VARCHAR(100),
    root_cause_description   TEXT,
    action_type              capa_action_type NOT NULL DEFAULT 'both',
    corrective_action_plan   TEXT,
    preventive_action_plan   TEXT,
    action_owner             UUID REFERENCES users(id),
    action_due_date          TIMESTAMP,
    task_completed_at        TIMESTAMP,
    voe_performed_by         UUID REFERENCES users(id),
    voe_outcome              TEXT,
    approval_by              UUID REFERENCES users(id),
    approval_timestamp       TIMESTAMP,
    linked_deviation_id      INT REFERENCES deviation(id),
    linked_oos_id            INT REFERENCES oos(id),
    capa_status              capa_status NOT NULL DEFAULT 'open',
    created_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS capa_action (
    id             SERIAL PRIMARY KEY,
    capa_id        INT NOT NULL REFERENCES capa(id) ON DELETE CASCADE,
    task_description TEXT,
    assigned_to    UUID REFERENCES users(id),
    due_date       TIMESTAMP,
    completed_at   TIMESTAMP,
    task_status    capa_task_status NOT NULL DEFAULT 'pending',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* =========  Helpful Indexes  ========= */
CREATE INDEX IF NOT EXISTS idx_sample_type     ON sample(sample_type_id);
CREATE INDEX IF NOT EXISTS idx_sample_box      ON sample(box_id);
CREATE INDEX IF NOT EXISTS idx_aliquot_sample  ON aliquot(sample_id);
CREATE INDEX IF NOT EXISTS idx_test_sample     ON test(sample_id);
CREATE INDEX IF NOT EXISTS idx_test_aliquot    ON test(aliquot_id);
CREATE INDEX IF NOT EXISTS idx_result_test     ON test_result(test_id);
CREATE INDEX IF NOT EXISTS idx_result_parameter ON test_result(test_parameter_id);
CREATE INDEX IF NOT EXISTS idx_test_method    ON test_method(name);
CREATE INDEX IF NOT EXISTS idx_test_parameter ON test_parameter(test_method_id);
CREATE INDEX IF NOT EXISTS idx_test_specification ON test_specification(test_parameter_id);
CREATE INDEX IF NOT EXISTS idx_test_procedure ON test_procedure(test_method_id);
CREATE INDEX IF NOT EXISTS idx_test_step     ON test_step(test_procedure_id);
CREATE INDEX IF NOT EXISTS idx_test_step_execution ON test_step_execution(test_step_id);
CREATE INDEX IF NOT EXISTS idx_instrument     ON instrument(name);
CREATE INDEX IF NOT EXISTS idx_instrument_calibration ON instrument_calibration(instrument_id);
CREATE INDEX IF NOT EXISTS idx_instrument_maintenance ON instrument_maintenance_log(instrument_id);
CREATE INDEX IF NOT EXISTS idx_material      ON material(name);
CREATE INDEX IF NOT EXISTS idx_material_lot ON material_lot(material_id);
CREATE INDEX IF NOT EXISTS idx_material_usage ON material_usage_log(material_lot_id);
CREATE INDEX IF NOT EXISTS idx_material_inventory ON material_inventory_adjustment(material_lot_id);
CREATE INDEX IF NOT EXISTS idx_storage_location ON storage_location(location_name);
CREATE INDEX IF NOT EXISTS idx_storage_room ON storage_room(room_name);
CREATE INDEX IF NOT EXISTS idx_freezer      ON freezer(freezer_name);
CREATE INDEX IF NOT EXISTS idx_box          ON box(box_code);
CREATE INDEX IF NOT EXISTS idx_inventory_slot ON inventory_slot(slot_code);
CREATE INDEX IF NOT EXISTS idx_chain_of_custody ON chain_of_custody(aliquot_id);
CREATE INDEX IF NOT EXISTS idx_sample_status_log ON sample_status_log(sample_id);
CREATE INDEX IF NOT EXISTS idx_storage_transaction_log ON storage_transaction_log(sample_id);
CREATE INDEX IF NOT EXISTS idx_oos          ON oos(sample_id);
CREATE INDEX IF NOT EXISTS idx_oos_investigation ON oos_investigation(oos_id);
CREATE INDEX IF NOT EXISTS idx_deviation    ON deviation(deviation_reference_number);
CREATE INDEX IF NOT EXISTS idx_capa_action ON capa_action(capa_id);
CREATE INDEX IF NOT EXISTS idx_audit_trail ON audit_trail(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_electronic_signature ON electronic_signature(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_users        ON users(email);
CREATE INDEX IF NOT EXISTS idx_test_master ON test_master(test_method_id);
CREATE INDEX IF NOT EXISTS idx_test_master_code ON test_master(test_code);
CREATE INDEX IF NOT EXISTS idx_test_result ON test_result(test_id);
CREATE INDEX IF NOT EXISTS idx_test_result_parameter ON test_result(test_parameter_id);
CREATE INDEX IF NOT EXISTS idx_test_result_status ON test_result(result_status);
CREATE INDEX IF NOT EXISTS idx_test_status ON test(status);

-- Add some sample data
INSERT INTO users (full_name, email, role, department) VALUES 
('John Doe', 'john.doe@company.com', 'Analyst', 'QC'),
('Jane Smith', 'jane.smith@company.com', 'Supervisor', 'QA'),
('Bob Wilson', 'bob.wilson@company.com', 'Manager', 'Operations')
ON CONFLICT (email) DO NOTHING;

INSERT INTO sample_type (name, description, matrix_type) VALUES 
('Blood', 'Human blood samples', 'Biological'),
('Urine', 'Human urine samples', 'Biological'),
('Tissue', 'Human tissue samples', 'Biological'),
('Environmental', 'Environmental samples', 'Environmental')
ON CONFLICT (name) DO NOTHING;

-- Create a storage location
INSERT INTO storage_location (location_name, location_code, description) VALUES 
('Main Lab', 'ML001', 'Main laboratory storage area')
ON CONFLICT (location_code) DO NOTHING;

-- Create a storage room
INSERT INTO storage_room (room_name, floor, building, access_control) VALUES 
('Storage Room 1', 1, 'Building A', true)
ON CONFLICT (room_name) DO NOTHING;

-- Create a freezer
INSERT INTO freezer (freezer_name, freezer_type, storage_room_id) VALUES 
('Freezer 1', 'Ultra-low temperature', 1)
ON CONFLICT DO NOTHING;

-- Create a box
INSERT INTO box (box_code, box_type, capacity, freezer_id) VALUES 
('BOX001', 'Standard', 100, 1)
ON CONFLICT (box_code) DO NOTHING;

COMMIT; 