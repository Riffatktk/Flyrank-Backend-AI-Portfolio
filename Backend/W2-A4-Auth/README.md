# FlyRank A4 — Supabase Authentication API

A secure FastAPI authentication API built for the **FlyRank Backend Internship**.

This project demonstrates how to integrate **Supabase Authentication** with FastAPI to provide user registration, login, JWT-based authentication, protected routes, and logout functionality.

---

## 🚀 Features

- User signup
- User login
- Supabase authentication
- JWT access-token verification
- Protected API routes
- Authentication dependencies/middleware
- User authentication verification
- Logout functionality
- Swagger UI Bearer Authentication
- Secure environment-variable handling
- `.env` protection using `.gitignore`

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Supabase Auth**
- **JWT**
- **Uvicorn**
- **Swagger UI**
- **python-dotenv**

---

## 📁 Project Structure

```text
W2-A4-Auth/
├── auth.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/
    ├── signup.png
    ├── login.png
    ├── swagger-auth.png
    ├── protected-route.png
    └── logout.png
```

---

## 🔐 Authentication Flow

The API follows this authentication flow:

```text
User
  │
  ├── Signup
  │      ↓
  │   Supabase Auth
  │
  ├── Login
  │      ↓
  │   JWT Access Token
  │
  └── Protected API
         ↓
     Bearer Token
         ↓
   JWT Verification
         ↓
    Authorized User
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd W2-A4-Auth
```

---

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project directory.

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

Never commit the `.env` file to GitHub.

The project uses `.gitignore` to prevent sensitive credentials from being uploaded.

Example:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

---

## 🗄️ Supabase Configuration

1. Create a project in Supabase.
2. Open the Supabase project dashboard.
3. Navigate to **Authentication**.
4. Configure the authentication settings.
5. Copy the project URL.
6. Copy the required API key.
7. Add the credentials to your local `.env` file.

---

## ▶️ Run the API

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## 📖 Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test:

- Signup
- Login
- Protected routes
- JWT authentication
- Logout

---

## 🔑 Authentication with Swagger

After successfully logging in, the API returns an access token.

Copy the access token.

In Swagger UI:

1. Open `/docs`.
2. Click **Authorize**.
3. Enter the access token.
4. Click **Authorize**.
5. Close the authorization window.
6. Test the protected endpoint.

The token should be sent as a Bearer token:

```text
Authorization: Bearer <access_token>
```

---

## 🔗 API Endpoints

### Signup

```http
POST /signup
```

Creates a new user account using Supabase Authentication.

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

### Login

```http
POST /login
```

Authenticates an existing user.

Example request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

A successful login returns an authentication token.

---

### Protected Route

```http
GET /protected
```

This endpoint requires a valid JWT access token.

Example header:

```text
Authorization: Bearer <access_token>
```

Without a valid token, access should be denied.

---

### Logout

```http
POST /logout
```

Logs out the authenticated user/session.

A valid authentication token is required.

---

## 🛡️ Security

This project follows basic authentication security practices:

- Authentication is handled by Supabase.
- JWT tokens are verified before accessing protected routes.
- Protected endpoints require authentication.
- Credentials are stored in environment variables.
- `.env` is excluded from Git.
- `.env.example` contains only placeholder values.
- Secret keys are never hard-coded in source files.

---

## 🧪 Testing

The API can be tested using Swagger UI.

### Test Sequence

```text
1. Signup
   ↓
2. Login
   ↓
3. Copy access token
   ↓
4. Click Authorize
   ↓
5. Enter Bearer token
   ↓
6. Call protected endpoint
   ↓
7. Verify authenticated response
   ↓
8. Test logout
```

---

## 📸 Screenshots

Screenshots demonstrating the completed authentication API are stored in the `screenshots/` directory.

### Signup

![Signup](screenshots/signup.png)

### Login

![Login](screenshots/login.png)

### Swagger Authentication

![Swagger Authentication](screenshots/swagger-auth.png)

### Protected Route

![Protected Route](screenshots/protected-route.png)

### Logout

![Logout](screenshots/logout.png)

---

## ✅ Assignment Checklist

- [x] FastAPI application created
- [x] Supabase authentication integrated
- [x] User signup implemented
- [x] User login implemented
- [x] JWT authentication implemented
- [x] Protected route implemented
- [x] Authentication dependency implemented
- [x] Logout implemented
- [x] Swagger UI authentication tested
- [x] Environment variables configured
- [x] `.env` protected with `.gitignore`
- [x] `.env.example` added
- [x] Screenshots added
- [x] README documentation completed

---

## 🎯 Learning Outcomes

Through this assignment, I practiced:

- Integrating Supabase Auth with FastAPI
- Implementing user authentication
- Working with JWT access tokens
- Protecting API endpoints
- Using FastAPI dependencies for authentication
- Testing authenticated APIs through Swagger UI
- Managing secrets with environment variables
- Following secure Git/GitHub practices

---

## 👩‍💻 Internship

**FlyRank AI Internship — Backend Track**

**Assignment:** A4 — Supabase Authentication API

**Focus:** Authentication, JWT verification, protected APIs, and secure environment configuration.

---

## 📌 Important Security Note

The `.env` file contains private credentials and must **not** be committed to GitHub.

Only `.env.example` should be included in the repository with placeholder values.

```text
.env          → Private / DO NOT COMMIT
.env.example  → Safe template / COMMIT
```

---

## 📄 License

This project was created for educational and internship purposes as part of the FlyRank Backend Internship.