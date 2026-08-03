# API Documentation

This project uses FastAPI, which automatically generates interactive Swagger UI documentation. When running the project locally, you can access the full interactive API docs at: `http://localhost:8000/docs`.

### Core Endpoints

#### 1. Upload & Process Resume

- **Endpoint:** `POST /upload-resume/{job_id}`
- **Description:** Accepts a PDF or DOCX file, extracts text, uses AI to parse skills/education, calculates a match score against the job ID, and stores the candidate in the database.
- **Parameters:** `job_id` (integer, path parameter)
- **Body:** `file` (multipart/form-data)
- **Response:** JSON containing `match_score`, `raw_text`, and `email_found`.

#### 2. Fetch Candidates

- **Endpoint:** `GET /candidates/{job_id}`
- **Description:** Retrieves a list of all processed candidates associated with a specific Job ID, sorted by match score.
- **Parameters:** `job_id` (integer, path parameter)
- **Response:** JSON array of candidate objects containing ID, name, email, skills, education, and match score.

#### 3. Send Interview Invite (In progress for now)

- **Endpoint:** `POST /send-invite/{candidate_id}`
- **Description:** Triggers a background task to queue and send an automated interview invitation email to the shortlisted candidate.
- **Parameters:** `candidate_id` (integer, path parameter)
- **Response:** JSON success message confirming the email queue status.
