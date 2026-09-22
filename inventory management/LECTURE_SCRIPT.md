# Employee Leave & Asset Management System — 30 Minute Lecture Script

**Delivery notes:** roughly 4,300 spoken words, about 30 minutes at a normal pace.
Timing markers are cumulative. `[DEMO]` means switch to the browser, `[CODE]` means
switch to the editor. If you run short on time, the compressible sections are marked
`[CAN TRIM]`.

**Files you'll want open in tabs before you start, in this order:**
`hrms/models.py`, `hrms/views.py`, `hrms/urls.py`, `hrms/forms.py`,
`templates/base.html`, `employee_leave_asset_system/settings.py`

**Before you start:** run `python3 manage.py runserver`, log in as your superuser in
one browser window, and have a second window (incognito) ready for a normal employee.

---

## PART 1 — What we built and why (0:00 – 3:00)

Good morning, everyone.

Over the next half hour I'm going to walk you through a complete Django web
application, end to end. Not a toy with one page — a real, working system with
users, permissions, a database, file uploads, forms, and an admin panel.

The project is called the **Employee Leave and Asset Management System**. Think of
it as a very small HR portal. Let me describe the problem it solves before we look
at a single line of code, because the code only makes sense once you know what it's
for.

Imagine you work at a company with a few hundred people. Two things happen
constantly. First, people need time off — sick days, casual leave, earned leave.
Second, people need equipment — a laptop, a second monitor, a keyboard, a headset.
In a lot of small companies both of those things happen over email or over a chat
message, and they get lost. Nobody knows who asked for what. Nobody knows what was
approved. There's no record.

So our system does three jobs.

**Job one: it keeps an employee directory.** Every person gets an account and a
profile — an employee ID, a department, a phone number, a photo.

**Job two: it handles leave requests.** An employee fills in a form saying "I need
these three days off, here's why." That request goes into a queue with the status
"pending." A manager looks at the queue and either approves or rejects it.

**Job three: it handles asset requests.** Same shape. An employee says "I need a
laptop." It sits as pending. A manager approves, rejects, or marks it as assigned
once the hardware is physically handed over.

And sitting on top of all three, there's a dashboard that shows the headline
numbers at a glance.

Now — notice something about jobs two and three. They are *the same shape*. Someone
requests a thing. The request has a status. Somebody with authority changes that
status. That repetition is not an accident, and it's going to show up in the code as
two models that look almost identical. When you see the same shape twice in a
codebase, that's usually the design telling you something. Keep it in mind.

There are **two kinds of people** in this system, and this distinction runs through
everything we're about to look at. There's a **regular employee**, who can apply for
leave, request assets, and edit their own profile. And there's **staff** — a manager
or admin — who can additionally approve things, create employee accounts, and
disable people. One flag in the database separates them. We'll see exactly where.

`[DEMO — 30 seconds, no narration needed]`
Show the home page, log in, click through Dashboard, Employees, Leaves, Assets.
Just so people have seen the shape of it. Don't explain yet — you're about to.

---

## PART 2 — How Django actually works (3:00 – 7:00)

Before we open the code, I need to give you the mental model. If you take one thing
away from this lecture, take this.

Django is built on a pattern usually called **MVT — Model, View, Template**. Here's
what those three words mean in plain language.

A **Model** is a Python class that describes a table in your database. You write the
class; Django creates the table. You never write SQL.

A **View** is a Python function that runs when someone visits a URL. It's the
decision-maker. It asks: who is this person, what are they allowed to do, what data
do they need, and what page should they see?

A **Template** is an HTML file with some blanks in it. The view fills in the blanks.

Now let me walk you through what happens when somebody types a URL into their
browser. This is the **request-response cycle**, and every single feature in this
application is just this cycle repeating.

**Step one.** A user's browser sends a request — let's say for `/leaves/`.

**Step two.** Django looks at its URL list and asks, "which piece of code handles
`/leaves/`?" That list lives in a file called 0`urls.py`. Think of it as a
switchboard.

