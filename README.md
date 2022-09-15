## connectapi

> **WARNING:** this library is under active development and should not be used for production. The API will change and documentation could be wrong or incomplete.

## Installation

```bash
pip install connectapi
```

## Usage

```python
from connectapi import Client, Content

client = Client()
content = Content.get_one(client, content_guid="241fe2cd-6eba-4a79-9aa3-6e6fe28c5714")
print(content)
# guid='241fe2cd-6eba-4a79-9aa3-6e6fe28c5714' name='Jupyter-Notebook---Palmer-Penguins-1662582421920' title='Jupyter Notebook - Palmer Penguins' description='' access_type='all' connection_timeout=None read_timeout=None init_timeout=None idle_timeout=None max_processes=None min_processes=None max_conns_per_process=None load_factor=None created_time=datetime.datetime(2022, 9, 7, 20, 27, 2, tzinfo=datetime.timezone.utc) last_deployed_time=datetime.datetime(2022, 9, 7, 20, 30, tzinfo=datetime.timezone.utc) bundle_id='61875' app_mode='jupyter-static' content_category='' parameterized=False cluster_name='Kubernetes' image_name='ghcr.io/rstudio/content-pro:r4.1.3-py3.10.4-bionic' r_version=None py_version='3.10.4' quarto_version=None run_as=None run_as_current_user=False owner_guid='d03a6b7a-c818-4e40-8ef9-84ca567f9671' content_url='https://colorado.rstudio.com/rsc/content/241fe2cd-6eba-4a79-9aa3-6e6fe28c5714/' dashboard_url='https://colorado.rstudio.com/rsc/connect/#/apps/241fe2cd-6eba-4a79-9aa3-6e6fe28c5714' role=None id='12560' client=Client(connect_server='https://colorado.rstudio.com/rsc', connect_api_key='XXXXXXXX', api_endpoint='https://colorado.rstudio.com/rsc/__api__/v1')
```

## Resources

- <https://docs.rstudio.com/connect/api/#overview>
- <https://pkgs.rstudio.com/connectapi/>