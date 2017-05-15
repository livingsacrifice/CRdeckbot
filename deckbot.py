import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime

SCOPES = "https://www.googleapis.com/auth/spreadsheets"
CLIENT_SECRET = 'client_id.json'
store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
	credz = tools.run_flow(flow, store)
SHEETS = discovery.build('sheets', 'v4', http=credz.authorize(Http()))
spreadsheetId = [enter google sheet ID here]

my_bot = Bot(command_prefix="!")

cardList = ['knight','icespirit','skeletons','rocket','mortar','arrows','archers','thelog','goblins','zap','firespirits','speargoblins','goblingang','minions','cannon','bomber','tesla','barbarians','minionhorde','royalgiant','elitebarbarians','icegolem','tombstone','dartgoblin','megaminion','furnace','fireball','musketeer','minipekka','valkyrie','hogrider','battleram','wizard','bombtower','infernotower','goblinhut','giant','elixircollector','barbarianhut','threemusketeers','mirror','rage','clone','guards','skeletonarmy','goblinbarrel','tornado','darkprince','babydragon','freeze','poison','bowler','executioner','prince','witch','balloon','giantskeleton','x-bow','lightning','pekka','golem','miner','princess','icewizard','infernodragon','electrowizard','lumberjack','graveyard','sparky','lavahound','bandit','heal']

#if name is in cardList, returns original input
#if name is not in cardList, checks alternate names, and returns that
#if not in card list or alternate, returns cardunknown
def altnamecheck(input):
	return_val = "cardunknown"
	for i in range(len(cardList)):
		if cardList[i] == input:
			return_val = input
	matchArray = [['log','thelog'],['lava','lavahound'],['xbow','x-bow'],['hog','hogrider'],['3m','threemusketeers'],['rg','royalgiant'],['ebarbs','elitebarbarians'],['loon','balloon'],['ewiz','electrowizard'],['inferno','infernotower'],['it','infernotower'],['pump','elixircollector'],['collector','elixircollector'],['barrel','goblinbarrel'],['barbs','barbarians'],['gy','graveyard'],['valk','valkyrie'],['skarmy','skeletonarmy'],['ram','battleram'],['lj','lumberjack'],['gang','goblingang'],['horde','minionhorde']]		
	if return_val == "cardunknown":
		for row in matchArray:
			if input == row[0]:
				return_val = row[1]
	return return_val

@my_bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(my_bot.user))

@my_bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await my_bot.say('{0.name} joined in {0.joined_at}'.format(member))

@my_bot.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await my_bot.send_message(server, fmt.format(member, server))

