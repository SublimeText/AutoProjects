# AutoProjects

A [Sublime Text][] plugin to automatically open folders as projects.

The key benefit is to enable "hot_exit" on arbitrary folders,
so Sublime Text window can be closed without loosing unsaved content.

## Usage

Simply open a folder via command line (e.g.: `subl <folder>`) or Explorer's context menu
and never loose unsaved files or get bothered by "Do you want to save ..." dialogs anymore.

If no project is found a new `.sublime/<Folder>.sublime-project` file is created and opened,
just like VS Code creates its `.vscode` sub directory to store all folder related information.

Automatic project creation can be disabled by setting `"auto_generate_projects": false`
in `Preferences.sublime-settings`.


[Sublime Text]: https://sublimetext.com
