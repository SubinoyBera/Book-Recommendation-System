# End to End Book Recommender System

Book Recommendation System is a type of information filtering system that suggests books to users besed on their reading preferences, interests and behaviour. Such recommender systems helps to create loyal customers, improves user experiences and increasing sales by recommending them relevant products & services for which they came to your site!

This project is a machine learning based collaborative-filtering book recommendation system that leverges user behavior and preferences to suggest books to readers. The system also has AI feature to recommend relevant books from book description provided by user. Performed exploratory data analysis, developed end-to-end ML pipeline along with semantic search pipeline.


## ⚡ Features
- Provides options of two types of recommendation engines :-
  * ML based recommendation.
  * Semantic recommendation.

- For ML based recommendation --
  * Select your favourite book from the dropdown list of available books.
  * Uses a trained ML model besed on Nearest Neighbors clustering algorithm to recommend you 5 most similar books from the avilable books.
  * Also displays the recommended books images for better understanding and user experience!

- For Semantic Recommendation --
  * Write a description about what type of books you want; example: "Books about life and Nature."
  * Uses Google Embedding-model to generate the dense-vector embeddings of the query for getting the semantic meaning.
  * Performs similarity search in the ChromaDB vector store to retrieve the most similar books and recommends to you.

- Also provides you the option for re-training of the ML model on the existing dataset in case if some unexpected happens! 


## 🛠️ Tech Stack
<ul>
    <li><b>Python</b> : Core programming language and backend logic.</li>
    <li><b>Pandas & NumPy</b> : Data manipulation and numerical analysis.</li>
    <li><b>SciPy</b> : For scientific analysis.</li>
    <li><b>Scikit-learn</b> : Machine Learning algorithms.</li>
    <li><b>Streamlit</b> : Lightweight web application framework.</li>
    <li><b>LangChain</b> : Framework for creating LLM based applications.</li>
    <li><b>Google-GenAI</b> : For generating vector embeddings using Google Embedding models.</li>
    <li><b>ChromaDB</b> : Lightweight local vector store.</li>
</ul>


## 📊 Dataset Info
<b>Source</b> : Book Crossing Dataset.<br>
<b>Books</b> : 270,000+ book records.<br>
<b>Users</b> : 278,000+ registered users.<br>
<b>Ratings</b> : 1.1M+ book ratings (scale 1-10).<br>
<b>Features</b> : Book titles, authors, publication years, ISBNs, user-ids, cover image urls.
<br>


## 🚀 Get Started

<b>STEP: 01 - Clone the repository</b>

```bash
git clone https://github.com/SubinoyBera/Book-Recommender-System
cd Book-Recommender-System
```

<b>STEP: 02 - Create and activate conda evironment</b>

```bash
conda create -p venv python=3.11.5 -y
conda activate venv
```

<b>STEP: 03 - Install project requirements</b>

```bash
pip install -r requirements.txt
```

Create a file named `.env` in the root directory and add your Gemini API key:

```env
GOOGLE_API_KEY = your_google_gemini_api_key
```

<b>STEP: 04 - Run the application</b>

```bash
streamlit run app.py
```
Then open the local URL shown in your terminal (usually `http://localhost:8501`) in a browser.
<br>

### 📌 Contributing :
Want to add new features or any improvement, fix bug, etc.. - Please feel free to contact and/or make a pull request. Looking forward for your contributions, suggestions and ideas! Your contibution can make a significant difference!!<br>
For any issues or problem while you find, please report it with proper details in the `issues` section.

<br>

<b>THANK YOU ! 🙏🎗️ </b>
<br>
*with regards : Subinoy Bera (author)* <br>
🧡🤍💚