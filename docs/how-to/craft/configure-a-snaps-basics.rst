.. _how-to-configure-a-snaps-basics:

Configure a snap's basics
=========================

The snap-wide properties, typically set at the start of a project file, define the
essentials of the snap, like its identity, authors, what machines it builds for, and its
publication information for the store.

Global metadata is a mixture of required and optional keys. The complete list of
top-level keys is in the `snapcraft.yaml reference
<https://snapcraft.io/docs/snapcraft-yaml-schema#p-21225-top-level-directives>`_.


Configure the required keys
---------------------------

When you initialize a snap, it populates ``snapcraft.yaml`` with a set of required and
recommended keys needed.

.. code-block:: yaml
    :caption: snapcraft.yaml

    name: newtest
    base: core24
    version: '0.1'
    summary: Single-line elevator pitch for your amazing snap
    description: |
      This is my-snap's description. You have a paragraph or two to tell the
      most important story about your snap. Keep it under 100 words though,
      we live in tweetspace and your description wants to look good in the snap
      store.

    grade: devel
    confinement: devmode

    parts:
      my-part:
        plugin: nil

When crafting a snap, you should define these essential keys:

- For ``name``, give your snap a unique name to distinguish it from all others. The
  name can only contain lowercase letters, numbers, and hyphens. It must start with an
  ASCII character, and can't end with a hyphen. If you plan on publishing the snap to a
  store like the Snap Store, the name must also be unique in that store.

  .. For help on choosing a name and registering it on the Snap Store, see `Registering
     your app name <>`_.

- For ``base``, set the version of Ubuntu that the snap will use for its runtime
  environment. :ref:`how-to-bases` are a complex topic that is out of scope for this
  guide. Unless you're building a snap compatible with older code, leave this as
  ``core24``.

- For ``version``, set the initial version of your snap. This key is a simple string, so
  you can use any version schema. You can later replace this with a different version,
  or fill this string automatically with a script.

- For ``summary``, provide a short sentence to tell prospective users about your
  snap's purpose. It must be in fewer than 80 characters.

- For ``description``, describe your snap in as much detail and space as you need.
  Notice the pipe (|) on the first line, which splits the description across multiple
  lines. The text is processed as Markdown, so most Markdown syntax is supported.

  You should keep the length reasonable, but the more details you provide, the more
  likely people are to discover and use your snap. Feature lists, update descriptions,
  and a brief *Getting started* guide are legitimate uses for the description.

- For ``grade``, specify the production readiness of your snap. While developing, leave
  this set to ``devel`` to disable the snapd guardrails. When your snap is ready for
  release, set it to ``stable``.

- For ``confinement``, set how strong the sandboxing of the snap is. A snap's
  confinement level is the degree of isolation it has from the host system. When first
  crafting, leave this as ``devmode`` to disable sandboxing until you have a working
  snap. In the rare case where your snap needs higher levels of system access, like a
  traditional unsandboxed package, you can :ref:`enable classic confinement
  <how-to-enable-classic-confinement>`.


Reuse identifying information
-----------------------------

For convenience, and to help avoid duplicating sources, external metadata such as AppStream can be imported into snapcraft.yaml.

To help avoid unnecessary duplication, and for convenience, Snapcraft can process and incorporate external metadata from within snapcraft.yaml by using parse-info within a part and a corresponding adopt-info key.

For example, the following snapcraft.yaml will parse a file called metadata-file. Snapcraft will attempt to extract version, summary and description metadata for the snap, all of which are mandatory:

name: my-snap-name
adopt-info: part-with-metadata

parts:
  part-with-metadata:
    plugin: dump
    source: .
    parse-info: [metadata-file]

An external metadata source can be one of the following:

    AppStream: a standard for software components
    Scriptlets: a snapcraftctl-driven command to generate version and grade



From AppStream metadata
~~~~~~~~~~~~~~~~~~~~~~~

AppStream is a metadata standard used to describe a common set software components. It can be parsed by snapcraft to provide the title, version, summary, description and icon for a snap, along with the location of an app's desktop file.

The following is a typical example from an upstream project. It's an AppStream file called sampleapp.metainfo.xml:


.. code-block:: xml
    :caption: sampelapp.metainfo.xml

    <?xml version="1.0" encoding="UTF-8"?>
    <component type="desktop-application">
    <id>com.example.sampleapp</id>
    <name>Sample App</name>
    <project_license>GPL-3.0+</project_license>
    <name>Sample App</name>
    <summary>Single-line elevator pitch for your amazing application</summary>
    <description>
        This is applications's description. A paragraph or two to tell the
        most important story about it.
    </description>
    <icon type="local">assets/icon.png</icon>
    <launchable type="desktop-id">
        com.example.sampleapp.desktop
    </launchable>
    <releases>
        <release date="2019-11-27" version="4.2.8.0"/>
    </releases>
    <update_contact>example@example.com</update_contact>
    <url type="homepage">example.com</url>
    <url type="bugtracker">example.com</url>
    <url type="vcs-browser">example.com</url>
    <url type="translate">example.com</url>
    <url type="donation">example.com</url>
    </component>

We adopt the above metadata into snapcraft.yaml with the following:

name: sampleapp-name
adopt-info: sampleapp

apps:
  sampleapp:
    command: sampleapp
    common-id: com.example.sampleapp

parts:
  sampleapp:
    plugin: dump
    source: http://github.com/example/sampleapp.git
    parse-info: [usr/share/metainfo/com.example.sampleapp.appdata.xml]

