# StayFlow — Supabase Monolith

A single Flask application for hotel discovery, guest booking, manager operations and administration. This revision removes SQLite and uses **Supabase Auth + Supabase PostgreSQL**.

## What changed

- Responsive StayFlow UI with improved public discovery, authentication, and guest onboarding.
- Guests can create their own accounts at `/register`; new self-service accounts are always assigned the `guest` role.
- Authentication is handled by Supabase Auth (email/password).
- Authorization remains server-side in Flask (`admin`, `manager`, `guest`) so changing browser data cannot elevate a role.
- Application data is stored in Supabase PostgreSQL. `sqlite3` and `hotel_booking.db` are no longer used.
- Admin-created manager/admin/guest accounts are provisioned in Supabase Auth with the server-only service-role key.
- `supabase/schema.sql` contains the database schema, constraints, indexes, and RLS enablement.

## Supabase setup

1. Create a Supabase project.
2. Open **SQL Editor** and run `supabase/schema.sql`.
3. In **Authentication > Providers**, keep Email enabled. Choose whether email confirmation is required for guest signup.
4. Copy `.env.example` to `.env` and fill `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, and `DATABASE_URL` from your Supabase project settings/connect dialog.
5. Keep the service-role key server-side only. Never place it in templates, frontend JavaScript, Git, or a public deployment variable exposed to clients.

The schema enables RLS and defines no browser-facing table policies because this Flask server is the trusted data boundary and connects to Postgres server-side. Supabase Auth remains the identity provider.

## Install and run

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## First admin

Create an Auth user in the Supabase dashboard (email/password), copy that user's UUID, then run this once in SQL Editor:

```sql
insert into public.users(auth_user_id, username, role, email)
values ('AUTH-USER-UUID', 'admin', 'admin', 'admin@example.com');
```

After that, the admin dashboard can create additional manager/admin accounts. Public registration can only create `guest` profiles.

## Demo data

After the schema and environment variables are configured:

```bash
python seed_demo_data.py
```

This adds sample hotels/rooms only; it does not create insecure default passwords.

## Security notes

Use strong random `SESSION_SECRET` and `JWT_SECRET` values in production, HTTPS, a restricted database credential, and Supabase's recommended production email/redirect settings. Uploaded hotel/room images are stored locally in `uploads/`; Supabase Storage can be added later if you want stateless/cloud media storage too.