@my_bot.command()
async def search(*optionx : str):
	"""Searches for decks based on parameters (default is -c if no parameter given): \n -c for cards to include (use ! in front of card to get decks without that card)\n -e for average elixir cost\n -l for minimum arena level\n -r for maximum rarirty (c/r/e/l)\n -a for maximum age of deck\n -u for a specific user\n For example, [!search -c golem !lightning -e 4 -a 30] will search for a golem deck without lightning with avg elixir from 3.75 to 4.25 that is less than 30 days old.\n If YouTube images are too much clutter, go to user setting -> text and images -> disable 'when posted as links to chat'"""
	if len(optionx) == 0:
		return await my_bot.say('You must enter search options')
	options = ''
	for value in optionx:
		options = options + value.lower() + ' '
	options = options[0:(len(options)-1)]
	print(options)
	strAge = ''
	strCards = ''
	strElixir = ''
	strLevel = ''
	strRarity = ''
	strUser = ''
	if '-r' in options:
		locRarity =  options.find('-r')
		endRarity = options[locRarity:].find(' -')
		if endRarity == -1:
			strRarity = options[(locRarity+3):]
		else:
			endRarity = endRarity + locRarity
			strRarity = options[(locRarity+3):endRarity]
	if '-a' in options:
		locAge = options.find('-a')
		endAge = options[locAge:].find(' -')
		if endAge == -1:
			strAge = options[(locAge+3):]
		else:
			endAge = endAge + locAge
			strAge = options[(locAge+3):endAge]
	if '-c' in options:
		locCards = options.find('-c')
		endCards = options[locCards:].find(' -')
		if endCards == -1:
			strCards = options[(locCards+3):]
		else:
			endCard = endCards + locCards
			strCards = options[(locCards+3):endCards]
	if '-e' in options:
		locElixir = options.find('-e')
		endElixir = options[locElixir:].find(' -')
		if endElixir == -1:
			strElixir = options[(locElixir+3):]
		else:
			endElixir = endElixir + locElixir
			strElixir = options[(locElixir+3):endElixir]
	if '-l' in options:
		locLevel = options.find('-l')
		endLevel = options[locLevel:].find(' -')
		if endLevel == -1:
			strLevel = options[(locLevel+3):]
		else:
			endLevel = endLevel + locLevel
			strLevel = options[(locLevel+3):endLevel]
	if '-u' in options:
		locUser = options.find('-u')
		endUser = options[locUser:].find(' -')
		if endUser == -1:
			strUser = options[(locUser+3):]
		else:
			endUser = endUser + locUser
			strUser = options[(locUser+3):endUser]
	#changing default behavior to assume they meant -c     if options == '23': 
	if optionx == '':
		return await my_bot.say('You must enter search options')
	#elif strUser == '' and strAge == '' and strLevel == '' and strCards == '' and strRarity == '' and strElixir == '':
	#	return await my_bot.say('Invalid search formatting; enter !help search for formatting hints')
	else:
		rangeName = 'decks!D1'
		result = SHEETS.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
		values = result.get('values', [])
		if not values:
			print('No data found.')
			return await my_bot.say('Error reading from sheet')
		else:
			print('Rarity: ' + strRarity)
			print('Level: ' + strLevel)
			print('Age: ' + strAge)
			print('Cards: ' + strCards)
			print('Elixir: ' + strElixir)
			print('User: ' + strUser)
			rownum = 20
			for row in values:
				rownum = int(row[0])
			rangeName = 'decks!A2:AM' + str(rownum)
			result = SHEETS.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
			values = result.get('values', [])
			if not values:
				print('No data found.')
				return await my_bot.say('No decks saved')
			else:
				if strCards == '':
					if strUser == '' and strAge == '' and strLevel == '' and strCards == '' and strRarity == '' and strElixir == '':
						#assume user meant to search by cards
						for value in optionx:
							strCards = strCards + value.lower() + ' '
						strCards = strCards[0:(len(strCards)-1)]
						print('Cards2: ' + strCards)
				if strCards != '':
					cardx = strCards.split(' ')
					print(str(len(cardx)) + ' cards being searched')
					for i in range(len(cardx)):
						if cardx[i][0] == '!':
							cardx[i] = cardx[i][0] + altnamecheck(cardx[i][1:])
						else:
							cardx[i] = altnamecheck(cardx[i])
						print(cardx[i])
						if cardx[i] == 'cardunknown':
							return await my_bot.say('Unknown card in parameters')
				strx = ["" for i in range(3)]
				cnt = 0
				print('length of values is ' + str(len(values)))
				for row in values:
					failx = False
					if strCards != '' and strCards != ' ':
						foundC = [False for i in range(len(cardx))]	
						for i in range(len(cardx)):
							if cardx[i][0] == '!':
								foundC[i] = True
								for j in range(8):
									if cardx[i][1:] == row[j+1].replace('\n',''):
										foundC[i] = False
							else:
								for j in range(8):
									if cardx[i] == row[j+1].replace('\n',''):
										foundC[i] = True
						for i in range(len(cardx)):
							if foundC[i] == False:
								failx = True
					if failx == False and strLevel != '':
						if int(row[36]) > int(strLevel):
							failx = True
					if failx == False and strElixir != '':
						if float(row[17]) < (float(strElixir)-0.25) or float(row[17]) > (float(strElixir)+0.25):
							failx = True
					if failx == False and strUser != '':
						if row[0] != strUser:
							failx = True
					if failx == False and strRarity != '':
						rarityx = strRarity[0]
						rarityz = 0
						if rarityx == 'c':
							rarityz = 0
						elif rarityx == 'r':
							rarityz = 1
						elif rarityx == 'e':
							rarityz = 2
						elif rarityx == 'l':
							rarityz = 3
						else:
							return await my_bot.say('Invalid rarity selection')
						if int(row[26]) > rarityz:
							failx = True
					if failx == False and strAge != '':
						if len(row) > 38:
							deckdate = datetime.strptime(str(row[38]),"%m/%d/%y")
							present = datetime.now()
							datediff = present - deckdate
							if datediff.days > int(strAge):
								failx = True
					if failx == False:
						if cnt < 3:
							strx[cnt] = row[0] + ': ' + row[1] + ', ' + row[2] + ', ' + row[3] + ', ' + row[4] + ', ' + row[5] + ', ' + row[6] + ', ' + row[7] + ', ' + row[8] + '; Avg elixir: ' + row[17] + '; Max rarity: ' + row[27] + '; Min arena: ' + row[36] + '\n'
							if len(row) > 37:
								if row[37] != '':
									strx[cnt] = strx[cnt] + row[37] + '\n'
						cnt = cnt + 1			
				print(str(cnt) + 'matches found')
				print(strx[0])
				if cnt == 0:
					return await my_bot.say('No decks found matching criteria')
				elif cnt == 1:
					return await my_bot.say(strx[0])
				elif cnt == 2:
					return await my_bot.say(strx[0] + strx[1])
				elif cnt == 3:
					return await my_bot.say(strx[0] + strx[1] + strx[2])
				elif cnt > 3:
					return await my_bot.say(strx[0] + strx[1] + strx[2] + '\n' + 'More than 3 (' + str(cnt) + ') results. Add extra parameters to narrow results.')

