# Resume Analytics Tool 📄

A smart resume analysis and feedback tool that compares your resume against job roles or custom job descriptions. Built with Streamlit and integrated with Snowflake for analytics storage.

## ✨ Features

* Upload your **resume (PDF)** and either:

  * Choose an **industry and job role**, or
  * Upload a **custom job description (PDF/TXT)**
* Extracts **keywords** from resume and JD
* Calculates **match score** and highlights matched/missing keywords
* Generates a downloadable **PDF report**
* Offers **AI-powered feedback** based on the analysis
* Stores resume analytics in **Snowflake database**
* A visual **dashboard** to view and filter past analyses

## 📑 Project Structure

```
resume-analytics/
├── .env                     # Contains environment variables (excluded from Git)
├── .gitignore              # Ignores config and environment secrets
├── app.py                  # Main Streamlit app
├── config.py               # Loads Snowflake config from environment
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── src/
    ├── compare_with_jobs.py
    ├── extract_keywords.py
    ├── fetch_from_snowflake.py
    ├── parse_resume.py
    ├── save_to_snowflake.py
    ├── suggest_feedback.py
```

## 🔑 Security

All credentials (e.g., Snowflake account, user, password) are stored securely in a **`.env`** file and accessed using **`os.getenv()`** in `config.py`. This file is ignored from Git using `.gitignore`.

## ⚡ Setup

1. **Clone the repo**:

```bash
git clone https://github.com/yourusername/resume-analytics.git
cd resume-analytics
```

2. **Create a virtual environment & install dependencies**:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Create `.env` file**:

```
SNOWFLAKE_ACCOUNT=xxxxx
SNOWFLAKE_USER=xxxxx
SNOWFLAKE_PASSWORD=xxxxx
SNOWFLAKE_ROLE=xxxxx
SNOWFLAKE_WAREHOUSE=xxxxx
SNOWFLAKE_DATABASE=xxxxx
SNOWFLAKE_SCHEMA=xxxxx
SNOWFLAKE_TABLE=xxxxx
```

4. **Run locally**:

```bash
streamlit run app.py
```

## 🌐 Deployment

You can deploy this on **[Streamlit Cloud](https://streamlit.io/cloud)** for free.

Steps:

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and log in
3. Click **"New app"**, select the GitHub repo and `app.py`
4. Set your **secrets** in the Streamlit cloud dashboard for `.env` keys
5. Deploy and share the link!

## 🚀 Coming Soon

* AI-powered **resume suggestions**
* Support for **multiple resume uploads**
* Email alerts (optional)

---

Made with ❤️ by [Parvez Mohammad](mailto:parvez2114@gmail.com)
