# %%
from connectapi import Client, User, Content
# %%

client = Client()
user = User.whoami(client)
print(user)
# %%

print(user.get_my_content())

# %%
my_content = Content.get_my_content(client)
print(my_content)


# %%