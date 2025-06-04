# Complete TR Chatbot (Single-Folder Demo)
```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```
Endpoints:
* `POST /register` {username,password,role}
* `POST /login` -> token
* `POST /chat` header `Authorization: Bearer <token>`
* `POST /pref` set daily notification utc hour
```
