from pathlib import Path

import sublime
import sublime_plugin

PROJECT_TEMPLATE = R"""
{
    "folders": [
        {
            "path": ".."
        }
    ],
    "build_systems": [],
    "settings": {},
}
"""


class FolderProjectAssigner(sublime_plugin.EventListener):
    """
    This class describes a folder project assigner.

    If a new window is opened with a single folder but no project assigned,
    it is very likely a result of ``subl folder``.

    So, search for a ``*.sublime-project`` file to open instead.

    If not project file was found, a new one is created in a `.sublime`
    sub directory, to make ``hot_exit`` work as expected.
    """

    def on_init(self, views: sublime.View):
        for window in sublime.windows():
            self.assign_project(window)

    def on_new_window(self, window: sublime.Window):
        sublime.set_timeout(lambda: self.assign_project(window))

    def assign_project(self, window: sublime.Window):
        if not window:
            return

        project = window.project_file_name()
        if project:
            return

        folders = window.folders()
        if len(folders) != 1:
            return

        root = Path(folders[0])

        project_file = self.find_project_file(root)
        if not project_file:
            settings = sublime.load_settings("Preferences.sublime-settings")
            if not settings.get("auto_generate_folder_projects", True):
                return

            sublime_dir = root / ".sublime"
            sublime_dir.mkdir(exist_ok=True)

            project_file = sublime_dir / (root.name + ".sublime-project")
            with open(project_file, mode="w", encoding="utf-8") as fp:
                fp.write(PROJECT_TEMPLATE.lstrip())

        window.run_command(
            "open_project_or_workspace",
            {"file": str(project_file), "new_window": False},
        )

    def find_project_file(self, root):
        patterns = (
            "*.sublime-project",
            ".sublime/*.sublime-project"
        )
        for pattern in patterns:
            try:
                return next(root.glob(pattern))
            except StopIteration:
                pass

        return None
