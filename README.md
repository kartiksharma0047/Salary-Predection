# 💼 Salary Prediction App (AI-Powered)

Welcome to the **AI-powered Salary Prediction Web App** built using `Streamlit`, `Gemini AI`, and various data science tools like `Pandas`, `Plotly`, `Matplotlib`, and `NumPy`.

> 🌐 **Live Demo**: [Click here to try it out](https://kartiksharma0047-salary-predection-app-vo4vkj.streamlit.app/)

---

## 📌 Project Overview

This app allows users to **estimate their expected salary** based on various factors such as job title, years of experience, location, education level, and more.  
It combines **data analytics** with **AI-powered predictions** using **Google's Gemini AI (Generative AI)**.

---

## 🚀 Key Features

### 🧠 AI Salary Prediction
- Integrates **Gemini (Gen AI)** to generate salary estimates using structured natural language prompts.
- Uses caching (`salary_cache.db`) with hashed inputs to avoid repeated API calls.

### 📊 Data Analysis and Visualization
- Multiple **interactive graphs** created using:
  - 📈 `Matplotlib` (static visualizations)
  - 📊 `Plotly` (dynamic and interactive graphs)

### 🧹 Data Cleaning and Munging
- `Pandas` used extensively to:
  - Clean raw data.
  - Apply filters for job titles, industry, experience, etc.
  - Display clean, interactive DataFrames.

### 📂 CSV Updation (CRUD-like Operation)
- Users can **contribute** salary data via a form.
- New entries are **appended to the CSV file**, making the dataset grow over time.

### 📑 Multi-Page Navigation with Streamlit
- Streamlit app includes **3 functional pages**:
  1. **Home** – Overview and visualizations.
  2. **Prediction** – Gemini AI salary estimate based on form inputs.
  3. **Contribute** – Submit your own salary data to improve the model.

### 🎨 Clean, Responsive UI
- Minimalistic design with **gradient effects**, layout grids, and styled elements.
- Progress bar simulates response time when waiting for AI.

---

## 🛠️ Tech Stack

| Technology      | Purpose                                  |
|-----------------|-------------------------------------------|
| Python          | Backend logic and data processing         |
| Streamlit       | UI and web deployment                     |
| Pandas          | Data wrangling and filtering              |
| NumPy           | Numerical operations                      |
| Matplotlib      | Static plots and visualizations           |
| Plotly          | Interactive data visualizations           |
| Gemini AI (GenAI) | Natural language salary estimation     |
| SQLite3         | Caching AI predictions (`salary_cache.db`) |
| .env / dotenv   | Secure API key management                 |

---

## ⚙️ How the AI System Works

1. **User Input**: The user fills a form with details like:
   - Job title, company size, industry, experience, location, education, remote or not.

2. **Input Hashing**: 
   - All input fields are combined and hashed to check if this combination was previously queried.
   - If found in SQLite cache (`salary_cache.db`) → show cached result.
   - Else → generate new prediction using Gemini AI.

3. **Prompt Generation**: 
   - A structured prompt is generated for Gemini

4. **AI Response**:
   - Gemini returns something like:  
     `₹6,00,000 - ₹8,50,000 per annum`

5. **Caching**: 
   - This result is stored in SQLite DB with timestamp and hash.

6. **Display**: 
   - The estimated salary is shown on-screen with a loading animation.

This ensures **performance**, **cost-efficiency**, and a **smooth user experience**.

---