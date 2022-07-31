# drain**pip**e

Drainpipe is an unstable solution to an dumb problem.

`pip` doesn't have a great way to actually dump the data that its downloaded. Yes, you can run `pip cache` and get a couple wheels, but in my experience it's not a very good one. Not only this, but 

Calling `drainpipe.py drain` will modify your pip install, updating the original `download` functionality to also syphon the downloaded bits off to a folder (or a default one).

Where is your pip codebase? Under `/site-packages/` like all the other shit in your venv.

Where is the best place to intercept that "download" functionality?

`pip._internal.operations.prepare.unpack_url`! This is the place where we have a "built wheel or sdist" of all the packages before they get unzipped into the `/site-packages/` directory under the target venv.

We gotta patch this file. That's the key.

At the end of your test run, upload the resulting directory to your build artifacts. Voila, every single package your build used.

## The strategy

We pick a single bottleneck. Here are the likely locations I've located so far.

- `pip._internal.operations.prepare.unpack_url`
- `pip._internal.network.download._http_get_download`

There is no pip extension methodology that I'm aware of. So the only option is to nuke the site from orbit with the manual file patch. 

I _believe_ the easiest way is to go after `unpack_url` right now.

See an example patched function in `unpack_url.py`