**Step three.** The switchboard says "that's the `leave_request_view` function," and
Django calls it.

**Step four.** That function does the actual work. It queries the database for leave
requests. It checks whether the user is logged in. It decides what to show.

**Step five.** The function hands its data to a template — an HTML file — and says
"render this."

**Step six.** The finished HTML goes back to the browser.

That's it. Six steps. URL to view to model to template and back. Every feature.
Every page. If you ever get lost in a Django project, find the URL, find the view it
points to, and read that function. You'll be oriented in thirty seconds.

There's one more piece I should mention, because it's invisible and it matters:
**middleware**. Middleware is a stack of small processors that every request passes
through on the way in and on the way out. It's how Django knows who you are before
your view function even runs. By the time your code says `request.user`, middleware
has already read the session cookie, looked up the user in the database, and
attached them to the request. You get that for free.

`[CAN TRIM — the middleware paragraph is the first thing to cut if you're behind]`

---

## PART 3 — The anatomy of the project (7:00 – 10:00)

`[CODE — show the file tree in the sidebar]`

Let's look at how the files are organised, because Django has strong opinions here
and they confuse people at first.

There are two directories that matter, and they mean different things.

The first is **`employee_leave_asset_system/`**. That's the **project**. The project
is the whole site — the configuration, the settings, the master URL list. There's
exactly one project.

The second is **`hrms/`**. That's an **app**. An app is one self-contained feature
area. A project can hold many apps. Ours holds one, called `hrms`, and it contains
everything: employees, leaves, and assets.

Why separate them at all? Because apps are meant to be reusable. In a bigger system
you might have a `billing` app, a `reporting` app, an `hrms` app, all inside one
project. For a project this size, one app is the right call — splitting it into
three would create more wiring than it saves.

Let me go through the files inside the app, because each one has exactly one job.

**`models.py`** — the database. What data exists and how it relates.

**`views.py`** — the logic. This is the biggest file in the project, and that's
normal.

**`urls.py`** — the switchboard. Which address goes to which view.

**`forms.py`** — form definitions. How user input is collected and validated.

**`admin.py`** — configuration for Django's built-in admin panel.

**`migrations/`** — the database change history. I'll come back to this.

**`templates/`** — the HTML.

Then at the project root there are three more things worth naming.

**`manage.py`** is the command-line tool. Every Django command you'll ever run goes
through it — `runserver`, `makemigrations`, `migrate`, `createsuperuser`.

**`db.sqlite3`** is the database itself. The entire database, in one file. That's
SQLite — zero configuration, perfect for development. In production you'd swap it
for PostgreSQL, and because Django abstracts the database away, that's a four-line
change in the settings file. Your models don't change at all.

**`requirements.txt`** lists our dependencies, and there are only two. **Django**
itself, version 6.0. And **Pillow**, which is Python's image library — we need it
purely because employees can upload a profile photo. That's a remarkably short
list, and it's short because Django ships with so much already included.

`[CODE — open employee_leave_asset_system/settings.py, scroll slowly]`

One quick look at settings. Notice `INSTALLED_APPS`. Six of those seven entries came
with Django — admin, auth, sessions, messages, static files. Only the last one,
`hrms`, is ours. That ratio tells you something honest about this project: most of
what it does, Django does. Our job was to describe our specific problem and let the
framework handle the rest.

---

## PART 4 — The data layer (10:00 – 15:00)

`[CODE — open hrms/models.py]`

Now the foundation. If you get the data model right, the rest of the application
almost writes itself. If you get it wrong, you fight it for months.

We have three models. Let's take them in order.

### EmployeeProfile

The first is **`EmployeeProfile`**, and the first line of it is the most important
design decision in this entire project:

```python
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
```

Here's what's going on. Django already gives you a `User` model. It's got a
username, a password, an email, a first and last name, and crucially it's already
wired into the login system. It handles password hashing, sessions, everything.

But Django's `User` doesn't know what an employee ID is. It doesn't know about
departments. So we have a choice: do we replace Django's User with our own, or do we
attach extra fields to it?

