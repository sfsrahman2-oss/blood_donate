# Blood Donate & Request System

A Django-based web application where users can register as blood donors, create blood
requests, and find suitable donors based on blood group and location.

Built for the Final Django Assignment: **Blood Donate & Request System**.

## Features Implemented

- **User Registration & Login** — Django's built-in auth system, extended with a
  `UserProfile` model (phone number, blood group, location, date of birth, profile picture).
- **Donor Profile** — logged-in users can create/update a `DonorProfile` (one per user),
  including availability status (`Available` / `Not Available`).
- **Blood Requests** — full CRUD: create, view, edit, delete, and update status
  (`Pending` / `Fulfilled` / `Cancelled`), restricted to the request's owner.
- **Donor Search** — filter donors by blood group, location, and availability.
- **Blood Request Listing** — filter requests by blood group, location, and status,
  with pagination.
- **Request Details Page** and **Donor Details Page** with full information.
- **Ownership restrictions** — users can only edit/delete their own donor profile and
  their own blood requests (enforced in views, not just the UI).
- **Home Page** with a welcome hero, quick actions, and live stats.
- **Navigation Bar** with links that adapt to logged-in/logged-out state.
- **Form Validation** — required fields, phone number format, positive bag count,
  future-dated required date, blood group choices.
- **Django Messages** for success/error feedback.
- **Pagination** on donor and request listings.
- **Admin dashboard** — all models registered with list/search/filter configuration.

## Tech Stack

- Django 5/6 (tested with Django 6.1)
- SQLite (default, zero-config)
- Pillow (for profile picture / `ImageField` support)
- Plain CSS (no frontend framework required)

## Project Structure

```
blooddonate/
├── manage.py
├── requirements.txt
├── blooddonate/          # Project settings, root URLs
├── donors/               # Main app: models, views, forms, urls, admin
│   ├── models.py         # UserProfile, DonorProfile, BloodRequest
│   ├── forms.py          # SignUpForm, UserProfileForm, DonorProfileForm,
│   │                       BloodRequestForm, DonorSearchForm, RequestFilterForm
│   ├── views.py          # All CRUD + auth + search views
│   ├── urls.py
│   ├── admin.py
│   └── templates/donors/ # App-specific templates
├── templates/            # base.html + registration/login.html + register.html
├── static/css/style.css  # Site-wide stylesheet
└── media/                # Uploaded profile pictures (created at runtime)
```

## Setup Instructions

1. **Clone the repository and enter the project folder:**
   ```bash
   git clone <your-repo-url>
   cd blooddonate
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create an admin superuser (optional, for `/admin/`):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Visit the site:**
   - Main site: http://127.0.0.1:8000/
   - Admin dashboard: http://127.0.0.1:8000/admin/

## Notes on Settings

- `DEBUG = True` and `ALLOWED_HOSTS = ['*']` are set for local development/grading
  convenience. **Change these before any real deployment** — set `DEBUG = False` and
  list your actual domain(s) in `ALLOWED_HOSTS`.
- Media files (profile pictures) are served by Django's dev server only while
  `DEBUG = True`. In production, configure your web server (or a service like
  Cloudinary/S3) to serve `MEDIA_URL`/`MEDIA_ROOT`.
- The `SECRET_KEY` in `settings.py` is a development key. Replace it with an
  environment-variable-based secret before deploying anywhere public.

## Suggested Pages Map

| Page                     | URL                          |
|--------------------------|-------------------------------|
| Home                     | `/`                            |
| Register                 | `/register/`                   |
| Login / Logout           | `/login/`, `/logout/`          |
| My Profile / Edit        | `/profile/`, `/profile/edit/`  |
| Donor List (search)      | `/donors/`                     |
| Donor Details            | `/donors/<id>/`                |
| Become a Donor           | `/donors/become/`              |
| Edit My Donor Profile    | `/donors/edit/`                |
| Blood Request List       | `/requests/`                   |
| Blood Request Details    | `/requests/<id>/`               |
| Create Blood Request     | `/requests/create/`            |
| Edit / Delete My Request | `/requests/<id>/edit/`, `/requests/<id>/delete/` |
| My Requests              | `/requests/mine/`              |
| Admin Dashboard          | `/admin/`                      |

## Bonus Features Included

- Pagination on donor and request listings
- Profile picture upload (via `UserProfile.profile_picture`)
- Success/error messages using Django Messages
- Multi-field filtering on both donor search and request listing

## Testing

The application was manually smoke-tested end-to-end (registration → donor profile
creation/editing → blood request creation/editing/status update/deletion → search &
filter → ownership/permission checks → logout), with all flows behaving as expected
and form validation correctly rejecting invalid input (e.g. non-numeric phone numbers,
zero/negative bag counts).
