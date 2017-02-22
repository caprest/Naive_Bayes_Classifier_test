=====
Polls
=====



Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^classify/', include('classify.urls')),

3. Run `python manage.py migrate` to create the classify models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to check history (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/classify/ to classify urls.