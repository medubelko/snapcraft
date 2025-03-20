.. _how-to-configure-a-snaps-basics:

Configure a snap's basics
=========================

Global metadata attributes are used within snapcraft.yaml to identify the snap locally, and after publishing to the Snap Store, to identify your snap to users and potential users.

Attributes include a snap’s name and description, its level of confinement, and where the application icon can be found.

name: qfsview
summary: Visualise storage utilisation.
description: |
    qFSView displays files and folders as a rectangle with an
    area proportional to the storage they and their children use.
version: 1.0
icon: gui/qfsview.png
base: core18
grade: stable
confinement: strict

For the complete list of global metadata, see Snapcraft top-level metadata.


For convenience, and to help avoid duplicating sources, external metadata such as AppStream can be imported into snapcraft.yaml. See Using external metadata for further details.


Add required metadata
---------------------

Global metadata is a mixture of mandatory and optional values.

You can generate a buildable template of both required and recommended values with the snapcraft init command in a new project folder (see Snapcraft overview for more details).

The following attributes are mandatory:

    name A snap’s name is important. It must start with an ASCII character and can only contain 1) letters in lower case, 2) numbers, and 3) hyphens, and it can’t start or end with a hyphen. For the Snap Store, it also needs to be both unique and easy to find.

    For help on choosing a name and registering it on the Snap Store, see Registering your app name.

    summary The summary is a short descriptive sentence to tell prospective users about an application’s primary purpose, in fewer than 80 characters.

    description Unlike the summary, the description can be as verbose as you need it to be. The above snippet shows the description text following a pipe symbol (|), which is used in YAML to maintain newline formatting in multiline text blocks.

    The following, for example, will ensure both Line one and Line two appear on separate lines:

    description: |
        Line one
        Line two

    While you shouldn’t write thousands of words, the more details you provide, the more likely people are to discover and use your application. Feature lists, update descriptions, a brief Getting started guide, are legitimate uses for the description.

    version While having a value for version is mandatory, its value can be anything. Setting this to something like test makes sense while you’re first building your snap, and you can later replace this with a specific version, or a reference to a script that replaces the version number automatically.

    The value for version is also commonly imported for external metadata. See Using using external metadata for further details.

        base A base snap is a special kind of snap that provides a run-time environment with a minimal set of libraries that are common to most applications.

    See Base snaps for help selecting a base for your snap.

    grade This should initially be devel and changed to stable when you have a snap ready for release.

    confinement A snap’s confinement level is the degree of isolation it has from your system. When first building a snap, set this to devmode to initially limit the side-effects of confinement until you have a working snap.

    See Snap confinement for further details.


Add optional metadata
---------------------


Copy metadata from other sources
--------------------------------

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

AppStream is a metadata standard used to describe a common set software components. It can be parsed by snapcraft to provide the title, version, summary, description and icon for a snap, along with the location of an app’s desktop file.

The following is a typical example from an upstream project. It’s an AppStream file called sampleapp.metainfo.xml:

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

Note: The process to get the .desktop file entry from the AppStream metadata goes as follows. First, Snapcraft searches for a parsed AppStream file with the same component id as the app’s common-id and extracts the Desktop File ID (desktop-id) from that component. If that component doesn’t specify a desktop-id, Snapcraft will use the component id as the Desktop File ID. Snapcraft will then search for a desktop file matching the Desktop File ID in the usr/local/share and usr/share directories relative to the part source, and by following the Desktop File ID rules.


From scripts in parts
~~~~~~~~~~~~~~~~~~~~~

Individual parts in your snapcraft.yaml can set the version and grade by using craftctl. All you need to do is select which part to adopt using adopt-info:

# ...
adopt-info: my-part
# ...
parts:
  my-part:
    # ...
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

apps:
  foliate:
    command: desktop-launch $SNAP/usr/bin/com.github.johnfactotum.Foliate
    desktop: usr/share/applications/com.github.johnfactotum.Foliate.desktop
    plugs:
      - desktop
      - desktop-legacy
    ...

During a build, snapcraft will also try to change the Icon= path in the desktop entry file. However, you need to make sure that the Icon= path is accessible from the prime folder. This example replaces the icon path after pulling the source.

parts:
  foliate:
    plugin: meson
    meson-parameters: [--prefix=/snap/foliate/current/usr]
    override-pull: |
      snapcraftctl pull

      # Point icon to the correct location
      sed -i.bak -e 's|Icon=com.github.johnfactotum.Foliate|Icon=/usr/share/icons/hicolor/scalable/apps/com.github.johnfactotum.Foliate.svg|g' data/com.github.johnfactotum.Foliate.desktop.in
