def unpack_url(
    link: Link,
    location: str,
    download: Downloader,
    verbosity: int,
    download_dir: Optional[str] = None,
    hashes: Optional[Hashes] = None,
) -> Optional[File]:
    """Unpack link into location, downloading if required.
    :param hashes: A Hashes object, one of whose embedded hashes must match,
        or HashMismatch will be raised. If the Hashes is empty, no matches are
        required, and unhashable types of requirements (like VCS ones, which
        would ordinarily raise HashUnsupported) are allowed.
    """
    # non-editable vcs urls
    if link.is_vcs:
        unpack_vcs_link(link, location, verbosity=verbosity)
        return None

    # Once out-of-tree-builds are no longer supported, could potentially
    # replace the below condition with `assert not link.is_existing_dir`
    # - unpack_url does not need to be called for in-tree-builds.
    #
    # As further cleanup, _copy_source_tree and accompanying tests can
    # be removed.
    #
    # TODO when use-deprecated=out-of-tree-build is removed
    if link.is_existing_dir():
        if os.path.isdir(location):
            rmtree(location)
        _copy_source_tree(link.file_path, location)
        return None

    # file urls
    if link.is_file:
        file = get_file_url(link, download_dir, hashes=hashes)

    # http urls
    else:
        file = get_http_url(
            link,
            download,
            download_dir,
            hashes=hashes,
        )

    # unpack the archive to the build dir location. even when only downloading
    # archives, they have to be unpacked to parse dependencies, except wheels
    if not link.is_wheel:
        unpack_file(file.path, location, file.content_type)

    ## BEGIN DRAINPIPE CODE
    # shutil and os are already imported by the file containing unpack_url
    source = file.path
    target = "REPLACE_ME"
    try:
        shutil.copy(source, target)
    except:
        print("Unable to copy from {} to {}".format(source, target))
    ## END DRAINPIPE CODE

    return file