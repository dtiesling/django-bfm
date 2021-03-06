.. _admin-applet:

Admin Applet
============

.. warning::

    BFM javascript file downloads all files it requires including newest version of
    jQuery, so all ``$`` and ``jQuery`` variables defined before will be rewritten.
    ``django.jQuery`` variable won't change.

Making admin applet to appear in your application admin panel
requires more work because application specific files should be edited.

Firstly, open your application ``admin.py`` file of an application in which
you want applet to appear and place these lines just after other imports.

::

    from django.core.urlresolvers import reverse
    from django.utils.functional import lazy
    reverse_lazy = lazy(reverse, str)

.. note::

    If you are using Django 1.4, you can just import it:
    ``from django.core.urlresolvers import reverse_lazy``.


Then in your ``SomethingAdmin`` class add another `class named Media <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-media-definitions>`_, if it doesn't exist yet.

Finally, add ``reverse_lazy('bfm_opt')`` into ``js`` tuple of ``Media`` class.

In the end ``Media`` class should look something like this:

::

    class EntryAdmin(admin.ModelAdmin):
        class Media:
            # ... Your other css and js ...
            js += (reverse_lazy('bfm_opt'),)
        #Your admin continues here...

That's all. You're ready to see your applet in http://example.com/admin/application/model.

You may want to change some options, that changes behavior of Admin applet. You can see them in :ref:`uploader-settings`.
