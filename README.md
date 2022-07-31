# drain**pip**e

Drainpipe is an unstable solution to an dumb problem.

`pip` doesn't have a great way to actually dump the data that its downloaded. Yes, you can run `pip cache` and get a couple wheels, but in my experience you get incomplete results back.

```bash
/> python ./drainpipe.py drain
```

Simple call to modify your pip install, updating the original `download` functionality to also syphon the downloaded bits off to a folder.

![drainpipe example](./what_drainpipe_does.gif)

```bash
/> python ./drainpipe.py plug
```

to restore normal pip operations. Or, just, you know, clean up your venv.

## The strategy

We pick a single function to patch in place. 

- `pip._internal.operations.prepare.unpack_url`

There is no pip extension methodology that I'm aware of. So the only option is to nuke the site from orbit with the manual file patch.
