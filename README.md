# scala_import_formatter

Cover the case where items are on different lines.

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

Copy the .py file to ~/Library/Application Support/Sublime Text 2/Packages/User/organize_scala_imports.py.

ctrl+` for console, then
view.run_command("organize_scala_imports") to execute.