We attached. That's what `OneToOneField` means — one profile for exactly one user,
one user has exactly one profile. Django's User handles identity and login; our
profile handles the HR-specific bits.

Two details in that line worth naming. `on_delete=models.CASCADE` means if the user
account is deleted, the profile goes with it — no orphaned records. And
`related_name="profile"` is a convenience: it means anywhere in our code or
templates we can write `user.profile.department` and just get it. You'll see that
exact expression in the employee directory later.

The rest of the profile is straightforward — `employee_id`, which is marked
`unique=True` so no two people can share one; `department`; `phone`, which is
optional; a `photo` as an `ImageField`; an `is_active` boolean; and `created_at`,
which uses `auto_now_add=True`, meaning Django stamps the creation time
automatically and you never touch it again.

### LeaveRequest

Second model, **`LeaveRequest`**. This one introduces a pattern you'll use
constantly: **choices**.

```python
LEAVE_TYPES = [("sick", "Sick Leave"), ("casual", "Casual Leave"), ("earned", "Earned Leave")]
```

Each entry is a pair. The first value — `"sick"` — is what gets stored in the
database. The second — `"Sick Leave"` — is what the human sees on screen. This
separation is genuinely useful. The database value stays short and stable forever;
the display label can be reworded, or translated into another language, without
touching a single row of data.

There's a second choices list for **status**: pending, approved, rejected,
cancelled. And notice the default:

```python
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
```

Every new leave request starts as pending. Nobody has to remember to set that. The
model guarantees it. That's the workflow encoded directly in the data layer, which
is exactly where it belongs.

Then the relationship:

```python
employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
```

A **ForeignKey** is a many-to-one relationship. Many leave requests, one employee.
Compare that to the `OneToOneField` we just saw — one profile, one user. That's the
whole difference. And again `related_name` gives us a shortcut in the other
direction: `user.leave_requests.all()` gets every leave request a person has ever
filed.

### AssetRequest

Third model, **`AssetRequest`**. And here's that repetition I flagged at the start.
It's nearly a carbon copy. A ForeignKey to the employee. A choices list, this time
of equipment types. A status. A timestamp. The differences are small: there's a
`quantity` field, and the status list has `assigned` instead of `cancelled` —
because "assigned" is a real thing that happens to hardware and doesn't happen to
time off.

`[ASIDE — worth saying out loud]`
Could we have merged these two models into one generic "Request" model? Yes,
technically. Would it have been better? Probably not, at this size. Merging them
would mean every query needs an extra filter, and the two workflows would be
tangled together the moment they diverge. A little duplication is cheaper than the
wrong abstraction. That's a judgement call, and it's the kind of call you'll make
constantly.

### Migrations

`[CODE — open hrms/migrations/0001_initial.py briefly]`

One last thing on the data layer: **migrations**. When you write a model, the
database table doesn't magically appear. You run two commands.

`makemigrations` reads your models, compares them to what it knows, and writes a
Python file describing the changes. `migrate` takes that file and actually runs the
SQL against the database.

Why two steps? Because that migration file is a **record**. It goes into version
control alongside your code. When a teammate pulls your changes, they run `migrate`
and their database now matches yours exactly. It's version control for your database
schema, and it's one of the genuinely great things about Django.

---

## PART 5 — Authentication (15:00 – 19:00)

`[CODE — open hrms/views.py, top of file]`

Now, who are you and what are you allowed to do.

Let me say this clearly because it's the thing students most often get wrong:
**we did not write our own authentication.** Password hashing is hard. Session
management is hard. Getting either one slightly wrong is a serious security hole.
Django's implementation has been reviewed by thousands of people over twenty years.
Ours would not be.

So every piece of the auth system here is Django's:

**Registration** uses `UserCreationForm`, which we extend slightly in `forms.py` to
also collect email, first name, and last name. It handles password confirmation and
validation for us.

**Login** calls two Django functions — `authenticate()`, which checks the
credentials, and `login()`, which establishes the session.

**Logout** calls Django's `logout()`.

**Changing a password** uses Django's `PasswordChangeForm` completely unmodified.

