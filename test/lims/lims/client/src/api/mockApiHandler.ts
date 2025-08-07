import { AxiosRequestConfig } from 'axios';
import * as mockData from './mockData';
import { v4 as uuidv4 } from 'uuid';

// Helper to extract ID from URL path like /api/samples/123 would return 123
const extractIdFromUrl = (url: string): string => {
    const parts = url.split('/');
    return parts[parts.length - 1];
};

// Helper to determine entity type from URL
const getEntityTypeFromUrl = (url: string): string => {
    const path = url.toLowerCase();
    if (path.includes('sample')) return 'samples';
    if (path.includes('aliquot')) return 'aliquots';
    if (path.includes('test')) return 'tests';
    if (path.includes('metadata')) return 'metadata';
    return '';
};

// Main mock API handler
const mockApiHandler = async (config: AxiosRequestConfig): Promise<any> => {
    const { method, url } = config;

    console.log(`[Mock API] ${method} ${url}`, config);

    if (!url) return null;

    const entityType = getEntityTypeFromUrl(url);
    const id = url.includes('/') ? extractIdFromUrl(url) : '';

    console.log(`[Mock API] Entity: ${entityType}, ID: ${id}`);

    // GET requests
    if (method?.toLowerCase() === 'get') {
        // Handle specific entity retrieval
        if (id && id !== 'metadata') {
            switch (entityType) {
                case 'samples':
                    const sample = mockData.mockSamples.find(sample => sample.id === id);
                    return sample ? { data: sample, status: 200, success: true } : null;
                case 'aliquots':
                    // Iterate through samples to find aliquot
                    for (const sample of mockData.mockSamples) {
                        const aliquot = sample.aliquots.find(a => a.id === id);
                        if (aliquot) return { data: aliquot, status: 200, success: true };
                    }
                    return null;
                case 'tests':
                    // Iterate through samples and aliquots to find test
                    for (const sample of mockData.mockSamples) {
                        for (const aliquot of sample.aliquots) {
                            const test = aliquot.tests.find(t => t.id === id);
                            if (test) return { data: test, status: 200, success: true };
                        }
                    }
                    return null;
            }
        }

        // Handle list retrievals
        switch (entityType) {
            case 'samples':
                return {
                    data: {
                        data: mockData.mockSamples,
                        totalCount: mockData.mockSamples.length,
                        totalPages: 1,
                        currentPage: 1,
                        pageSize: mockData.mockSamples.length,
                        hasMore: false
                    },
                    status: 200,
                    success: true
                };
            case 'metadata':
                // Return all metadata
                return {
                    data: {
                        sampleTypes: mockData.mockSampleTypes,
                        sampleStatuses: mockData.mockSampleStatuses,
                        labLocations: mockData.mockLabLocations,
                        users: mockData.mockUsers,
                        storageLocations: mockData.mockStorageLocations
                    },
                    status: 200,
                    success: true
                };
        }
    }

    // POST requests (create)
    if (method?.toLowerCase() === 'post') {
        const requestData = config.data ? JSON.parse(config.data) : {};

        switch (entityType) {
            case 'samples':
                const newSample = {
                    id: `sample-${uuidv4().substring(0, 8)}`,
                    submissionDate: new Date().toISOString(),
                    status: 'submitted',
                    lastMovement: new Date().toISOString(),
                    volumeLeft: requestData.totalVolume || 0,
                    aliquotsCreated: 0,
                    aliquots: [],
                    ...requestData
                };
                mockData.mockSamples.push(newSample as any);
                return newSample;

            case 'aliquots':
                const sampleForAliquot = mockData.mockSamples.find(s => s.id === requestData.sampleId);
                if (!sampleForAliquot) return null;

                const newAliquot = {
                    id: `aliquot-${uuidv4().substring(0, 8)}`,
                    createdAt: new Date().toISOString(),
                    tests: [],
                    ...requestData
                };

                sampleForAliquot.aliquots.push(newAliquot as any);
                sampleForAliquot.aliquotsCreated += 1;
                sampleForAliquot.volumeLeft -= newAliquot.volume;

                return newAliquot;

            case 'tests':
                // Find the sample and aliquot to add a test
                for (const sample of mockData.mockSamples) {
                    const aliquot = sample.aliquots.find(a => a.id === requestData.aliquotId);
                    if (aliquot) {
                        const newTest = {
                            id: `test-${uuidv4().substring(0, 8)}`,
                            status: 'Pending',
                            startDate: new Date().toISOString(),
                            ...requestData
                        };
                        aliquot.tests.push(newTest as any);
                        return newTest;
                    }
                }
        }
    }

    // PUT/PATCH requests (update)
    if (method?.toLowerCase() === 'put' || method?.toLowerCase() === 'patch') {
        const requestData = config.data ? JSON.parse(config.data) : {};

        if (id) {
            switch (entityType) {
                case 'samples':
                    const sampleToUpdate = mockData.mockSamples.find(s => s.id === id);
                    if (sampleToUpdate) {
                        Object.assign(sampleToUpdate, requestData);
                        return sampleToUpdate;
                    }
                    break;

                case 'tests':
                    // Find and update test
                    for (const sample of mockData.mockSamples) {
                        for (const aliquot of sample.aliquots) {
                            const testIndex = aliquot.tests.findIndex(t => t.id === id);
                            if (testIndex >= 0) {
                                aliquot.tests[testIndex] = {
                                    ...aliquot.tests[testIndex],
                                    ...requestData
                                };
                                return aliquot.tests[testIndex];
                            }
                        }
                    }
                    break;
            }
        }
    }

    // DELETE requests
    if (method?.toLowerCase() === 'delete' && id) {
        switch (entityType) {
            case 'samples':
                const sampleIndex = mockData.mockSamples.findIndex(s => s.id === id);
                if (sampleIndex >= 0) {
                    const [deletedSample] = mockData.mockSamples.splice(sampleIndex, 1);
                    return deletedSample;
                }
                break;
        }
    }

    // If no specific handler matched
    return null;
};

export default mockApiHandler;
