"""
Sublime-Text API Interface of HackLime

Author  : Pravendra Singh (pravj)
Contact : hackpravj@gmail.com (https://pravj.github.io)
"""

# modules for Sublime-Text's API
import sublime
import sublime_plugin

# module to talk with HackerEarth API
from HackerEarth import HackerEarth

# Help guide text for HackLime
import HelpGuide

# class for code-compile command
class HacklimeCompileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "HackLime is compiling !!")
		instance = HackerEarth(self.view.file_name())
		print instance.lang


# class for code-run command
class HacklimeRunCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "HackLime is running !!")
		instance = HackerEarth(self.view.file_name())
		print instance.lang

# class for help with package, kind of way to use
class HacklimeHelpCommand(sublime_plugin.WindowCommand):
    def run(self):
    	# view instance representing help guide
        self.help_view = self.window.get_output_panel("HackLime-Help")

        # allows to write custom help text in view
        self.help_view.set_read_only(False)

        # writing to help view
        edit = self.help_view.begin_edit()
        self.help_view.insert(edit, self.help_view.size(), HelpGuide.helptext)
        self.help_view.end_edit(edit)

        # help guide is now read only
        self.help_view.set_read_only(True)

        # running the show_panel window command 
        # with the panel argument set to the name with an "output." prefix.
        # Sublime-API Docs : sublime.Window.get_output_panel() -> Description
        self.window.run_command("show_panel", {"panel": "output.HackLime-Help"})