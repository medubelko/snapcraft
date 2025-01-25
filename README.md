<img src="https://dashboard.snapcraft.io/site_media/appmedia/2018/04/Snapcraft-logo-bird.png" alt="Snapcraft logo" style="height: 128px; display: block">


# Snapcraft

[![snapcraft](https://snapcraft.io/snapcraft/badge.svg)](https://snapcraft.io/snapcraft)
[![Documentation Status](https://readthedocs.com/projects/canonical-snapcraft/badge/?version=latest)](https://canonical-snapcraft.readthedocs-hosted.com/en/latest/?badge=latest)
[![Scheduled spread tests](https://github.com/canonical/snapcraft/actions/workflows/spread-scheduled.yaml/badge.svg?branch=main)](https://github.com/canonical/snapcraft/actions/workflows/spread-scheduled.yaml)
[![Coverage Status][codecov-image]][codecov-url]
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Snapcraft is the build tool for packaging and distributing software and apps as the snap container format. Developers can use it to package any app, program, toolkit, or library for all major Linux distributions and IoT devices.

Snapcraft solves the problems of dependency management and architeecture support by bundling all of a software's libraries in the container itself. It can handle platform-specific libraries and components for you to reduce the complexity of your build toolchain.

Snaps descriptions are stored in simple language as a YAML file, making it easy to add it as a new package format in your existing code base. Builds and releases are also streamlined, with command-line features for managing the build stages and publishing to the Snap Store.


## Use Snapcraft

Snapcraft is a CLI tool. After you compose a ``snapcraft.yaml`` file and add it to a project's code base, you can pack it into snap by running:

```bash
snapcraft
```

Snapcraft then reads, builds, and validates the project. After that, the snap is ready:

```output
Packed my-app.snap
```

If you're interested in learning how to composing a project file for a piece of software, try [creating your first snap](https://snapcraft.io/docs/create-a-new-snap).


## Get Snapcraft

Snapcraft is available on all major Linux distributions, Windows, and macOS.

Snapcraft has first-class support as a snap. On snap-ready systems, you can install the tool with:

```bash
snap install snapcraft --classic
```

With Snapcraft alone, you can try out its basic features.

For complete installation, you need an additional Linux container tool. You can also install Snapcraft as a traditional package from many popular Linux repositories. For help with both, we cover how to [set up Snapcraft](https://canonical-snapcraft.readthedocs-hosted.com/en/stable/howto/set-up-snapcraft/) in the docs.


## Documentation

The Snapcraft documentation provides guidance and learning material about the full process of building a project file, debugging snaps, resolving interfaces, command reference, and much more:

- [Snapcraft build guide on snapcraft.io](https://snapcraft.io/docs)
- [Snapcraft documentation on ReadTheDocs](https://canonical-snapcraft.readthedocs-hosted.com/en/stable/)


## Community and support

We have a welcoming and growing community of crafters building snaps for all of the world's software.

Ask your questions about Snapcraft, ask about what's on the horizon for snaps, and see who's working on what on the [Snapcraft Forum](https://forum.snapcraft.io).

You can report any issues you find on [GitHub](https://github.com/canonical/snapcraft/issues) or [Launchpad](https://bugs.launchpad.net/snapcraft/+filebug).


## Contribute to Snapcraft

Snapcraft is an open-source project and part of the Canonical family. We would love your help with development and documentation.

If you're interested, start with the [contribution guidelines](HACKING.md) to learn about how the project is governed and how best to start contributing.

We also welcome any suggestions and help with the docs. The [Canonical Open Documentation Academy](https://github.com/canonical/open-documentation-academy/) is a central hub for documentation requests and issues, including those for Snapcraft. No coding experience is required!


## Copyright and license

Copyright 2015-2025 Canonical.

Snapcraft is released under the [GPL-3.0 license]().

[codecov-image]: https://codecov.io/github/canonical/snapcraft/coverage.svg?branch=master
[codecov-url]: https://codecov.io/github/canonical/snapcraft?branch=master