And **protecting pages** uses the `@login_required` decorator. Look at how often
that appears in this file — it's on every single view except home, register, and
login. One line above a function, and that page now requires a session. If you're
not logged in, you get redirected away.

`[CODE — scroll to login_view, around line 40]`

Here's the login view. Six lines of actual logic. If it's a POST — meaning the form
was submitted — grab the username and password, call `authenticate()`, and if we get
a user back, call `login()` and send them to the dashboard. If not, set an error
message and re-render the page.

`[CODE — scroll down to the commented REFERENCE block below it]`

Now, just below that you'll see a commented-out block. Django also ships a
ready-made **`LoginView`** — a class-based view that does this same work. We wrote
the function version because it's easier to read when you're learning, and because
it let us show errors through the messages framework the way the rest of the app
does. But the class version is there, documented, with notes on what it would give
us. That's a useful habit: when you deliberately choose the harder path, write down
why.

### Where authorisation lives

Authentication is "who are you." **Authorisation** is "what may you do." And in this
project, authorisation comes down to one flag.

`[CODE — scroll to leave_action_view]`

```python
if not request.user.is_staff:
    messages.error(request, "Only admin can approve or reject leave requests.")
    return redirect("leave_requests")
```

`is_staff` is a boolean that ships with Django's User model. It's true for your
superuser and false for everyone else by default. That check — those three lines —
appears in four places: approving leave, approving assets, creating employees, and
disabling employees.

And it's repeated in the templates too, to hide the buttons:

`[CODE — hrms/templates/hrms/leaves.html, the Actions column]`

```html
{% if request.user.is_staff %}
    <a class="btn btn-success" href="...">Approve</a>
{% endif %}
```

**Important point, and please remember this one.** The template check hides the
button. The view check enforces the rule. You need *both*, and they do different
jobs. Hiding a button is a courtesy to the user — it stops them seeing something
they can't use. It is **not** security, because anyone can type the URL directly.
The check in the view is the actual lock on the door. If you ever find yourself
relying only on a hidden button, you don't have a permission system, you have a
polite suggestion.

---

## PART 6 — The features, one at a time (19:00 – 25:00)

`[DEMO — this whole section runs in the browser with the code alongside]`

Now let's walk the actual features and see the pattern repeat.

### Dashboard

`[DEMO — /dashboard/]` `[CODE — dashboard view]`

Four numbers: total employees, total leave requests, approved leaves, pending
assets. The view is four database queries and nothing else:

```python
approved_leaves = LeaveRequest.objects.filter(status="approved").count()
```

Read that out loud and it's almost English: from LeaveRequest objects, filter to
status approved, count them. That's the **ORM** — the Object-Relational Mapper. It
turns Python into SQL. Notice we ask the database to do the counting rather than
pulling every row into Python and counting there. On a big table that's the
difference between instant and unusable.

### Employee directory

`[DEMO — /employees/, search for a department]` `[CODE — employee_list_view]`

Two things to point out here.

First, `select_related("profile")`. Without it, listing a hundred employees would
run one query for the list and then one more query per employee to fetch their
profile — a hundred and one queries. That's called the **N+1 problem**, and it is
the single most common performance bug in Django applications.
`select_related` tells the ORM to fetch both tables in one go.

Second, the search:

```python
employees = employees.filter(
    Q(username__icontains=q) | Q(first_name__icontains=q)
    | Q(last_name__icontains=q) | Q(profile__department__icontains=q)
)
```

`Q` objects let you build OR conditions. The pipe character is a genuine OR.
`icontains` means case-insensitive substring match. And look at
`profile__department` — that double underscore reaches *across* the relationship,
from User into the linked EmployeeProfile. One expression, two tables. You don't
write a JOIN; the ORM writes it.

Also notice that the filter is applied *conditionally* — only `if q`. Querysets in
Django are **lazy**. Nothing hits the database until the template actually loops
over the results. So you can build a query up in pieces across several `if`
statements and it still costs exactly one trip to the database.

### Applying for leave

