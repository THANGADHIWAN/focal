# Mock Data in Development Mode

This project supports using mock data in development mode for easier frontend development without requiring a running backend API.

## How to Use Mock Data

1. Set the environment variable `VITE_USE_MOCK_API` to `true` in `.env.development`:

```
VITE_USE_MOCK_API=true
```

2. When in development mode (using `npm run dev` or `yarn dev`), the application will automatically use mock data instead of making real API calls.

3. To use the real API, set `VITE_USE_MOCK_API` to `false`.

## Mock Data Structure

Mock data is defined in `src/api/mockData.ts` and includes:

- Sample data
- Aliquots
- Tests
- Metadata (sample types, statuses, users, etc.)

Feel free to modify the mock data to suit your development needs.

## API Services

All API services (`sampleService`, `aliquotService`, `testService`, `metadataService`) have been updated to support both mock and real API modes.

Each service checks the `USE_MOCK_API` flag to determine whether to use mock data or make real API calls.
