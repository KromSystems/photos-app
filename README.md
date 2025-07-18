## Running the Project with Docker

This project is containerized using Docker and Docker Compose for easy setup and deployment.

### Requirements & Dependencies
- **Python Version:** 3.11 (as specified in the Dockerfile: `python:3.11-slim`)
- **System Dependencies:** The Dockerfile installs build tools and libraries required for dependencies such as Pillow and psycopg2 (`gcc`, `libpq-dev`, `libjpeg-dev`, `zlib1g-dev`).
- **Python Dependencies:** All Python dependencies are managed via `requirements.txt` and installed in a virtual environment inside the container.

### Environment Variables
- The application expects environment variables to be set via a `.env` file (see the commented `env_file: ./.env` line in `docker-compose.yml`).
- **Action Required:**
  - Ensure you have a `.env` file in the project root with the necessary environment variables for your application (refer to your app's documentation or code for required variables).
  - Uncomment the `env_file: ./.env` line in `docker-compose.yml` if you want Docker Compose to loaad these variables automatically.

### Build and Run Instructions
1. **Build and start the application:**
   ```sh
   docker compose up --build
   ```
   This will build the Docker image and start the `python-app` service.

2. **Accessing the Application:**
   - The application will be available on your host at [http://localhost:5000](http://localhost:5000).

### Ports
- **5000:** The application exposes port 5000 (as set in both the Dockerfile and `docker-compose.yml`).

### Special Configuration
- The application runs as a non-root user inside the container for improved security.
- If your application requires additional services (e.g., a database), you can add them to `docker-compose.yml` and set up the `depends_on` and `networks` sections as needed.

---

*Update this section if you add more services or change the exposed ports or environment variable requirements.*
#   p h o t o s - a p p 
 
 