@my_bot.command(pass_context=True, no_pm=True)
async def save(ctx, *cards : str):
	"""Saves a deck under your username; !save [card1 card2...card8]"""
	user = ctx.message.author
	rangeName = 'decks!D1'
	result = SHEETS.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
		return await my_bot.say('Error reading from sheet')
	else:
		rownum = 20
		for row in values:
			rownum = int(row[0])+1
		
		if len(cards) != 8:
			return await my_bot.say('Deck does not have 8 cards')
		else:
			cardx=[cards[i].lower() for i in range(8)]
			for i in range(8):
				cardx[i] = altnamecheck(cardx[i])
				if cardx[i] == "cardunknown":
					return await my_bot.say('Unknown card in parameters')
			#check if deck already exists
			rangeName = 'decks!A2:I' + str(rownum-1)
			result = SHEETS.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
			values = result.get('values', [])
			for row in values:
				cnt = 0
				for i in range(8):
					for j in range(8):
						if row[j+1] == cardx[i]:
							cnt = cnt + 1
				if cnt == 8:
					return await my_bot.say('Deck already exists')
			rangeName = 'decks!A' + str(rownum) + ':I' + str(rownum)
			values = [[user.name.lower(),cardx[0],cardx[1],cardx[2],cardx[3],cardx[4],cardx[5],cardx[6],cardx[7]]]
			body = {
				'values': values
			}
			#body = values
			#body = ['values': values]
			result = SHEETS.spreadsheets().values().update(
				spreadsheetId=spreadsheetId, range=rangeName,
				valueInputOption='RAW', body=body).execute()
			present = datetime.now()
			rangeName = 'decks!AM' + str(rownum)
			strPresent = str(present.month) + '/' + str(present.day) + '/' + str(present.year)[2:]
			values = [[strPresent]]
			body = {
				'values': values
			}
			result = SHEETS.spreadsheets().values().update(
				spreadsheetId=spreadsheetId, range=rangeName,
				valueInputOption='RAW', body=body).execute()
			#F.write(user.name.lower() + ',' + cardx[0] + ',' + cardx[1] + ',' + cardx[2] + ',' + cardx[3] + ',' + cardx[4] + ',' + cardx[5] + ',' + cardx[6] + ',' + cardx[7] + '\n')
			#F.close()
			return await my_bot.say('Saving deck for {0} with {1} cards'.format(user.name,len(cards)))

@my_bot.command()
async def strikes(userx : str):
	"""Lists how many strikes a user has; !strikes [user] or !strikes high"""
	usery = userx.lower()
	rangeName = 'Alchemy_activity!A5:D'
	result = SHEETS.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	if not values:
		print('No data found.')
	else:
		if usery == 'high':
			returnstr = ''
			for row in values:
				if row[2] == '2' or row[2] == '3' or row[2] == '4':
					if row[1] == 'FALSE':
						returnstr = returnstr + row[0] + ' has ' + row[2] + ' strikes.\n'
			if returnstr == '':
				return await my_bot.say('No users have 2 or more strikes')
			else:
				return await my_bot.say(returnstr)
		else:
			for row in values:
				if row[0].lower() == usery:
					return await my_bot.say(usery + ' has ' + row[2] + ' strikes.')
	return await my_bot.say(usery + ' not found.')
my_bot.run([insert token here])
