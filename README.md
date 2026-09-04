# Django In-Memory Cache

A beginner-friendly Django project that demonstrates how to use **Django's Local Memory Cache** to reduce unnecessary database queries and understand the basic concept of caching.

This project was created specifically for beginners who are learning Django caching and want a simple, practical example that they can run locally and understand easily.

---

## Project Overview

Caching is an important concept in backend development.

Instead of querying the database every time a user requests the same data, Django can temporarily store frequently used data in a cache.

In this project, a list of YouTube users is retrieved from the database and stored in Django's **Local Memory Cache** for a limited amount of time.

The project demonstrates:

* Cache Miss
* Cache Hit
* Setting data in cache
* Retrieving data from cache
* Cache expiration
* Manually clearing cached data
* Django Admin custom actions
* Database-backed user data
* Django messages for cache status

The goal is not to build a complex production system, but to provide a simple example that beginners can use to understand how Django caching works.

---

## What is In-Memory Cache?

Django provides different cache backends.

This project uses:

```python
django.core.cache.backends.locmem.LocMemCache
```

Local Memory Cache stores cached data in the memory of the running Django process.

For example:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

This makes Local Memory Cache very easy to use while learning because it does not require Redis, Memcached, or another external caching service.

---

## How Caching Works in This Project

When the user opens the users list page, Django first checks whether the user data already exists in the cache.

```python
users = cache.get("user_data")
```

### Cache Miss

If the data does not exist in the cache, Django retrieves it from the database:

```python
users = YouTubeUser.objects.all()
```

The result is then stored in the cache:

```python
cache.set("user_data", users, timeout=20)
```

The cached data remains available for **20 seconds**.

The application displays:

```text
Cache Miss: Fetching data from database
```

### Cache Hit

If the data is already available in the cache, Django uses the cached data instead of fetching it again from the database.

```text
Cache Hit: Fetching Data From Cache
```

This helps beginners understand the basic difference between a database request and a cached response.

---

## Cache Flow

```text
User Request
     |
     v
Check Cache
     |
     +----------------------+
     |                      |
     v                      v
Cache Miss              Cache Hit
     |                      |
     v                      v
Fetch from Database     Get from Cache
     |                      |
     v                      |
Store in Cache             |
     |                      |
     +----------+-----------+
                |
                v
          Display Users
```

---

## Admin Cache Clearing

The project also includes a custom Django Admin action that allows the administrator to manually clear the cached user data.

```python
@admin.action(description="Clear The cache")
def clear_user_cache(modeladmin, request, queryset):
    cache.delete("user_data")
    messages.success(request, "Clear Cache Successfully")
```

This demonstrates how cached data can be deleted programmatically.

After clearing the cache, the next request will produce a **Cache Miss** and Django will fetch the data from the database again.

---

## Model

The project uses a simple `YouTubeUser` model:

```python
class YouTubeUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribers = models.IntegerField(default=0)

    def __str__(self):
        return self.name
```

It contains:

| Field         | Type         | Description           |
| ------------- | ------------ | --------------------- |
| `name`        | CharField    | YouTube user's name   |
| `email`       | EmailField   | Unique email address  |
| `subscribers` | IntegerField | Number of subscribers |

---

## Technologies Used

* Python
* Django 6.0.7
* SQLite
* Django Local Memory Cache
* Django Templates
* Django Admin
* Django Messages

---

## Project Structure

```text
dj34_InMemoryCache/
│
├── manage.py
├── db.sqlite3
│
├── dj34_InMemoryCache/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── youtube/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── tests.py
│
└── templates/
    └── cache/
        └── user_list.html
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd dj34_InMemoryCache
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install Django:

```bash
pip install django
```

---

## Database Setup

Run migrations:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## Create Admin User

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Follow the instructions in the terminal.

---

## Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## Testing the Cache

You can easily test the cache behavior.

### First Request

Open the users page.

You should see:

```text
Cache Miss: Fetching data from database
```

Django retrieves the users from SQLite and stores the result in Local Memory Cache.

### Second Request

Refresh the page within 20 seconds.

You should see:

```text
Cache Hit: Fetching Data From Cache
```

This means Django retrieved the data from the cache.

### After 20 Seconds

Wait until the cache expires and refresh the page again.

You should see:

```text
Cache Miss: Fetching data from database
```

Django will query the database again and create a new cache entry.

---

## Clearing the Cache From Admin

Go to:

```text
http://127.0.0.1:8000/admin/
```

Log in using your superuser account.

Open the `YouTubeUser` section, select a user, and choose:

```text
Clear The cache
```

After executing the action, the cached `user_data` will be deleted.

The next request will result in a cache miss.

---

## Important Learning Concepts

This project is mainly designed to help beginners understand these Django concepts:

### `cache.get()`

Retrieves data from the cache.

```python
users = cache.get("user_data")
```

### `cache.set()`

Stores data in the cache.

```python
cache.set("user_data", users, timeout=20)
```

### `cache.delete()`

Removes data from the cache.

```python
cache.delete("user_data")
```

### Cache Timeout

The project uses:

```python
timeout=20
```

This means the cached data expires after 20 seconds.

---

## Why Local Memory Cache?

Local Memory Cache is useful for learning because it is simple.

You do not need to install or configure:

* Redis
* Memcached
* Docker
* External cache servers

Everything works locally through Django.

This makes it a good starting point for beginners before moving toward more advanced caching systems.

---

## Limitations

Local Memory Cache is mainly useful for development, learning, and simple use cases.

It has important limitations compared with production-oriented caching systems.

For example, cached data is stored in the memory of the Django process and is not designed to provide a shared cache across multiple application servers.

For production applications, developers commonly consider dedicated caching systems such as Redis or Memcached depending on the application's requirements.

---

## Learning Path

This project can be used as a starting point for learning Django caching.

A beginner can continue by exploring:

```text
Django Local Memory Cache
        |
        v
Cache Keys & Timeouts
        |
        v
Cache Decorators
        |
        v
Template Fragment Caching
        |
        v
Database Query Caching Concepts
        |
        v
Redis
        |
        v
Production Caching Strategies
```

---

## Purpose of This Project

This project was built as a **Django learning project** with a specific focus on making caching concepts easy to understand.

Instead of introducing Redis or complex infrastructure immediately, it starts with Django's built-in Local Memory Cache so beginners can focus on understanding the fundamental caching workflow.

The project demonstrates a simple real-world idea:

> Check the cache first. If the data is not available, fetch it from the database, store it in the cache, and use the cached data for subsequent requests.

---

## Author

**Sultan Zaib**

Python Engineer | Django Engineer | Backend Engineer

Focused on learning and building backend applications with Python and Django.

---

## License

This project is available for educational and learning purposes.

You are free to use the code to learn Django caching, experiment with the project, and build your own projects from the concepts demonstrated here.

---

## Built With

Built with Django and Python by **Sultan Zaib**.

```

