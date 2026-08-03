# Database Schema

This project utilizes SQLite (or PostgreSQL in production) managed via SQLAlchemy.

### Table: `candidates`

Stores all extracted applicant data and calculated metrics.

| Column Name      | Data Type | Constraints                 | Description                                        |
| ---------------- | --------- | --------------------------- | -------------------------------------------------- |
| `id`             | Integer   | Primary Key, Auto-increment | Unique identifier for the candidate record         |
| `job_id`         | Integer   | Indexed                     | The specific job posting the resume is tied to     |
| `name`           | String    | Not Null                    | Candidate's full name or filename                  |
| `email`          | String    | Nullable                    | Extracted email address for outreach               |
| `education`      | String    | Nullable                    | Parsed educational background (Degrees, etc.)      |
| `experience`     | String    | Nullable                    | Parsed work experience details                     |
| `skills`         | String    | Nullable                    | Comma-separated list of extracted technical skills |
| `certifications` | String    | Nullable                    | Any identified certifications                      |
| `match_score`    | Integer   | Default: 0                  | AI-calculated percentage match to job criteria     |
