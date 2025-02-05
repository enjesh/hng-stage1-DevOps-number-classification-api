# **hng-stage1-DevOps-number-classification-api**
HNG Internship project for DevOps Stage 1 - Number Classification API

---

# **Number Classification API**  

A FastAPI-based web service that classifies numbers based on their mathematical properties and provides fun facts.  

## **Features**  
✅ Check if a number is:  
- **Prime**  
- **Perfect**  
- **Armstrong**  
- **Odd/Even**  
✅ Get the **sum of digits** of the number.  
✅ Fetch a **fun fact** from the [Numbers API](http://numbersapi.com).  

---

## **Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/your-username/hng-stage1-DevOps-number-classification-api.git
cd hng-stage1-DevOps-number-classification-api
```

### **2️⃣ Set Up a Virtual Environment**  
```bash
python3 -m venv .venv
source .venv/Script/activate  # On Linux, use venv\bin\activate
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **Usage**  

### **Run the API Locally**
```bash
uvicorn numberApi:app --host 127.0.0.1 --port 8080 --reload
```
Now, visit:  
📌 **Swagger UI**: [`http://127.0.0.1:8080/docs`](http://127.0.0.1:8000/docs)  

---

## **API Endpoints**  

### **Classify a Number**  
#### **GET `/api/classify-number`**  
🔹 **Query Parameter**:  
- `number` (integer) – The number to classify.  

🔹 **Example Request**:  
```bash
curl "http://127.0.0.1:8080/api/classify-number?number=5"
```

🔹 **Example Response**:  
```json
{
    "number": 5,
    "is_prime": true,
    "is_perfect": false,
    "properties": ["odd"],
    "digit_sum": 5,
    "fun_fact": "5 is the number of Platonic solids."
}
```

---

## **Deploying to an Ubuntu Server on Azure**  

### **1️⃣ Install Dependencies on the Server**  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip -y
pip3 install virtualenv
```

### **2️⃣ Set Up the API**  
```bash
cd /opt
sudo mkdir myapi && cd myapi
sudo virtualenv .venv
source .venv/bin/activate
git clone https://github.com/your-username/hng-stage1-DevOps-number-classification-api.git .
pip install -r requirements.txt
```

### **3️⃣ Run the API**  
```bash
uvicorn numberApi:app --host 127.0.0.1 --port 8080 --reload
```

### **4️⃣ Configure a Systemd Service for Auto-Restart**  
```bash
sudo nano /etc/systemd/system/numberApi.service
```
Paste this:
```ini
[Unit]
Description=FastAPI Number Classification API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/opt/myapi
ExecStart=/opt/myapi/.venv/bin/uvicorn numberApi:app --host 0.0.0.0 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
```
Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start myapi
sudo systemctl enable myapi
```

### **5️⃣ Set Up Nginx Reverse Proxy**  
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/myapi
```
Paste:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Activate and restart:
```bash
sudo ln -s /etc/nginx/sites-available/myapi /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### **6️⃣ Secure with SSL (HTTPS)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

---

## **Testing**  
Run **pytest** to check API functionality:  
```bash
pytest
```

---

## **Contributing**  
Feel free to **fork** and submit a **pull request**! 🥳  

---

## **Author**
Elizabeth Njeri Kihuha

---

## **License**  
📜 MIT License.  

---

