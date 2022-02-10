# Django Vite Vue

[![pub package](https://img.shields.io/pypi/v/django-vitevue)](https://pypi.org/project/django-vitevue/)

Manage Vitejs frontends and compile them to Django static files and templates. Features

- [Configure Vitejs for Django](#configuration-of-a-vitejs-app-to-compile-to-django-templates-and-static-files): use a management
command to help configuring Vitejs to compile to Django templates and static files
- [Typescript scaffolding](#typescript-models): generate Typescript models from existing Django models
- [Api and views](#add-an-api-to-the-generated-frontend-models): api helper frontend class configured for Django and login/logout views with single page app support

## Install

   ```
   pip install django-vitevue
   ```

Add `"vv",` to `INSTALLED_APPS`

Make sure the basic Django template and static dirs settings are present. Run the 
`vvcheck` management command to see if the config is ok

## Configuration of a Vitejs app to compile to Django templates and static files

### Architecture and settings

The recommended file structure for a single page app is:

- project_root_dir
	- django_project
 	- vite_project

A management command is available to configure some Vitejs frontends compilation options
and commands. First create a frontend in the parent folder of the Django project with a command
like:

  ```bash
  yarn create vite frontend --template=vue-ts
  ```

Or use and existing one. 

The root directory can be configured by a setting. By default it is
the parent directory of the Django's `BASE_DIR`, like in the file structure shown above. 
Example setting to put the frontend dev code directly in the django project directory:

  ```python
  VV_BASE_DIR = BASE_DIR
  ```

### Generate the Vitejs config

If the Vite app project folder is named *frontend* the command can run without arguments:

  ```
  python {django_project}/manage.py viteconf
  ```

Otherwise add the app folder name as an argument:

  ```
  python {django_project}/manage.py viteconf --app=my_frontend_app_folder_name
  ```

This command will do the following things:

- Generate compilation options for the *vite.config.js* or *vite.config.ts* file
- Generate npm build commands for *package.json*
- Check if all the required npm dependencies are installed

The command runs in dry mode and outputs the config. To write to config files
use the `-w` flag:

  ```
  python {django_project}/manage.py viteconf -w
  ```

### Options

#### Configure templates and static files destination

The npm *build* command will be configured to output to the Django static file
folder and an *index.html* template. To change these options use these command flags:

`--template=mytemplate.html`: the template to compile to. Relative to the django templates dir
`--static=myfolder`: the static folder to compile assets to. Relative to the first staticfiles dir

Example to compile the template to `templates/myapp/mytemplate.html` and the static assets to `static/myapp`:

  ```
  python {django_project}/manage.py viteconf --template=myapp/mytemplate.html --static=myapp
  ```

#### Compile to a partial template

By default it will compile a full index page, in single page app mode. It is possible to
compile to a static partial template, without the html tags. Use the partial flag:

`-p`: the template will not have html tags and can be included in a parent Django template

To configure Vitejs to compile an app in partial mode to a specific template and static folder:

  ```
  python {django_project}/manage.py viteconf -p --app=partialapp --template=mytemplate.html --static=myfolder
  ```

## Typescript models

### Generate Typescript models from Django models

The `tsmodels` command can generate Typescript models from Django models:

   ```
  python {django_project}/manage.py tsmodels my_django_app
   ```

To write the models to the frontend app:

   ```
  python {django_project}/manage.py tsmodels my_django_app -w
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

### Add an api to the generated frontend models

To scaffold an api for an existing frontend model:

  ```
  python {django_project}/manage.py tsapi my_django_app_name
  ```

This will create an api for the Typescript models and copy an `api` helper
in the frontend `src` directory

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

</details>

### Login views

Some login/logout views are available from the backend, and supported by the frontend
api helper class. Add the urls in `urls.py`:

```
urlpatterns = [
    path("vv/", include("vv.urls")),
		#...
]
```

Two api views will be available: `/vv/auth/login/` and `/vv/auth/logout/`. The frontend api
helper class have support for these views [example code](https://github.com/synw/django-vitevue-example/blob/main/django_vitevue_example/static/demo/App.vue)

## Example

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