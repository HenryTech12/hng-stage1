# 🧠 String Analyzer API

The **String Analyzer API** is a Django REST Framework (DRF) project that allows users to analyze strings and store their computed properties — such as whether they are palindromes, their length, character frequency, and more.
It also supports **natural language-based filtering**, letting users query data using plain English phrases.

---

## 🚀 Features

* 🔤 **Add and analyze strings** (e.g., check if a string is a palindrome)
* 🔍 **Search and filter** analyzed strings using query parameters
* 💬 **Filter with natural language queries** (e.g., *“show palindromic strings longer than 5 characters”*)
* ⏱️ **Auto-timestamped** records
* 🧾 **JSON-based properties** field for storing string metrics
* 🛠️ Built on **Django REST Framework (DRF)** for clean and robust RESTful endpoints

---

## 🧩 Tech Stack

* **Backend:** Django 5+, Django REST Framework
* **Database:** SQLite (default) or PostgreSQL
* **Language:** Python 3.11+
* **Libraries:** `djangorestframework`, `hashlib`, `re`

---

## 📂 Project Structure

```
string_analyzer/
│
├── analyzer/
│   ├── models.py          # Analyzer model
│   ├── views.py           # API logic (CRUD + Natural Language Filter)
│   ├── serializer.py      # DRF serializer
│   ├── urls.py            # Analyzer app routes
│
├── string_analyzer/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root project routes
│
└── manage.py
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/string-analyzer-api.git
cd string-analyzer-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Start the Server

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints

### **1️⃣ Create or Analyze a String**

**POST** `/strings/`

**Example Request**

```json
{
  "value": "madam"
}
```

**Example Response**

```json
{
  "id": 1,
  "value": "madam",
  "properties": {
    "length": 5,
    "is_palindrome": true,
    "word_count": 1,
    "character_frequency_map": {
      "m": 2,
      "a": 2,
      "d": 1
    }
  },
  "created_at": "2025-10-22T14:30:00Z"
}
```

---

### **2️⃣ Get All Analyzed Strings**

**GET** `/strings/`

Returns all stored strings and their computed properties.

---

### **3️⃣ Filter by Parameters**

**GET** `/strings/?is_palindrome=true&min_length=3`

Filters based on JSON fields like palindrome status, length, or word count.

---

### **4️⃣ Filter by Natural Language**

**GET** `/strings/filter-by-natural-language?query=<your query>`

**Example Requests**

```
GET /strings/filter-by-natural-language?query=palindromic strings
GET /strings/filter-by-natural-language?query=strings longer than 5 characters
GET /strings/filter-by-natural-language?query=single word strings
GET /strings/filter-by-natural-language?query=strings containing the letter a
```

**Example Response**

```json
{
  "data": [
    {
      "id": 1,
      "value": "madam",
      "properties": {
        "length": 5,
        "is_palindrome": true,
        "word_count": 1,
        "character_frequency_map": {
          "m": 2,
          "a": 2,
          "d": 1
        }
      },
      "created_at": "2025-10-22T14:30:00Z"
    }
  ],
  "count": 1,
  "interpreted_query": {
    "original": "palindromic strings",
    "parsed_filters": {
      "is_palindrome": true
    }
  }
}
```

---

## 🧠 How Natural Language Filtering Works

The `/strings/filter-by-natural-language` endpoint uses regular expressions to interpret human-like phrases and automatically applies Django ORM filters.

| Example Query                        | Parsed Filter                          |
| ------------------------------------ | -------------------------------------- |
| `palindromic strings`                | `is_palindrome=True`                   |
| `strings longer than 5 characters`   | `length__gte=6`                        |
| `strings shorter than 10 characters` | `length__lte=9`                        |
| `single word strings`                | `word_count=1`                         |
| `strings containing the letter a`    | `character_frequency_map__has_key='a'` |

---

## 🧪 Example Testing with cURL

```bash
curl -X GET "http://127.0.0.1:8000/strings/filter-by-natural-language?query=palindromic strings"
```

---

## 📘 API Documentation

If you use **DRF Browsable API**, visit:

```
http://127.0.0.1:8000/strings/
```

---

## 🛡️ Error Handling

The API returns standard HTTP response codes:

| Status Code                 | Meaning                  |
| --------------------------- | ------------------------ |
| `200 OK`                    | Successful Request       |
| `400 Bad Request`           | Missing or invalid query |
| `404 Not Found`             | No matching results      |
| `500 Internal Server Error` | Unexpected backend error |

