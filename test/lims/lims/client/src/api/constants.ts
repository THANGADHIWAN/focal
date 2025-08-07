// API endpoints
export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/auth/token',
        REGISTER: '/auth/register',
        LOGOUT: '/auth/logout',
        REFRESH_TOKEN: '/auth/refresh-token',
    },
    SAMPLES: {
        BASE: '/samples',
        BY_ID: (id: string) => `/samples/${id}`,
        EXPORT: '/samples/export_csv',
        ALIQUOTS: (sampleId: string) => `/samples/${sampleId}/aliquots`,
        ALIQUOT: (sampleId: string, aliquotId: string) => `/samples/${sampleId}/aliquots/${aliquotId}`,
        ALIQUOT_LOCATION: (sampleId: string, aliquotId: string) => `/samples/${sampleId}/aliquots/${aliquotId}/location`,
        TESTS: (sampleId: string, aliquotId: string) => `/samples/${sampleId}/aliquots/${aliquotId}/tests`,
        TEST: (sampleId: string, aliquotId: string, testId: string) =>
            `/samples/${sampleId}/aliquots/${aliquotId}/tests/${testId}`,
        TIMELINE: (sampleId: string) => `/samples/${sampleId}/timeline`,
        ALIQUOT_TIMELINE: (sampleId: string, aliquotId: string) => `/samples/${sampleId}/timeline/aliquots/${aliquotId}`,
        TEST_TIMELINE: (sampleId: string, testId: string) => `/samples/${sampleId}/timeline/tests/${testId}`,
    },
    STORAGE: {
        BOXES: '/storage/boxes',
        FREEZERS: '/storage/freezers',
        HIERARCHY: '/storage/hierarchy',
        LOCATIONS: '/storage/locations',
        AVAILABLE_SLOTS: '/storage/available_slots',
    },
    TESTS: {
        METHODS: '/tests/methods',
    },
    PRODUCTS: {
        BASE: '/products',
        BY_ID: (id: string) => `/products/${id}`,
        SUMMARIES: '/products/summaries',
        SAMPLES: (productId: string) => `/products/${productId}/samples`,
        TESTS: (productId: string) => `/products/${productId}/tests`,
    },
    METADATA: {
        SAMPLE_TYPES: '/metadata/sample_types',
        SAMPLE_TYPES_ENUM: '/metadata/sample_types_enum',
        SAMPLE_STATUSES: '/metadata/sample_statuses',
        LAB_LOCATIONS: '/metadata/lab_locations',
        USERS: '/metadata/users',
        STORAGE_LOCATIONS: '/metadata/storage_locations',
        EQUIPMENT: '/metadata/equipment',
        EQUIPMENT_TYPES: '/metadata/equipment_types',
        EQUIPMENT_STATUSES: '/metadata/equipment_statuses',
        HEALTH: '/metadata/health',
        ALL: '/metadata/all',
    },
};

// HTTP Status codes
export const HTTP_STATUS = {
    OK: 200,
    CREATED: 201,
    NO_CONTENT: 204,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    CONFLICT: 409,
    INTERNAL_SERVER_ERROR: 500,
};

// Local storage keys
export const STORAGE_KEYS = {
    AUTH_TOKEN: 'authToken',
    USER_INFO: 'userInfo',
    PREFERENCES: 'userPreferences',
};
