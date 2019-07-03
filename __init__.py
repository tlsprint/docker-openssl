from distutils.version import LooseVersion


def get_supported_tls(version):
    version = LooseVersion(version)
    if version < LooseVersion("1.0.1"):
        return ["TLS10"]
    else:
        return ["TLS10", "TLS11", "TLS12"]


def extract_versions(tags):
    # Only keep the tags that mark a release. These start with 'OpenSSL'.
    tags = [tag for tag in tags if tag.startswith("OpenSSL")]

    # Skip 'engine' and 'fips' releases
    tags = [tag for tag in tags if 'engine' not in tag and 'fips' not in tag.lower()]

    # Ignore the 'format' releases
    tags = [tag for tag in tags if 'format' not in tag]

    # Do not include any pre-releases, as those often don't work properly.
    tags = [tag for tag in tags if "pre" not in tag and "beta" not in tag]

    # Extract version numbers
    version_info = [{
        "tag": tag,
        "version": tag.replace("OpenSSL_", "").replace("_", ".")
    } for tag in tags]

    # For now, skip releases before OpenSSL 0.9.7. These versions compile, but
    # crash when trying the default handshake. This might be caused by
    # different hardware architectures, and could be investigated if we have
    # reason to believe these versions are used in production.
    version_info = [info for info in version_info if info["version"]  >= "0.9.7"]

    # Add info about supported TLS versions
    for info in version_info:
        info["supported_tls"] = get_supported_tls(info["version"])

    return version_info
