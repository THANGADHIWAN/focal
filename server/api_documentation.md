# API Documentation

This document provides an overview of the APIs, their functionalities, and the associated files in our system. This documentation is designed to be easily understood by someone with no prior coding knowledge.

## API Overview

Our system provides various APIs (Application Programming Interfaces) that allow different parts of the application to communicate with each other and perform various operations. These APIs are implemented in both Go and Python programming languages.

## Go Implementation

### File: api/api.go

This file contains the main API structure and route registrations for the Go implementation.

Key components:

1. API struct: Represents the main API object that handles various operations.
2. RegisterRoutes function: Sets up different API endpoints (URLs) that the application can respond to.

### File: server/server.go

This file contains the server implementation in Go, which sets up and manages the API services.

Key components:

1. Server struct: Represents the main server object that manages various services.
2. Start function: Initializes and starts the server, including setting up API routes.

## Python Implementation

### File: api/api.py

This file contains the main API structure and route registrations for the Python implementation.

Key components:

1. API class: Represents the main API object that handles various operations.
2. register_routes method: Sets up different API endpoints (URLs) that the application can respond to.

### File: server/server.py

This file contains the server implementation in Python, which sets up and manages the API services.

Key components:

1. Server class: Represents the main server object that manages various services.
2. start method: Initializes and starts the server, including setting up API routes.

## API Functionalities

The APIs provide the following main functionalities:

1. User Management: Handling user registration, login, and authentication.
2. Board Management: Creating, updating, and deleting boards (which are organizational units in the application).
3. Block Management: Managing blocks, which are components within boards.
4. Team Management: Handling team-related operations.
5. File Management: Uploading and managing files within the application.
6. Subscription Management: Handling user subscriptions to various elements in the application.

These functionalities are implemented through various routes (URLs) that the API responds to. When a user or another part of the application needs to perform an operation, it sends a request to the appropriate route, and the API handles that request and returns a response.

### Detailed API Endpoints

Based on the `RegisterRoutes` function in `api/api.go`, the following API endpoints are available:

1. User Routes:
   - Register new users
   - User login
   - Get user information

2. Board Routes:
   - Create new boards
   - Get board information
   - Update board details
   - Delete boards
   - Duplicate boards

3. Block Routes:
   - Create new blocks
   - Get block information
   - Update block details
   - Delete blocks
   - Move blocks

4. Team Routes:
   - Create new teams
   - Get team information
   - Update team details

5. File Routes:
   - Upload files
   - Get file information

6. Subscription Routes:
   - Create subscriptions
   - Get subscription information
   - Delete subscriptions

7. Sharing Routes:
   - Share boards or blocks
   - Get sharing information

8. Category Routes:
   - Create categories
   - Get category information
   - Update category details

9. Card Routes:
   - Create cards
   - Get card information
   - Update card details

10. Search Routes:
    - Search for boards, blocks, or cards

Each of these endpoints corresponds to a specific URL and HTTP method (GET, POST, PUT, DELETE) that clients can use to interact with the API. The exact URLs and required parameters for each endpoint are defined in the server implementation.

The Python implementation in `api/api.py` likely provides similar functionality, although the specific route names and structures may differ slightly due to language and framework differences.

## Client Implementations

The API can be accessed and used by client applications. There are implementations in both Go and Python to help developers interact with the API easily.

### Go Client (File: client/client.go)

The Go client provides methods to interact with the API endpoints. Key features include:

1. Creating a new client with a server URL and session token
2. Methods for various API operations like:
   - Logging in
   - Getting, creating, updating, and deleting boards
   - Managing users
   - Uploading files
   - And more

Example of creating a client and logging in:

```go
client := NewClient("http://server-url", "session-token")
loginResponse, err := client.Login(loginRequest)
```

### Python Client (File: client/client.py)

The Python client also provides methods to interact with the API endpoints. Key features include:

1. Asynchronous client implementation using aiohttp
2. Methods for various API operations like:
   - Logging in
   - Getting and creating boards
   - (Other methods would be implemented similarly to the Go client)

Example of creating a client and logging in:

```python
async with Client("http://server-url", token) as client:


## How APIs Are Used in the Application

1. User Interaction: When a user performs an action in the application (like creating a board), the client application sends a request to the appropriate API endpoint.

2. Data Management: The APIs handle creating, reading, updating, and deleting data in the system's database.

3. Authentication: The login and user management APIs ensure that only authorized users can access certain parts of the application.

4. Real-time Updates: Some APIs might be used in conjunction with WebSocket connections to provide real-time updates to users.

5. File Handling: The file upload APIs allow users to add images or documents to their boards or projects.

6. Search Functionality: The search APIs enable users to find specific boards, blocks, or cards quickly.

## Conclusion

This API system forms the backbone of the application, allowing different components to communicate and perform various operations. While the actual implementation is complex and involves programming knowledge, the basic idea is that these APIs provide a way for the application to handle user requests, manage data, and coordinate different parts of the system.

Users of the application don't need to understand the technical details of how the APIs work. Instead, they interact with a user-friendly interface, and the application uses these APIs behind the scenes to perform the necessary operations and provide a smooth user experience.