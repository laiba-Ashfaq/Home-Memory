
# HomeMemory

> A private memory assistant for the small things families keep forgetting.

## About

HomeMemory is a personal memory assistant designed to help families remember where important everyday things are and keep track of dates such as document or medicine expiry dates.

The idea came from a simple experience: my mother once left her credit card behind at a shop. It made me think about how often we forget small but important things at home — where we kept our wallet, keys, receipts, documents, or other belongings.

Instead of expecting someone to remember everything, HomeMemory lets them simply **ask**.

## What It Does

With HomeMemory, you can:

* Take or upload a photo of an item.
* Add a short note about where it is.
* Use an open model to analyze the photo and extract useful details.
* Review and edit the information before saving it.
* Ask questions about saved items in English, Urdu, or Roman Urdu.
* Get the original photo as evidence for the answer.
* View upcoming medicine and document expiry dates through the **Due Soon** section.

## How It Works

```text
Photo + Note
     ↓
Image Analysis
     ↓
Review & Edit
     ↓
Save to Memory
     ↓
Ask a Question
     ↓
Find Matching Memory
     ↓
Answer + Original Photo
```

The system is designed around the idea that the user's own saved information should remain the source of truth.

## Key Features

### 📸 Remember Things

Save a photo together with a short description or location, such as:

> "Wallet on the side table in my bedroom."

### 🔎 Ask Later

Instead of searching manually, ask:

> "Where is my wallet?"

HomeMemory searches the saved memories and provides the relevant answer along with the original photo.

### 🌐 Multilingual Questions

Users can ask questions in:

* English
* Urdu
* Roman Urdu

### 📅 Due Soon

HomeMemory can keep track of important dates and highlight medicines and documents that are approaching their expiry date.

### ✏️ Review Before Saving

AI-generated information can be checked and edited before it becomes part of the user's memory.

### 🔒 Privacy First

HomeMemory is designed around keeping personal family information private. The project uses open models and is intended to keep sensitive memories and photos local rather than sending them to external AI services.

## Technology

The project uses:

* **Gemma** — open model for image understanding
* **ollama**- open model
* **python**- Language
* **Mongodb atlas**- Database



## Project Structure

```text
HomeMemory/
├── core.py/
├── app.py/
├── eval.py
├── README.md
└── .gitignore
```



## Evaluation

The project includes an evaluation script for testing how reliably HomeMemory retrieves the correct memory.

Run:

```bash
python eval.py
```

Add the final evaluation result here after running the test:

```text
Accuracy: XX/XX
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd HomeMemory
```

### 2. Install dependencies

Use the dependency instructions for the frontend and backend.

For Python:

```bash
pip install -r requirements.txt
```

### 3. Configure the application

Create your local environment configuration if required.

**Do not commit `.env` files or API keys to GitHub.**

### 4. Run the application

Use the appropriate commands for your frontend/backend setup.

## Demo

🎥 **Demo Video:** [YOUR_VIDEO_LINK](https://youtu.be/1i7o2_LhIHk)

The demo shows:

1. The problem HomeMemory is designed to solve.
2. Adding a memory with a photo and note.
3. Image analysis and editable information.
4. Asking a question about a saved item.
5. The answer with the original photo as proof.
6. The Due Soon section.

## Screenshots

<img width="1278" height="547" alt="image" src="https://github.com/user-attachments/assets/703e6f94-98c1-4105-b5b6-ba55713c3e8b" />


### Home

<img width="1278" height="547" alt="image" src="https://github.com/user-attachments/assets/a65675b3-69db-490f-81ad-8b2714d5f69e" />


### Add Memory

<img width="1279" height="535" alt="image" src="https://github.com/user-attachments/assets/9eeccae4-2720-461c-a8fc-963b001fca0c" />


### Ask
<img width="1278" height="535" alt="image" src="https://github.com/user-attachments/assets/f5eb7291-5abb-4123-8a39-c56dde579f88" />


### Due Soon

<img width="1271" height="523" alt="image" src="https://github.com/user-attachments/assets/abd4efe6-2f2b-4928-ad58-d2151d4ce6d4" />


## Why HomeMemory?

We often remember that we own something but forget **where we put it**.

HomeMemory turns those small memories into something searchable.

Instead of:

> "Where did I put my wallet?"

you can simply ask HomeMemory.


## Hacktoberfest Weekend Challenge

Built for the **Hacktoberfest Weekend Challenge 2026**.

## Author

**Laiba Ashfaq**

Software Engineering

## License

Add your chosen license here.
