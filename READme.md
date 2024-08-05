# Lunch Decision Service

This service allows company employees to make decisions about lunch choices. Restaurants upload their menus daily via an API. Employees vote for the menu before leaving for lunch using a mobile app, for which the backend has been implemented.
## 👩‍💻 _Installation & Run_

### 🧠 Set up the environment

### 📝 Set environment variable

- Copy and rename the **.env.sample** file to **.env**
- Open the .env file and edit the environment variables
- Save the .env file securely
- Make sure the .env file in .gitignore

On Windows:
```python
python -m venv venv 
venv\Scripts\activate
```

On UNIX or macOS:
```python
python3 -m venv venv 
source venv/bin/activate
```

### 🗃️ Install requirements

```python
docker-compose up --build
```

### 👥 Create a superuser (optional)

If you want to perform all available features, create a superuser account in a new terminal:
```python
docker exec -it restaurant-db-1 /bin/sh
python manage.py createsuperuser
```

### 😄 Go to site [http://localhost:8000/](http://localhost:8000/)


## 📰 Features

- JWT Authentication
- Docker
- Celery


## 📝 Contributing

If you want to contribute to the project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Submit a pull request.

## 😋 _Enjoy it!_

---