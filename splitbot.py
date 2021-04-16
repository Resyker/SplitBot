import discord
from discord.ext import commands
import json
import asyncio

#Roles that are allowed to confirm splits
check_roles = {'Mod'}


client = commands.Bot(command_prefix = '!')

@client.command()
async def shutdown(ctx):
	await client.close()

@client.event
async def on_ready():
	print('Bot is ready.\n')

@client.command()
async def split(ctx, amount_per, *mentions: discord.Member):

	with open("users.json", "r")as f:
		users = json.load(f)

		mentions = list(mentions)

		try:
			reaction, user = await client.wait_for('reaction_add', timeout=30.0,
				check= lambda reaction, user: bool(set(user.roles).intersection()))
#TODO: Add functionality for different emojis

			for member in mentions:
				await add_user(ctx, users, member)
				await update_user_split(ctx, users, member, amount_per)

			await ctx.send(f"Confirmed split of {amount_per} for {', '.join([i.name for i in mentions])}")

			with open("users.json", "w") as f:
				json.dump(users, f)

		except asyncio.TimeoutError:
			await ctx.send(f" {', '.join(check_roles)} has not confirmed your split. Please try again or contact a Mod")

#Uncomment when not debugging
		# except Exception as e:
		# 	print(e)
		# 	await ctx.send("Something went wrong")




async def add_user(ctx, users, user):
	uid = str(user.id)

	if users.get(uid) is None:
		users[uid] = {}
		users[uid]["total"] = 0
		users[uid]["number_of_splits"] = 0
		users[uid]["splits"] = []

		await ctx.send(f"Added {user.name} to the split database!")

async def update_user_split(ctx, users, user, splitamount):
	uid = str(user.id)

	users[uid]["splits"].append(
		{"date": 0, "amount": splitamount})
	users[uid]["total"] = int(users[uid]["total"]) + int(splitamount)
	users[uid]["number_of_splits"] = int(users[uid]["number_of_splits"]) + 1


client.run('ODMyNjAyNzk1MDIxOTU5MTc4.YHmLxw.r_31TfJ1GSabxQfqPyfRZtTZ2Y4')
