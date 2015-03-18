import collections, re
import sublime, sublime_plugin

def add( dict, key, value ):
	if key in dict.keys():
		dict[key].extend(value)
	else:
		dict[key] = value

def applyStrip( str ):
	return str.strip()

def getValues( blob ):
	match = re.search(r'{(.*)}', blob)
	if match:
		return map(applyStrip, match.group(1).split(","))
	else:
		return [blob]

def addSourceToStanza( imports, source, index ):
	parts = re.search(r'(.*)\.(.*)', source)
	key = parts.group(1)
	value = getValues(source[len(key) + 1:])
	add(imports[index], key, value)

def grabBracketItems( region, self ):
	if self.view.substr(region).strip().endswith("{"):
		return sublime.Region(region.a, (self.view.find(r'\}', region.a)).b)
	else:
		return region

class OrganizeScalaImportsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		content = self.view.substr(sublime.Region(0, self.view.size()))
		import_regions = self.view.find_all(r'^\s*import .*$')
		new_regions = []
		for region in import_regions:
			new_regions.append(grabBracketItems(region, self))

		if len(new_regions) == 0:
			return
		else:
			try:
				edit_obj = self.view.begin_edit("OrganizeScalaImports")

				cursor = new_regions[0].begin()
				imports = [{}, {}, {}]

				for region in new_regions:
					source = re.search(r'^\s*import (.*)', self.view.substr(region)).group(1)
					if (source.endswith("{")):
						source = self.view.substr(sublime.Region(region.a + len("import "), region.b))

					if source.startswith("java.") or source.startswith("scala."):
						addSourceToStanza(imports, source, 0)
					elif source.startswith("com.inkling."):
						addSourceToStanza(imports, source, 2)
					else:
						addSourceToStanza(imports, source, 1)

				# Delete existing import statements.
				offset = 0
				for region in new_regions:
					self.view.erase(edit_obj, sublime.Region(region.b - offset, region.a - offset))
					offset += (region.b - region.a)

				# Write new import statements.
				for i in range(0, 3):
					for key in sorted(imports[i]):
						import_list = imports[i][key]

						if len(import_list) > 1:
							import_list.sort()

							start_piece = "import " + key + ".{ "
							middle_piece = ", ".join(import_list)
							end_piece = " }\n"

							if len(start_piece + middle_piece + end_piece) >= 100:
								start_piece = "import " + key + ".{\n  "
								middle_piece = ",\n  ".join(import_list)
								end_piece = "\n}\n"

							self.view.insert(edit_obj, cursor, start_piece)
							cursor += len(start_piece)

							self.view.insert(edit_obj, cursor, middle_piece)
							cursor += len(middle_piece)

							self.view.insert(edit_obj, cursor, end_piece)
							cursor += len(end_piece)

						else:
							import_piece = "import " + key + "." + import_list[0]
							self.view.insert(edit_obj, cursor, import_piece)
							cursor += len(key) + len(import_list[0]) + len("import .") + 1
					self.view.insert(edit_obj, cursor, "")
					cursor += 1

			finally:
				self.view.end_edit(edit_obj)
