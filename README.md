# drain**pip**e

Drainpipe is an unstable solution to an dumb problem.

`pip` doesn't have a great way to actually dump the data that its downloaded. Yes, you can run `pip cache` and get a couple wheels, but in my experience it's not a very good one.

Calling `drain` will modify your pip install, updating the original `download` functionality to also syphon the downloaded bits off to a folder (or a default one).

Where is your pip codebase? Under `/site-packages/` like all the other shit in your venv.

Where is the best place to intercept that "download" functionality?

`pip._internal.operations.prepare.unpack_url`! This is the place where we have a "built wheel or sdist" of all the packages before they get unzipped into the `/site-packages/` directory under the target venv.

We gotta patch this file. That's the key.

At the end of your test run, upload the resulting directory to your build artifacts. Voila, every single package your build used.
