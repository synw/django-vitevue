# Django Vite Vue

Manage Vitejs frontends and compile them to Django static files and templates. Some management
commands are available:

- [viteconf](#configuration-of-a-vitejs-app): generate a Vitejs compilation configuration
- [tsmodels](#generate-typescript-models): generate Typescript models from Django models
- [tsapi](#add-an-api-to-the-generated-frontend-models): scaffold an api for the generated frontend models

## Install

   ```
   pip install django-vitevue
   ```

Add `"vv",` to `INSTALLED_APPS`

Make sure these basic Django settings are present:

   ```python
TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "templates"],
        # ...
    },
]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"
   ```

## Configuration of a Vitejs app

A management command is available to configure some Vitejs frontends compilation options
and commands. First create a frontend in the parent folder of the Django project with a command
like:

  ```
  yarn create vite frontend --template=vue-ts
  ```

### Settings

The root directory can be configured by a setting. By default it is
the parent directory of the Django's BASE_DIR. Example setting:

  ```
  VV_BASE_DIR = Path("/some/directory")
  ```

### Generate the Vitejs config

If the folder is named *frontend* the command can run without arguments:

  ```
  python {project_name}/manage.py viteconf
  ```

Otherwise add the app folder name as an argument:

  ```
  python {project_name}/manage.py viteconf --app=my_frontend_app_folder_name
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

### Configure templates and static files destination

The npm *build* command will be configured to output to the Django static file
folder and an *index.html* template. To change these options use these command flags:

`--template=mytemplate.html`: the template to compile to. Relative to the django templates dir
`--static=myfolder`: the static folder to compile assets to. Relative to the first staticfiles dir

### Compile to a partial template

By default it will compile a full index page, in single page app mode. It is possible to
compile to a static partial template, without the html tags. Use the partial flag:

`-p`: the template will not have html tags and can be included in a parent Django template

To configure Vitejs to compile an app in partial mode to a specific template and static folder:

  ```
  python {project_name}/manage.py viteconf -p --app=partialapp --template=mytemplate.html --static=myfolder
  ```

## Generate Typescript models

The `tsmodels` command can generate Typescript models from Django models:

   ```
  python {project_name}/manage.py tsmodels my_django_app
   ```

To write the models to the frontend app:

   ```
  python {project_name}/manage.py tsmodels my_django_app -w
   ```

<details>
<summary>Example output:</summary>

These Django models:
<p>

```python
class Market(models.Model):
    name = models.CharField(max_length=255)

class Instrument(models.Model):
    name = models.CharField(max_length=255)

class Trade(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    side = models.CharField(max_length=4, choices=SIDE)
```
</p>
Output these Typescript models:
<p>

```typescript
// Model Market

import MarketContract from "./contract";

export default class Market {
	id: number;
	name: string;

	constructor ({id, name}: MarketContract) {
		this.id=id;
		this.name=name
	}

	static fromJson(data: Record<string, any>): Market {
		return new Market(data as MarketContract)
	}
}

// -------------- Interface -------------- 

export default interface MarketContract {
	id: number,
	name: string,
}

// Model Instrument

import InstrumentContract from "./contract";

export default class Instrument {
	id: number;
	name: string;

	constructor ({id, name}: InstrumentContract) {
		this.id=id;
		this.name=name
	}

	static fromJson(data: Record<string, any>): Instrument {
		return new Instrument(data as InstrumentContract)
	}
}

// -------------- Interface -------------- 

export default interface InstrumentContract {
	id: number,
	name: string,
}

// Model Trade

import MarketContract from "../market/contract";
import InstrumentContract from "../instrument/contract";
import TradeContract from "./contract";

export default class Trade {
	id: number;
	date: string;
	price: number;
	quantity: number;
	market: MarketContract;
	instrument: InstrumentContract;
	side: string;

	constructor ({id, date, price, quantity, market, instrument, side}: TradeContract) {
		this.id=id;
		this.date=date;
		this.price=price;
		this.quantity=quantity;
		this.market=market;
		this.instrument=instrument;
		this.side=side
	}

	static fromJson(data: Record<string, any>): Trade {
		return new Trade(data as TradeContract)
	}
}

// -------------- Interface -------------- 

import MarketContract from "../market/contract";
import InstrumentContract from "../instrument/contract";

export default interface TradeContract {
	id: number,
	date: string,
	price: number,
	quantity: number,
	market: MarketContract,
	instrument: InstrumentContract,
	side: string,
}

```
</p>
</details>  

## Add an api to the generated frontend models

To scaffold an api for an existing frontend model:

  ```
  python {project_name}/manage.py tsapi my_django_app_name
  ```

<details>
<summary>Example output</summary>

<p>Methods will be added to models. Ex:</p>

```typescript
export default class Market {
	// ...

	static async load(id: number | string): Promise<Market> {
		const res = await api.get<Record<string, any>>(`/api/market/${id}/`);
		return Market.fromJson(res)
	}
}
```

<p>The command will create an api directory containing an helper class: https://github.com/synw/django-vitevue/blob/master/vv/files/api/model.ts</p>

</details>

## Example

### Backend

Create a project directory and initialize a Django project with *static* and *templates* folders:

  ```
  pip install django django-vitevue
  mkdir my_project
  cd my_project
  django-admin createproject my_project
  cd my_project
  mkdir templates static
  cd ..
  ```

Add `"vv",` to `INSTALLED_APPS`

Configure the basic settings:

   ```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        # ...
    },
]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"
   ```

Add an url to view the index template:

   ```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    path("", TemplateView.as_view(template_name="index.html")),
]
   ```

### Frontend

Initialize a Vue 3 Typescript frontend:

  ```
  yarn create vite frontend --template=vue-ts
  cd frontend
  yarn install
  cd ..
  ```

### Run

Run the migrations:

   ```
   python my_project/manage.py migrate
   ```

Generate the frontend config. Dry run:

   ```
   python my_project/manage.py viteconf
   ```

Install the frontend dev dependencies as indicated in the command output message:

   ```
  cd frontend 
  yarn add -D move-file-cli del-cli npm-run-all
  cd ..
   ```

Then write the config to *vite.config.ts* and *package.json*:

   ```
   python my_project/manage.py viteconf -w
   ```

Build the frontend:

   ```
  cd frontend 
  yarn build
  cd ..
   ```

Run the server:

   ```
   python my_project/manage.py runserver
   ```

Example repository: https://github.com/synw/django-vitevue-example

## Run the tests

Clone and run:

```
make install
make test-initial
```

To run the code quality checker install [Pycheck](https://github.com/emencia/pycheck) and run:

```
make quality
```