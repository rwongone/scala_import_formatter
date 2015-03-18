# scala_import_formatter

Automatically arrange your Scala imports as they are described in Inkling's Scala coding style guide (with some exceptions)!

e.g.
```
import java.io.{
  AThingThatShouldGoFirst,
  FileNotFoundException,
  HolySnap,
  AhIThinkThisWillMakeTheImportTooLong,
  File,
  Weird
}
```

# Caveats and Known Failing Cases

This plugin tends to add unnecessary whitespace to source code, but this problem is mitigated with the use of Scalariform.

This plugin doesn't play well with comments interspersed with import statements.

This plugin also doesn't play well with files that are not Scala source code.

If imports with comments will be grouped, the result will not compile.

```
import java.io.File // a comment
import java.io.FileNotFoundException
```
becomes
```
import java.io.{
	File // a comment,
	FileNotFoundException
}
```

# On the Other Hand...

If you mistakenly insert an import statement anywhere in your code, it will be shepherded to the top with the rest of your imports!
```
import java.io.File

class ClassThing {
	def main = {
		println("niceee")
		import java.io.FileNotFoundException
	}
}
```
becomes
```
import java.io.{ File, FileNotFoundException }


class ClassThing {
	def main = {
		println("niceee")

	}
}
```

# To Use

Copy the .py file to ~/Library/Application Support/Sublime Text 2/Packages/User/organize_scala_imports.py. From the Sublime GUI you can quickly access this folder by hitting cmd+shift+P and searching for `Preferences: Browse Packages`.

Hit cmd+shift+P and open `Preferences: Key Bindings - User`.

Find a suitable key binding for the command (e.g. ctrl+\\\\) and apply it to the keymap as follows:
```
[
	{ "keys": ["ctrl+\\"], "command": "organize_scala_imports"}
]
```

Or if you want to execute from a console,
ctrl+` for python console, then
`view.run_command("organize_scala_imports")` to execute.