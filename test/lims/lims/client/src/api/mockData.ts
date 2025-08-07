// Mock data for development mode
import { Sample, Aliquot, Test, SampleType, SampleStatus, TestMethod, TestStatus, LabLocation, User, StorageLocation } from './types';

// Define test data first
const test001: Test = {
    id: 'test-001',
    sample_id: 'sample-001',
    aliquot_id: 'aliquot-001',
    test_master_id: 'tm-001',
    test_name: 'CBC',
    status: 'Completed',
    analyst_id: 'analyst-001',
    instrument_id: 'inst-001',
    scheduled_date: new Date(2025, 5, 17).toISOString(),
    start_date: new Date(2025, 5, 17).toISOString(),
    end_date: new Date(2025, 5, 18).toISOString(),
    remarks: 'No abnormalities detected',
    test_results: []
};

// Define aliquots with tests
const aliquot001: Aliquot = {
    id: 'aliquot-001',
    sample_id: 'sample-001',
    aliquot_code: 'ALQ-001',
    volume: 5,
    volume_ml: 5,
    location: 'Freezer 1, Rack 3',
    creation_date: new Date(2025, 5, 16).toISOString(),
    status: 'active',
    assigned_to: 'tech-001',
    created_by: 'user-001',
    created_at: new Date(2025, 5, 16).toISOString(),
    purpose: 'Testing',
    tests: [test001]
};

const aliquot002: Aliquot = {
    id: 'aliquot-002',
    sample_id: 'sample-001',
    aliquot_code: 'ALQ-002',
    volume: 5,
    volume_ml: 5,
    location: 'Freezer 1, Rack 4',
    creation_date: new Date(2025, 5, 16).toISOString(),
    status: 'active',
    assigned_to: 'tech-002',
    created_by: 'user-001',
    created_at: new Date(2025, 5, 16).toISOString(),
    purpose: 'Backup',
    tests: []
};

const aliquot003: Aliquot = {
    id: 'aliquot-003',
    sample_id: 'sample-002',
    aliquot_code: 'ALQ-003',
    volume: 3,
    volume_ml: 3,
    location: 'Freezer 2, Rack 1',
    creation_date: new Date(2025, 5, 21).toISOString(),
    status: 'active',
    assigned_to: 'tech-003',
    created_by: 'user-002',
    created_at: new Date(2025, 5, 21).toISOString(),
    purpose: 'Analysis',
    tests: []
};

// Define samples with their aliquots
export const mockSamples: Sample[] = [
    {
        id: 'sample-001',
        sample_code: 'SMP-001',
        sample_name: 'Blood Sample A',
        type: 'blood',
        type_name: 'Blood',
        type_id: 1,
        status: 'submitted',
        owner: 'John Doe',
        box_id: 'box-001',
        location: 'Lab 1',
        volume_ml: 15,
        volume_left: 10,
        received_date: new Date(2025, 5, 15).toISOString(),
        due_date: new Date(2025, 6, 15).toISOString(),
        quantity: 1,
        created_by: 'user-001',
        created_at: new Date(2025, 5, 15).toISOString(),
        updated_at: new Date(2025, 5, 15).toISOString(),
        purpose: 'Clinical testing',
        notes: 'Blood sample for CBC analysis',
        aliquots: [aliquot001, aliquot002]
    },
    {
        id: 'sample-002',
        sample_code: 'SMP-002',
        sample_name: 'Tissue Sample B',
        type: 'tissue',
        type_name: 'Tissue',
        type_id: 2,
        status: 'aliquots_created',
        owner: 'Jane Smith',
        box_id: 'box-002',
        location: 'Lab 2',
        volume_ml: 8,
        volume_left: 5,
        received_date: new Date(2025, 5, 20).toISOString(),
        due_date: new Date(2025, 6, 20).toISOString(),
        quantity: 1,
        created_by: 'user-002',
        created_at: new Date(2025, 5, 20).toISOString(),
        updated_at: new Date(2025, 5, 21).toISOString(),
        purpose: 'Research analysis',
        notes: 'Tissue sample for histological examination',
        aliquots: [aliquot003]
    }
];

// Keep aliquots by sample ID for easy lookup
export const mockAliquots: Record<string, Aliquot[]> = {
    'sample-001': [aliquot001, aliquot002],
    'sample-002': [aliquot003]
};

// Keep tests by sample ID and aliquot ID for easy lookup
export const mockTests: Record<string, Record<string, Test[]>> = {
    'sample-001': {
        'aliquot-001': [test001]
    }
};

