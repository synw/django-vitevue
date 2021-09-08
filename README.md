# Django Vite Vue

Manage Vitejs frontends and compile them to Django static files and templates

## Configuration of a Vitejs app

A management command is available to configure some Vitejs frontends compilation options
and commands. First create a frontend at the root of the Django project with a command
like:

  ```
  yarn create vite frontend --template=vue-ts
  ```

If the folder is named *frontend* the command can run without arguments:

  ```
  python {project_name}/manage.py viteconf
  ```

Otherwise add the app folder name as an argument:

  ```
  python {project_name}/manage.py viteconf my_frontend_app_folder_name
  ```

This command will do the following things:

- Generate compilation options for the *vite.config.js* or *vite.config.ts* file
- Generate npm build commands for *package.json*
- Check if all the required npm dependencies are installed

The command runs in dry mode and outputs the config. To write to config files
use the `-w` flag:

  ```
  python {project_name}/manage.py viteconf -w
  ```

The npm *build* command will be configured to output to the Django static file
folder and an *index.html* template. To change these options use the settings

## Optional settings

Use the *VITE_APPS* setting to configure the compilation destination:

  ```python
  VITE_APPS: List[Dict[str, Path]] = [
	  {
		  "dir": settings.BASE_DIR / "frontend",
		  "template": templates_dir / "mytemplate.html",
		  "static": static_dir / "frontend",
	  }
	]
  ```
