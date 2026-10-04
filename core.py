import os, json, re
from datetime import datetime, timedelta
import ollama
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
col = MongoClient(os.environ["MONGO_URI"])["homememory"]["items"]
MODEL, EMBED = "gemma4:latest", "embeddinggemma"
MIN_SCORE = 0.5  # raise if wrong matches appear, lower if real ones are rejected
CATEGORIES = ["belonging", "document", "wifi_info", "medicine", "outfit", "receipt", "other"]
KEYS = ["category", "item", "description", "location_hint", "text_found", "expiry_date", "people", "amount"]
SCHEMA = {"type": "object", "required": KEYS,
          "properties": {k: ({"type": "string", "enum": CATEGORIES} if k == "category" else {"type": "string"}) for k in KEYS}}

PROMPT = """You help a family remember things. Describe this photo as JSON.
category: belonging = any physical object kept somewhere (wallet, keys, bag, jewelry, laptop, charger, glasses), even if it holds cards or papers.
document = mainly a paper/card itself (ID, degree, passport). wifi_info, medicine, outfit, receipt as named. Otherwise other.
item = short name. description = colours/type you SEE. text_found = important text/numbers actually readable.
expiry_date = YYYY-MM-DD or empty string. Use empty string for anything unclear. Never guess numbers, dates or passwords.
The user's note is the truth about WHERE something is: never contradict it."""


def parse_json(t):
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        return json.loads(m.group(0)) if m else {}


def to_date(s):
    try:
        return datetime.strptime(str(s).strip(), "%Y-%m-%d")
    except Exception:
        return None


def extract(img_bytes, note=""):
    r = ollama.chat(model=MODEL, format=SCHEMA, options={"temperature": 0},
                    messages=[{"role": "user", "content": PROMPT + f"\nUser note: {note}", "images": [img_bytes]}])
    return parse_json(r["message"]["content"])


def _embed(t):
    return ollama.embed(model=EMBED, input=t)["embeddings"][0]


def save(f, note, image_path):
    doc = {k: f.get(k) or "" for k in KEYS}
    doc.update(location_hint=doc["location_hint"] or note, user_note=note, image_path=image_path,
               expiry_date=to_date(f.get("expiry_date")), created=datetime.now())
    text = f"{note}. {doc['item']}. {doc['category']}. {doc['description']}. {doc['location_hint']}. {doc['text_found']}"
    doc["embedding"] = _embed(f"title: {doc['item'] or 'none'} | text: {text}")
    col.insert_one(doc)


def ask(q):
    hits = list(col.aggregate([
        {"$vectorSearch": {"index": "vector_index", "path": "embedding", "numCandidates": 100, "limit": 3,
                           "queryVector": _embed(f"task: search result | query: {q}")}},
        {"$addFields": {"score": {"$meta": "vectorSearchScore"}}},
        {"$project": {"embedding": 0, "_id": 0}}]))
    if not hits or hits[0]["score"] < MIN_SCORE:
        return None, []
    sys = (f"You are Memo, a friendly family memory assistant. Today is {datetime.now():%Y-%m-%d}. "
           "Answer ONLY from the records. Use the user_note wording for locations, but speak to the user as you/your (turn my into your). Never mention records or entries. If several match, use the newest. Write a natural sentence, never copy the note word for word. Example: note 'wallet,side table,my bedroom' -> 'Your wallet is on the side table in your bedroom.' Max 2 short sentences. "
           "Reply in the user's language (English, Urdu or Roman Urdu). Never give medical advice.")
    r = ollama.chat(model=MODEL, options={"temperature": 0}, messages=[
        {"role": "system", "content": sys},
        {"role": "user", "content": f"Records:\n{json.dumps(hits, default=str)}\n\nQuestion: {q}"}])
    return r["message"]["content"], hits


def due_soon(days=60):
    lim = datetime.now() + timedelta(days=days)
    return list(col.find({"expiry_date": {"$ne": None, "$lte": lim}}, {"embedding": 0}).sort("expiry_date", 1))


def stats():
    return {"total": col.count_documents({}), "soon": len(due_soon(60)),
            "cats": list(col.aggregate([{"$group": {"_id": "$category", "n": {"$sum": 1}}}, {"$sort": {"n": -1}}]))}


def recent(n=6):
    return list(col.find({}, {"embedding": 0}).sort("created", -1).limit(n))


def delete(doc_id):
    from bson import ObjectId
    col.delete_one({"_id": ObjectId(doc_id)})