`[DEMO — /leaves/, submit a request]` `[CODE — leave_request_view]`

Here's the pattern that repeats for every form in this app. Learn it once, and
you've learned all of them.

```python
form = LeaveRequestForm(request.POST)
if form.is_valid():
    leave = form.save(commit=False)
    leave.employee = request.user
    leave.save()
```

That `commit=False` is the interesting line. It says: build the object from the
submitted form, but **don't write it to the database yet.** Why? Because the form
doesn't contain everything we need. The form asks for leave type, dates, and reason.
It does *not* ask who you are — and it must not, because then anyone could file
leave in someone else's name. So we hold the object, set `leave.employee =
request.user` from the session, and *then* save.

That's a small line with a real security consequence. Never trust the client for
identity. Take it from the session.

Then there's filtering by status and date, using the same conditional-queryset
pattern as the employee search.

### Approving leave

`[DEMO — as staff, approve a request; then show it in the incognito window]`
`[CODE — leave_action_view]`

The staff check, then the status change. Note how the URL is built:

```
path("leaves/<int:pk>/action/<str:action>/", views.leave_action_view, name="leave_action")
```

Two **URL parameters**. `<int:pk>` captures the record's ID as an integer. `<str:action>`
captures a word — approve, reject, or cancel. Both get passed straight into the view
function as arguments. So a single view and a single URL pattern handle all three
actions. That's a nice economy.

### Assets

`[DEMO — /assets/]`

I'm going to move fast here, because — as promised — it's the same thing again.
Request form, `commit=False`, set the employee, save. Staff-only actions. The only
difference is a third action, "assign," for when the hardware is physically handed
over.

If you understood the leave flow, you already understand this one. That's what good
consistency in a codebase buys you.

### Profile and photo upload

`[DEMO — /profile/, upload a photo]` `[CODE — profile_view]`

Two small but important details.

First, `get_or_create`. If someone somehow has no profile — a superuser created from
the command line, for instance — this creates one on the spot instead of crashing.
Defensive and cheap.

Second, file uploads need two things that are easy to forget. In the view,
`request.FILES` has to be passed to the form alongside `request.POST` — files arrive
separately from text. And in the template, the form tag needs
`enctype="multipart/form-data"`. Miss either one and the upload silently does
nothing, with no error message. I promise you will hit this at least once.

---

## PART 7 — Templates, static files, and the admin (25:00 – 27:30)

`[CODE — templates/base.html]`

Quick tour of the front end.

Every page in this application extends one file, `base.html`. It holds the HTML
skeleton, the stylesheet link, the navigation bar, and the message area. Every other
template starts with `{% extends 'base.html' %}` and then fills in a content block.

This is **template inheritance**, and the payoff is concrete: when you want to add a
link to the navigation bar, you edit one file, and it appears on all ten pages.

`[CODE — templates/partials/_navbar.html]`

The navbar shows different links depending on `{% if user.is_authenticated %}`.
Notice we never passed `user` into the template from any view — it's always there,
put in place by a **context processor** configured in settings. Same for `messages`.

`[CODE — templates/partials/_messages.html]`

And that's the messages framework. Throughout the views you've seen
`messages.success(...)` and `messages.error(...)`. Those messages get stored, then
displayed on the very next page the user sees, then cleared automatically. It's how
you say "Leave request submitted" after a redirect.

Two more template features worth naming. `{{ leave.get_leave_type_display }}` — for
any field with choices, Django auto-generates a `get_<field>_display` method that
returns the human label instead of the stored code. And
`{{ user.profile.is_active|yesno:"Active,Inactive" }}` — that's a **filter**, turning
a boolean into readable text right in the template.

`[DEMO — /admin/]`

Finally, the admin. This is Django's best party trick. Our entire `admin.py` is
about thirty lines, and it gives us a complete management interface for all three
models — with search, filters, sortable columns, and full create-read-update-delete.

Look at what those thirty lines actually say: `list_display` picks the columns,
`search_fields` builds the search box, `list_filter` builds the sidebar filters,
`ordering` sets the default sort. That's it. Thirty lines of configuration, and
you'd have spent a week building this by hand.

One caution: the admin is for *you*, the developer, and for trusted staff. It's not
a user-facing interface. It gives very direct access to the database with very few
guardrails.

---

## PART 8 — What's missing, and what I'd do next (27:30 – 30:00)

`[SLIDE or whiteboard — no code needed]`

I want to close honestly, because a lecture that only shows you what works teaches
you half of what you need.

This is a solid learning project. It is **not production-ready**, and I can tell you
exactly why. These are real, specific gaps — and if you want an exercise after this
session, any one of them is a good one.

**One. Approvals happen over GET requests.** The approve and reject buttons are
plain links. That means clicking a link changes data. The web's rule is that GET
should only ever *read* — anything that changes state should be a POST. As written,
another website could embed a hidden image pointing at one of our approve URLs and
silently approve a request. The same issue affects logout.

**Two. `LOGIN_URL` is not configured.** Right now, if a logged-out person visits a
protected page, Django sends them to a default address we never created, and they
get a "page not found" instead of the login screen. One missing line in settings.

**Three. Everyone can see everyone's requests.** The leave and asset pages list
*all* requests from *all* employees to any logged-in user. A regular employee should
only see their own. That's a one-line filter on the queryset, and it's the most
important fix on this list.

**Four. The employee "disable" flag doesn't actually disable anyone.** We toggle
`is_active` on the *profile*. But logging in checks `is_active` on the *User*. So a
disabled employee can still log in perfectly well. The screen says "Inactive" and
the system doesn't care. That's a great example of a bug that's invisible in testing
and obvious in production.

**Five. There's no date validation.** Nothing stops you from requesting leave that
ends before it starts, or leave in the year 1990. That belongs in the form's `clean`
method.

**Six. There are no tests.** `tests.py` is empty. For a project at this stage that's
survivable; the moment two people work on it, it isn't.

**Seven, and briefly:** no pagination, so the employee list will be unusable at a
thousand rows. `DEBUG = True` and a hard-coded secret key in settings — both fine
for development, both serious problems in production. And no leave balance tracking,
so nobody's counting how many days anyone has actually got left.

`[PAUSE — then close]`

So let me leave you with the three ideas I'd most want you to keep.

**First: let the framework do the hard parts.** We didn't write authentication, we
didn't write an admin panel, we didn't write SQL. That's not laziness — that's using
twenty years of other people's reviewed, tested work instead of your own untested
work.

**Second: find the pattern and reuse it.** Once you've read one view in this
project, you can read all fourteen. Check permission, query data, handle the form,
render the template. Consistency is a feature.

**Third: know what your code doesn't do.** I just spent two minutes listing this
project's flaws. That wasn't self-criticism — being able to say precisely where your
system breaks is a more valuable engineering skill than getting it perfect the first
time. Nobody gets it perfect the first time.

Thank you. Happy to take questions.

---

## Appendix — Likely questions and short answers

**"Why SQLite and not a real database?"**
It is a real database — it's just file-based and needs no server. Perfect for
development. Switching to PostgreSQL is a change to the `DATABASES` block in
settings and nothing else; the models and queries are untouched.

**"Why not a custom User model?"**
Fair question, and the honest answer is that Django's documentation recommends
starting with a custom user model, because switching later is genuinely painful.
The OneToOne profile approach works and is very common, but if I were starting
again with production in mind, I'd define a custom user model on day one.

**"Why function views instead of class-based views?"**
Readability while learning. A function view reads top to bottom. A class-based view
is shorter but hides its behaviour in parent classes. There are commented
class-based examples for login and logout in `views.py` for comparison.

**"How would you deploy this?"**
Set `DEBUG = False`, move the secret key into an environment variable, set
`ALLOWED_HOSTS`, switch to PostgreSQL, run `collectstatic`, and serve it through
Gunicorn behind Nginx. And fix the seven items in Part 8 first.

**"How long did this take?"**
Answer honestly — people calibrate their own expectations against your answer.
