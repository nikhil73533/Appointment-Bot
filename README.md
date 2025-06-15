Here's the **modified README file** for your new project, keeping the structure of the previous README while incorporating your updated functionality and tech stack:

---

# Appointment Management AI Agent

## Overview

This project showcases an AI-powered appointment management agent capable of handling user registrations and performing key CRUD operations—**Create, Read, Update, and Delete appointments**. It also sends **automated email alerts** for each task using a Gmail SMTP server. The frontend is built with Vite + React, while the backend leverages **FastAPI**, **Gemini 2.5 Flash**, and **SQLite3**. The project is deployed on **Vercel**.

**Summary of Functionality and High-Level Approach**

This application enables real-time appointment handling and user management using AI and modern full-stack technologies. Key components of the implementation include:

1. **AI Agent Functionality (Gemini 2.5 Flash)**:

   * Uses prompt engineering to interface with the Gemini LLM, which performs contextual task handling such as scheduling, updating, and canceling appointments.
   * Can also handle user registration and trigger appropriate responses.

2. **Email Notification System**:

   * Automatically sends email alerts on appointment creation, updates, and deletions using **Gmail SMTP**. Credentials and keys are securely managed via `.env`.

3. **Frontend (Vite + React)**:

   * A modern, responsive interface for users to interact with the AI assistant.
   * Built using HTML, CSS, JavaScript, and React.js, and optimized via the Vite build tool.

4. **Backend (FastAPI)**:

   * A robust, asynchronous API backend powered by FastAPI.
   * Integrates Gemini API, SQLite3 for storage, and handles user input/output routing.

5. **Deployment**:

   * Deployed on **Vercel** for frontend and backend integration.
   * Also supports local development with ease.

## Prerequisites

1. **Python Version**: Python 3.10 or higher.
2. **Node Version**: Node.js LTS version (recommended).
3. **API Key**: A valid Gemini API key (add to `.env` file).
4. **Email Credentials**: Sender email address and password for Gmail SMTP (add to `.env`).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nikhil73533/Appointment-Bot.git
   cd Appointment-Bot
   ```

2. **Backend Setup**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Frontend Setup**:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Running the Backend**:

   ```bash
   cd ..
   python3 setup.py
   ```

## Usage

After completing the setup steps above, the application will be available on your local machine. You can access the frontend in your browser and begin interacting with the assistant to register users and manage appointments with real-time updates and email notifications.

## Environment Variables

Create a `.env` file in the root directory and add the following:

```env
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_ADDRESS=your_sender_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
```

## Video Demonstration

To view a demonstration of the product, click below:

[Demo Video](https://www.canva.com/design/DAGqcOJZzdI/bnZMl5i8lCzvFrbXPg18Ew/watch?utm_content=DAGqcOJZzdI&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h3e5fb07884)

## Live Deployment

Try the live version of the product here:

[Product Link](https://appointment-bot-eight.vercel.app/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you also want a short version for a project portfolio or CV.
