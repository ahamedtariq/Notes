SMART NOTES API

PROBLEM UNDERSTANDING & ASSUMPTIONS

1.1 Interpretation of Requirements

    The goal of this assessment is to design and implement a backend REST API using FastAPI and PostgreSQL. The solution must demonstrate proper database usage, integration with an external third-party API, clean API design, validation, error handling, and testing.

    The API must expose four endpoints:

    => Create data

    => Read data

    => Update data

    => Delete data

    At least one endpoint must interact with an external API before returning or persisting data.

1.2 Use Case Chosen

    Use Case: Smart Notes API:

    The system allows users to create, retrieve, update, and delete notes.
    When a note is created, the application fetches a summary from an external public API (DuckDuckGo Instant Answer API) based on the note title. This summary is stored along with the note.

    This use case was selected because it is realistic, simple, and clearly demonstrates third-party API integration.

1.3 Assumptions (Mandatory)

    The following assumptions were made:

    Authentication:
    No user authentication or authorization was implemented, as it was not explicitly required.

    External API Reliability:
    The DuckDuckGo API is assumed to be publicly available but may fail occasionally. The system is designed to handle such failures gracefully.

    Data Format:
    Each note contains a title, content, and a generated summary. The summary is topic-based and derived from the note title.

    Business Logic:
    A note is stored only after successfully generating a summary. If the external API fails, the request returns an error.

    Ambiguity Resolution:
    Since no specific external API was mandated, a free and public API was chosen to avoid paid dependencies.

DESIGN DECISIONS

2.1 Database Schema

    Table Name: notes

    Columns:

    id (Integer, Primary Key)

    title (String)

    content (Text)

    summary (Text)

    A single-table design was chosen to keep the schema simple and focused. Primary key indexing is handled automatically.

2.2 Project Structure

    The project follows a layered architecture to separate concerns:

    API Layer: Handles routing and HTTP logic

    Schema Layer: Handles request and response validation

    Model Layer: Handles database entities

    Service Layer: Handles external API communication

    Test Layer: Handles automated testing

    This structure improves maintainability and testability.

2.3 Validation Logic

    Request payloads are validated using Pydantic schemas.

    Required fields are enforced.

    Only valid data types and structures are accepted.

    Invalid inputs return a 422 Unprocessable Entity response.

2.4 External API Design

    DuckDuckGo Instant Answer API is used for summary generation.

    No authentication is required for the API.

    HTTP timeouts are configured.

    Errors from the external API are caught and converted into meaningful application errors.

SOLUTION APPROACH

    Step-by-step data flow:

    Create Note
    Client sends title and content.
    Backend calls the external API using the title.
    Summary is generated and stored in the database.
    Get Note
    Note ID is validated.
    Data is fetched from the database and returned.
    Update Note
    Existing note is fetched.
    Only provided fields are updated.
    Changes are committed to the database.
    Delete Note
    Note is identified by ID.
    Record is deleted from the database.

ERROR HANDLING STRATEGY

    Database Errors:
    Any database failure results in a 500 Internal Server Error.

    External API Failures:
    If the summary service is unavailable, a 503 Service Unavailable error is returned.

    Validation Errors:
    Automatically handled by FastAPI and Pydantic with a 422 response.

    Exception Handling
    Custom exceptions ensure consistent and readable error responses.

HOW TO RUN THE PROJECT

5.1 Setup Instructions

    Clone the repository

    Create and activate a virtual environment

    Install dependencies using pip (requirements.txt)

    Configure environment variables

    Start the FastAPI server using uvicorn main:app

5.2 Environment Variables

    Example .env file:

    DATABASE_URL=postgresql://postgres:password@localhost:5432/notes_db

5.3 Run the Application

    Command to start the server:

        uvicorn app.main:app --reload

    Swagger documentation will be available at:
        http://127.0.0.1:8000/docs

5.4 Example API Usage

Create Note
POST /notes/create_notes

Get All Notes
GET /notes/get_all_notes

5.5 Running Tests

    Command:
        pytest -v

