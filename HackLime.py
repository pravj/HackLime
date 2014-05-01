"""
Sublime-Text API Interface of HackLime
with help of https://www.sublimetext.com/docs/2/api_reference.html

Author  : Pravendra Singh (pravj)
Contact : hackpravj@gmail.com (https://pravj.github.io)
"""

import os

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
		filepath = self.view.file_name().encode("utf-8")
		#print (filepath)  maybe you are not waiting for it to load all
		instance = HackerEarth(filepath)

		# HackerEarth API response and text to write in output
		response = instance.Contact()

		"""
		creates file for output response, if not present already
		output file will have a prefix 'output_' to main file
		"""

		# shows error in quick panel
		if('er' in response):
			show_error(self.view.window, [response['er']])
		else:
			output_text = instance.Output(response)

			# shows the output buffer/file
			output = HacklimeOutput(self.view, file_handler(filepath), output_text)
			output.show()


# class for code-run command
class HacklimeRunCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		filepath = self.view.file_name().encode("utf-8")
		#print (filepath)  maybe you are not waiting for it to load all
		instance = HackerEarth(filepath)

		response = instance.Contact()

		# shows error in quick panel
		if('er' in response):
			show_error(self.view.window, [response['er']])
		else:
			output_text = instance.Output(response)

			# shows the output buffer/file
			output = HacklimeOutput(self.view, file_handler(filepath), output_text)
			output.show()


# class for help with package, kind of ways to use
class HacklimeHelpCommand(sublime_plugin.WindowCommand):
    def run(self):
    	# view instance representing help guide
        self.help_view = self.window.get_output_panel("HackLime-Help")

        # allows to write custom help text in view object
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


# shows result in new file
class HacklimeOutput:
	def __init__(self, view, output_file, text):
		# view object for current open file
		self.view = view

		# output file's name
		self.filename = output_file

		# output file's content
		self.text = text

	def show(self):
		# window object containing current view
		window = self.view.window()

		# output file's view object
		output_view = window.new_file()

		# shakespeare was wrong, name is necessary
		# names the output buffer/file
		output_view.set_name(self.filename)

		# edites the content of file
		editor = output_view.begin_edit()
		output_view.insert(editor, output_view.size(), self.text)
		output_view.end_edit(editor)


# returns output file's name using a given file
def file_handler(filepath):
	# original file name
	File = filepath.split('/')[-1]

	# output file name
	output_File = 'output_' + File.replace(File.split('.')[-1], 'txt')

	return output_File

# shows error in quick panel
def show_error(errors, window):
	window.show_quick_panel(errors, None, sublime.MONOSPACE_FONT)
