# %%
# from connectapi import Client, User, Content

# from rich import print, inspect
# # %%

# client = Client()
# user = User.whoami(client)
# print(user)
# # %%

# print(user.get_my_content())

# # %%
# my_content = Content.get_my_content(client)
# for content in my_content:
#     print(f"{content.guid} -> {content.title}")


# # %%
# from connectapi import Client, User, Content
# from rich import print, inspect

# client = Client()

# guid = "55550401-40ad-41e5-b148-68d6cc306986"
# content = Content.get_one(client, guid)

# content.title = "Yzzz"
# content.description = "X"
# content.max_processes = 5
# content.min_processes = 1
# content.load_factor = 0.77

# content.update()
# %%
from connectapi import Client, User, Content
from rich import print, inspect
from uuid import uuid4

client = Client()
# %%


# Create
data = {
        'access_type': 'acl',
        'connection_timeout': 3600,
        'description': 'This report calculates per-teamy statistics ...',
        'idle_timeout': 5,
        'init_timeout': 60,
        'load_factor': 0.5,
        'max_conns_per_process': 20,
        'max_processes': 3,
        'min_processes': 0,
        'name': str(uuid4()),
        'read_timeout': 3600,
        'run_as': 'rstudio-connect',
        'run_as_current_user': False,
        'title': 'Quarterly Analysis of Team Velocity'
    }
content = Content.create(client, **data)

# %%
# delete
content.delete(force=True)

# %%
# content = Content.get_one(client, "481ea207-367e-448b-a4c9-0da1acb5edcc")
# content.delete()
# %%
# my_content = Content.get_my_content(client)

# for content in my_content:
#     content.delete()