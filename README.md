# ✈️ CultureTrip Planner

> “Where you go next depends on what you love.”

**CultureTrip Planner** is a smart, culturally-aware travel assistant that builds personalized trip itineraries based on your mood, tastes (like music, food, fashion, or books), and travel goals (relax, explore, party). Powered by **GPT-4** and **Qloo’s Taste AI**, it crafts immersive experiences tailored just for you.

---

## 🧠 Concept Summary

Imagine telling your assistant:

> _"I'm going to Lisbon for 5 days. I want something relaxing and artistic, with a love for jazz, seafood, indie fashion, and books."_

CultureTrip Planner will generate a daily itinerary that includes:

- 🥘 Food spots aligned with your taste
- 🎶 Local jazz venues
- 🛍️ Indie boutiques
- 📚 Book cafés
- 🖼️ Artistic walks and cultural gems

---

## 🧭 User Flow

1. **User Input:**

   - Destination: _Lisbon_
   - Duration: _5 days_
   - Travel Style: _Relaxing, artistic, low budget_
   - Taste Preferences: _Jazz, seafood, indie fashion, books_

2. **Backend Workflow:**

   - GPT interprets mood and goals
   - Qloo provides geo-aware, taste-specific recommendations
   - GPT assembles everything into a custom itinerary

3. **User Output:**
   - Daily breakdown with morning, afternoon, and evening suggestions
   - Embedded map links
   - Share/export options

---

## How to run the project

1. Create a New Conda Environment
   `conda create -n ai-qloo-ify python=3.11`
2. Create a New Conda Environment
   `conda activate ai-qloo-ify`

3. Install pip inside the conda environment (optional, but safe to check)
   `conda install pip`

4. Install your dependencies from requirements.txt
   `pip install -r requirements.txt`

5. Verify Installed Packages
   `pip list`

6. If you want to save the exact environment for others to use with Conda, you can later export:
   `conda env export > environment.yml`
   OR recreate it using:
7. `conda env create -f environment.yml`

8. Use pip install and add package to requirement.txt file
   `pip install pydantic-settings`
   `echo pydantic-settings >> requirements.txt`
   OR Option 2: Re-freeze your environment. After installing the package, run:
   `pip freeze > requirements.txt`
   Note : This overwrites requirements.txt with everything currently installed in your environment — good for syncing it all, but might include extras you don’t want.

9. Start Project Server :
   `uvicorn app.main:app --reload`

## Some endpoint to check

http://127.0.0.1:8000 → Welcome message
http://127.0.0.1:8000/docs → Swagger UI

## Example of git workflow

# 1. Create and switch to the new branch

git checkout -b LLM-userhistory

# 2. Now you're on qloo-pipeline branch. Just add and commit your changes:

git add .
git commit -m "LLM codes with user history and data formatting"

# 3. Push the branch to remote

git push origin LLM-userhistory

# 4. Switch back to the main branch

git checkout main

# 5. Pull latest changes from remote (optional, to sync)

git pull origin main

# 6. Merge the changes from qloo-pipeline into main

git merge LLM-userhistory

# 7.

git push origin main