export const mockSampleTypes: SampleType[] = [
    { id: 1, value: 'blood', label: 'Blood', description: 'Blood sample' },
    { id: 2, value: 'tissue', label: 'Tissue', description: 'Tissue sample' },
    { id: 3, value: 'urine', label: 'Urine', description: 'Urine sample' },
    { id: 4, value: 'saliva', label: 'Saliva', description: 'Saliva sample' },
    { id: 5, value: 'plasma', label: 'Plasma', description: 'Plasma samples' },
    { id: 6, value: 'serum', label: 'Serum', description: 'Serum samples' },
    { id: 7, value: 'dna', label: 'DNA', description: 'DNA samples' },
    { id: 8, value: 'rna', label: 'RNA', description: 'RNA samples' },
    // Pharma-lab specific sample types
    { id: 9, value: 'api', label: 'API', description: 'Active Pharmaceutical Ingredient' },
    { id: 10, value: 'excipient', label: 'Excipient', description: 'Inactive substance in pharmaceutical formulation' },
    { id: 11, value: 'tablet', label: 'Tablet', description: 'Solid dosage form' },
    { id: 12, value: 'capsule', label: 'Capsule', description: 'Gelatin-based dosage form' },
    { id: 13, value: 'solution', label: 'Solution', description: 'Liquid pharmaceutical preparation' },
    { id: 14, value: 'suspension', label: 'Suspension', description: 'Pharmaceutical preparation with insoluble particles' },
    { id: 15, value: 'ointment', label: 'Ointment', description: 'Semi-solid preparation for external use' }
];

export const mockSampleStatuses: SampleStatus[] = [
    { id: 1, value: 'submitted', label: 'submitted', description: 'Sample has been submitted' },
    { id: 2, value: 'aliquots_created', label: 'aliquots_created', description: 'Aliquots have been created' },
    { id: 3, value: 'aliquots_plated', label: 'aliquots_plated', description: 'Aliquots have been plated' },
    { id: 4, value: 'testing_completed', label: 'testing_completed', description: 'Testing has been completed' },
    { id: 5, value: 'in_storage', label: 'in_storage', description: 'Sample is in storage' }
];

export const mockLabLocations: LabLocation[] = [
    { id: 1, value: 'loc-001', label: 'Lab 1', description: 'Main Laboratory' },
    { id: 2, value: 'loc-002', label: 'Lab 2', description: 'Secondary Laboratory' },
    { id: 3, value: 'loc-003', label: 'Lab 3', description: 'Research Laboratory' }
];

export const mockUsers: User[] = [
    { id: 1, value: 'user-001', label: 'John Doe', email: 'john@example.com' },
    { id: 2, value: 'user-002', label: 'Jane Smith', email: 'jane@example.com' },
    { id: 3, value: 'user-003', label: 'Bob Johnson', email: 'bob@example.com' }
];

export const mockStorageLocations: StorageLocation[] = [
    {
        id: 1,
        name: 'Freezer 1',
        capacity: 100,
        availableSpaces: 75,
        drawer: 'D1',
        rack: 'R1',
        shelf: 'S1',
        freezer: 'F1',
        lab: 'Lab 1'
    },
    {
        id: 2,
        name: 'Freezer 2',
        capacity: 80,
        availableSpaces: 60,
        drawer: 'D2',
        rack: 'R2',
        shelf: 'S2',
        freezer: 'F2',
        lab: 'Lab 2'
    }
];

export const mockTestMethods: TestMethod[] = [
    { id: 1, value: 'automated', label: 'Automated Analysis', description: 'Automated testing method' },
    { id: 2, value: 'manual', label: 'Manual Testing', description: 'Manual testing procedure' },
    { id: 3, value: 'spectroscopy', label: 'Spectroscopy', description: 'Spectroscopic analysis' },
    { id: 4, value: 'chromatography', label: 'Chromatography', description: 'Chromatographic analysis' }
];

export const mockTestStatuses: TestStatus[] = [
    { id: 1, value: 'pending', label: 'Pending', description: 'Test is pending' },
    { id: 2, value: 'in_progress', label: 'In Progress', description: 'Test is in progress' },
    { id: 3, value: 'completed', label: 'Completed', description: 'Test has been completed' },
    { id: 4, value: 'failed', label: 'Failed', description: 'Test has failed' },
    { id: 5, value: 'cancelled', label: 'Cancelled', description: 'Test has been cancelled' }
];
