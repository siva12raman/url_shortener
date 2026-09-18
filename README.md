# URL Shortener

A lightweight, efficient URL shortener service.

## Overview

This project provides a simple and fast service to convert long URLs into shortened, easy-to-share links, with analytics and custom alias support.

## Features

- **URL Shortening**: Generate short codes for long URLs.
- **Custom Aliases**: Allow users to specify custom short links.
- **Redirection**: Fast HTTP 301/302 redirects to target URLs.
- **Analytics & Tracking**: Track click counts, referrers, and basic analytics.
- **Expiration Dates**: Set optional expiration time for shortened links.

## Tech Stack (Planned)

- **Backend**: Python (FastAPI / Node.js)
- **Database**: SQLite / PostgreSQL / Redis
- **Frontend**: HTML / CSS / JS (or simple dashboard interface)

## Getting Started

### Prerequisites

- Python 3.10+ (or Node.js 18+)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/url-shortener.git
cd url-shortener

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run local dev server
python main.py
```

## API Specification (Placeholder)

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/shorten` | Create a shortened URL |
| `GET` | `/{code}` | Redirect to the original URL |
| `GET` | `/api/stats/{code}` | Get statistics for a short URL |

## License

MIT License