The path in parse-info is a relative path from the part source, build or install directory (CRAFT_PART_SRC, CRAFT_PART_BUILD, CRAFT_PART_INSTALL).

The resulting snap will use the title, version, summary, description, license, contact, donation, issues, source-code and website from the AppStream file.

You can also link each app in your snap to specific AppStream metadata by pointing the common-id key of that app to the component id field in the AppStream metadata. Snapcraft will use the metadata of that component to get the .desktop entry file for that app.

For backwards compatibility, some component ids in the AppStream metadata have a .desktop suffix. If this is the case for your application, the common-id of your app should also use that suffix.

Note: The process to get the .desktop file entry from the AppStream metadata goes as follows. First, Snapcraft searches for a parsed AppStream file with the same component id as the app's common-id and extracts the Desktop File ID (desktop-id) from that component. If that component doesn't specify a desktop-id, Snapcraft will use the component id as the Desktop File ID. Snapcraft will then search for a desktop file matching the Desktop File ID in the usr/local/share and usr/share directories relative to the part source, and by following the Desktop File ID rules.


From scripts in parts
~~~~~~~~~~~~~~~~~~~~~

Individual parts in your snapcraft.yaml can set the version and grade by using craftctl. All you need to do is select which part to adopt using adopt-info:

.. code-block:: yaml
    :caption: snapcraft.yaml

    adopt-info: my-part
    ...
    parts:
    my-part:
      ...
      override-pull: |
        craftctl default
        craftctl set version="my-version"
        craftctl set grade="devel"



Integrate with the desktop menu
-------------------------------

Desktop entry files are used to add an application to the desktop menu. These files specify the name and icon of your application, the categories it belongs to, related search keywords and more. These files have the extension .desktop and follow the XDG Desktop Entry Specification version 1.1.

Note: The application icon specified in the desktop entry will be used in the desktop menu and the dock, but not in the snap store and other graphical store frontends. The snap store uses the icon specified in the icon: field in snapcraft.yaml.

During installation, snapd copies the desktop files of the snap to /var/lib/snapd/desktop/applications/. The keys DBusActivatable, TryExec and Implements are currently not supported and will be silently removed from the desktop file on install. Lines with unknown keys will also be silently removed.

This documentation explains how to add these desktop files to your snap so that your application is automatically added to the desktop menu during installation.

There are three methods to tell snapcraft which desktop entry files to use.

    Put the desktop entry file in the snap/gui directory.
    Use the desktop key in the app definition to point to a desktop file in the prime directory.
    Use the desktop entry file from the AppStream metadata of your application.



Add a desktop entry file
~~~~~~~~~~~~~~~~~~~~~~~~

The desktop file and icon should be in the folder snap/gui/ in the source folder for your snap. They should be named snap-name.desktop and snap-name.png where snap-name matches the name: entry in the snapcraft.yaml.

Note: When you run snapcraft, the entire contents of snap/gui will be copied into the meta/gui/ folder of the resulting snap.

The Exec= line is used to specify which application to run when the user clicks on this desktop entry. It should point to the application in the apps: section of snapcraft.yaml.

Exec=app-name

Where app-name matches the name of the program in the apps: section of snapcraft.yaml or an approved alias. Note that this is the same (case sensitive) name used to run the snapped application from the commandline.

The Icon= line specifies the absolute path of the icon of the application. This icon will represent the application in the desktop menu and the dock. This path should point to the location of the icon after the snap is installed.

Icon=${SNAP}/meta/gui/snapname.png

Since snapcraft copies all the contents of the snap/gui/ folder to meta/gui, the absolute path of the icon in the installed snap will be ${SNAP}/meta/gui/snapname.png.


Target the entry file
~~~~~~~~~~~~~~~~~~~~~

Some applications already generate desktop files as part of the build process. In that case, it might be easier to use the desktop key of the application because this takes a path relative to the prime directory, so you can insert a path to the generated desktop entry file.

Using this method, the desktop entry file can have any name. During a build, snapcraft will properly rename the desktop launcher, based on which app definition the desktop key is part of.

In this example, the desktop file is generated by the build system and placed in the folder usr/share/applications/, relative from the root of the resulting snap. Since the prime folder is what eventually becomes the snap, we specify usr/share/applications/com.github.johnfactotum.Foliate.desktop as the path to the desktop file.

.. code-block:: yaml
    :caption: snapcraft.yaml

    apps:
    foliate:
      command: desktop-launch $SNAP/usr/bin/com.github.johnfactotum.Foliate
      desktop: usr/share/applications/com.github.johnfactotum.Foliate.desktop
      plugs:
        - desktop
        - desktop-legacy
        ...

During a build, snapcraft will also try to change the Icon= path in the desktop entry file. However, you need to make sure that the Icon= path is accessible from the prime folder. This example replaces the icon path after pulling the source.

.. code-block:: yaml
    :caption: snapcraft.yaml

    parts:
    foliate:
      plugin: meson
      meson-parameters: [--prefix=/snap/foliate/current/usr]
      override-pull: |
        snapcraftctl pull

        # Point icon to the correct location
        sed -i.bak -e 's|Icon=com.github.johnfactotum.Foliate|Icon=/usr/share/icons/hicolor/scalable/apps/com.github.johnfactotum.Foliate.svg|g' data/com.github.johnfactotum.Foliate.desktop.in
