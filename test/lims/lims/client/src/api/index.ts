import SampleService from './services/sampleService';
import AliquotService from './services/aliquotService';
import TestService from './services/testService';
import MetadataService from './services/metadataService';
import TimelineService from './services/timelineService';
import ProductService from './services/productService';

// Export all services
export {
    SampleService,
    AliquotService,
    TestService,
    MetadataService,
    TimelineService,
    ProductService
};

// Export constants and types
export * from './constants';
export * from './types';

// Create a single API object that contains all services
const API = {
    samples: SampleService,
    aliquots: AliquotService,
    tests: TestService,
    metadata: MetadataService,
    timeline: TimelineService,
    products: ProductService,
};

export default API;
