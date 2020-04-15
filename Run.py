import string
import time
import math
import datetime
import pytz
from pytz import timezone
import random
import urllib.request
from urllib.request import urlopen
from json import loads
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Read import getUser, getMessage
from Settings import CHANNEL, COOLDOWN, IDENT, CHANNELPASS, CLIENT_ID

#Checks to see if chat line is from Twitch or chat.
def Console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True

#Global cooldown
def cooldown():
    if user == CHANNEL:
        pass
    elif user:
        abort_after = COOLDOWN
        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break

def getUserID(username):
    try:
        url = "https://api.twitch.tv/kraken/users?login={}".format(username)
        hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise LookupError('User not found')
        return

    readable = response.read().decode('utf-8')
    lst = loads(readable)
    USER_ID = lst['users'][0]['_id']
    return USER_ID

def isLive(username):
    try:
        url = "https://api.twitch.tv/kraken/users?login={}".format(username)
        hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise LookupError('User not found')
        return

    readable = response.read().decode('utf-8')
    lst = loads(readable)
    live = False
    if lst['stream']:
        live = True
    return live

#Basic command function
def basicCommand(input, output):
    if input == message.strip():
        sendMessage(s, output)
        cooldown()

#Adds a text command to commands.txt
def addCommand(input):
    if input == message.lower().split()[0] and (user == CHANNEL or user in moderators) and user != IDENT:
        a = open("commands.txt", "r")
        commandList = a.readlines()
        commandNames = []
        for line in commandList:
            commandNames.append(line.split()[0].lower().strip(";"))
        a.close()
        writeCommand = open("commands.txt", "a")
        commandMessage = message
        command = commandMessage.split(input, 1)[-1].strip()
        try:
            if command[0] == "!" and command.split()[0] not in commandNames:
                writeCommand.write(command.split()[0] + "; " + command.split(' ', 1)[1] + "\n")
                sendMessage(s, "Command " + command.split()[0] + " successfully added.")
                writeCommand.close()
                cooldown()
            elif command.split()[0] in commandNames:
                sendMessage(s, "Error: Command " + command.split()[0] + " already exists")
                cooldown()
                return
            else:
                sendMessage(s, "Error: Invalid syntax for the !addcommand command. Correct syntax is: !addcommand !<command_name> <command_text>")
                cooldown()
        except IndexError as err:
            sendMessage(s, "Error: Invalid syntax for the !addcommand command. Correct syntax is: !addcommand !<command_name> <command_text>")
            cooldown()
    elif input == message.lower().split()[0]:
        sendMessage(s, "@" + user + " Only the channel owner and moderators may use the !addcommand command.")
        cooldown()

#Deletes a specified command from commands.txt
def deleteCommand(input):
    if input == message.lower().split()[0] and user == CHANNEL:
        a = open("commands.txt", "r")
        commandList = a.readlines()
        commandNames = []
        for line in commandList:
            commandNames.append(line.split()[0].lower().strip(";"))
        a.close()

        try:
            command = message.split()[1].strip().lower()
        except IndexError as err:
            sendMessage(s, "Error: Invalid syntax for the !delete command. Correct syntax is: !delete <command_name>")
            cooldown()
            return

        try:
            message.split()[2]
            if message.split()[2]:
                sendMessage(s, "Error: Invalid syntax for the !delete command. Correct syntax is: !delete <command_name>")
                cooldown()
                return
        except IndexError as err:
            pass

        if command in commandNames:
            for commandLine in commandList:
                if command == commandLine.split()[0].lower().strip(";"):
                    commandList.remove(commandLine)
            overwriteCommand = open("commands.txt", "w")
            overwriteCommand.writelines(commandList)
            overwriteCommand.close()
            sendMessage(s, "Command {} successfully deleted.".format(command))
            cooldown()
        else:
            sendMessage(s, "Error: Command {} not found".format(command))
            cooldown()

    elif input in message:
        sendMessage(s, "@" + user + " Only the channel owner may use the !delete command.")
        cooldown()

#Adds a quote to quotes.txt
def addQuote(input):
    if input == message.lower().split()[0] and (user == CHANNEL or user in moderators):
        try:
            message.split(input, 1)[-1]
        except IndexError as err:
            sendMessage(s, "Error: Invalid syntax for the !addquote command. Correct syntax is: !addquote <quote>")
            cooldown()
            return

        quote = message.split(input, 1)[-1].strip()
        q = open("quotes.txt", "a")
        q.write(quote + "\n")
        q.close()
        sendMessage(s, "Quote successfully added.")
        cooldown()

    elif input == message.lower().split()[0]:
        sendMessage(s, "@" + user + " Only the channel owner and moderators may use the !addquote command.")
        cooldown()

#Retrieves a quote
def quoteCommand(input):
    if input == message.lower().split()[0]:
        argument = False
        number = None

        try:
            message.split()[2]
        except IndexError as err:
            pass
        else:
            sendMessage(s, "Error: Invalid syntax for the !quote command. Correct syntax is: !quote [optional_integer]")
            cooldown()
            return

        try:
            message.split()[1]
        except IndexError as err:
            pass
        else:
            argument = True
            try:
                number = int(message.split()[1])
            except ValueError as err:
                sendMessage(s, "Error: Invalid syntax for the !quote command. Correct syntax is: !quote [optional_integer]")
                cooldown()
                return
            else:
                if number <= 0:
                    sendMessage(s, "Error: Quote number must not be zero or negative")
                    cooldown()
                    return

        q = open("quotes.txt", "r")
        quoteList = q.readlines()
        q.close()

        if len(quoteList) > 0:
            if argument == True:
                number = number - 1
            elif argument == False:
                randomNumber = random.randint(0, len(quoteList) - 1)
                number = randomNumber
            try:
                quote = quoteList[number]
            except IndexError as err:
                sendMessage(s, "Quote #" + str(number + 1) + " not found.")
                cooldown()
                return

            sendMessage(s, "Quote #" + str(number + 1) + ": " + quote)
            cooldown()

        elif len(quoteList) == 0:
            sendMessage(s, "No quotes found.")
            cooldown()

#Tells user how long they've been following the channel
def followAge(input):
    if input == message.lower().split()[0]:
        messageSplit = message.lower().split()
        try:
            messageSplit[1]
        except IndexError as err:
            follower = user
        else:
            follower = messageSplit[1]

        try:
            url = "https://api.twitch.tv/kraken/users/{}/follows/channels/{}".format(getUserID(follower), getUserID(CHANNEL))
            hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            sendMessage(s, follower + " is not following " + CHANNEL + ".")
            return

        readable = response.read().decode('utf-8')
        lst = loads(readable)

        now = datetime.datetime.now()
        date = datetime.datetime.strptime(lst["created_at"].split('T')[0], '%Y-%m-%d')

        age = now - date
        age = str(age)
        age_in_days = int(age.split()[0])
        years = divmod(age_in_days, 365)
        months = divmod(years[1], 30)
        days = months[1]
        if years[0] > 0:
            sendMessage(s, follower + " has been following " + CHANNEL.title() + " for " + str(years[0]) + (" year, " if years[0] == 1 else " years, ") + str(months[0]) + (" month, " if months[0] == 1 else " months, ") + str(days) + (" day." if days == 1 else " days."))
        elif months[0] > 0:
            sendMessage(s, follower + " has been following " + CHANNEL.title() + " for " + str(months[0]) + (" month, " if months[0] == 1 else " months, ") + str(days) + (" day." if days == 1 else " days."))
        else:
            sendMessage(s, follower + " has been following " + CHANNEL.title() + " for " + str(days) + (" day." if days == 1 else " days."))

        cooldown()
        return

#Returns the stream uptime
def upTime(input):
    if input == message.lower().strip():
        #Get the uptime from the Twitch API
        try:
            url = "https://api.twitch.tv/kraken/streams/{}".format(getUserID(CHANNEL))
            hdr = {'Client-ID': CLIENT_ID, 'Accept': 'application/vnd.twitchtv.v5+json'}
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            raise LookupError('User not found')
            return
        readable = response.read().decode('utf-8')
        stream_info = loads(readable)
        stream = stream_info["stream"]

        if stream == None:
            sendMessage(s, CHANNEL.title() + " is not live.")
            cooldown()
            return
        elif stream != None:
            pass

        createdAt = datetime.datetime.strptime(stream["created_at"][11:19], '%H:%M:%S').time()
        now = datetime.datetime.now().time()
        dateTimeCreatedAt = datetime.datetime.combine(datetime.date.today(), createdAt)
        dateTimeCreatedAtUTC = timezone('UTC').localize(dateTimeCreatedAt)
        dateTimeNow = datetime.datetime.combine(datetime.date.today(), now)
        dateTimeNowEST = timezone('US/Eastern').localize(dateTimeNow)
        dateTimeUptime = dateTimeNowEST - dateTimeCreatedAtUTC

        uptime_hours = str(int(str(dateTimeUptime).split(':')[0]))
        uptime_min = str(int(str(dateTimeUptime).split(':')[1]))

        if int(uptime_hours) == 0:
            sendMessage(s, CHANNEL.title() + " has been live for " + uptime_min + (" minute." if uptime_min == '1' else " minutes."))
            cooldown()
            return
        elif int(uptime_hours) > 0:
            sendMessage(s, CHANNEL.title() + " has been live for " + uptime_hours + (" hour, " if uptime_hours == '1' else " hours, ") + uptime_min + (" minute." if uptime_min == '1' else " minutes."))
            cooldown()
            return

#Timer for sending a Discord invite link
def discordTimer(currentTime):
    global discordTimerStartTime
    global chatCount
    delta = currentTime - discordTimerStartTime
    # 60-min timer
    if delta >= 3600 and chatCount >= 5:
        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= 5:
                break
        sendMessage(s, "Discord server: https://discord.gg/neG6pyD")
        discordTimerStartTime = time.time()
        chatCount = 0

#Counts chat messages from users (not Twitch or channel owner)
def chatCounter():
    if user != CHANNEL and user != IDENT:
        global chatCount
        for line in temp:
            if not Console(line):
                chatCount+= 1

#Displays commands
def getCommands(input):
    if input == message.strip().lower():
        sendMessage(s, '/me commands: !daily • !croissants • !top3 • !gamble • !slots • !followage • !uptime • !quote • !discord • !youtube • !donate • !bot')#+' • '.join(listCommand))
        cooldown()

#Mingy Jongo quote response when people mention him in chat
def mingyResponse(input):
        if input in message.strip().lower() and "!croissants" not in message.strip().lower() and "!award" not in message.strip().lower() and "!add" not in message.strip().lower():
            global mingyTimer
            #Aborts if 10 minutes have not yet passed since last Mingy response
            if not (time.time() - mingyTimer) > 600:
                return
            mingy_jongo_quotes = [
            "Hello, %s. Mumbo has big surprise for you." % user,
            "Har-har-harrr! Foolish %s, you fell straight into my trap!" % user,
            "I'm not that pathetic shaman you think I am! I'm Mingy Jongo and your worthless quest ends here, %s..." % user,
            "Foolish %s, why do you return? A few more shocks from my stick seem necessary..." % user,
            "As you see, %s, there's no escape and resistance is futile!" % user
            ]
            randomNumber = random.randint(0, len(mingy_jongo_quotes) - 1)
            randomQuote = mingy_jongo_quotes[randomNumber]
            #2 second delay for realism
            abort_after = 2
            start = time.time()
            while True:
                delta = time.time() - start
                if delta >= abort_after:
                    break
            sendMessage(s, randomQuote)
            mingyTimer = time.time()
            cooldown()

#Awards points to users (Channel owner only)
def pointAward(input):
    if user == CHANNEL:
        messageSeparated = message.lower().split()
        if input == messageSeparated[0]:
            try:
                recipient = str(messageSeparated[1])
                amount = int(messageSeparated[2])

            except (IndexError, ValueError) as err:
                sendMessage(s, "Error: Invalid syntax for the !award command. Correct syntax is: !award <user> <amount>")
                return

            if recipient == IDENT:
                sendMessage(s, "I cannot receive Croissants.")
                return
            elif (recipient in viewers) or (recipient in moderators) or (recipient in vips):
                pass
            elif recipient == CHANNEL:
                sendMessage(s, "The channel owner may not receive Croissants.")
                return
            else:
                sendMessage(s, "Error: Recipient not present")
                return

            pointGiver(recipient, amount)
            sendMessage(s, recipient + " has received " + str(amount) + (" Croissant." if amount == 1 else " Croissants.") + " " + crsnt)

    elif input in message.lower().strip() and user != CHANNEL:
        sendMessage(s, "@" + user + " Only the channel owner may use the !award command.")
        cooldown()

#Function that give points to users
def pointGiver(recipient, amount):
    pointsFile = open('points.txt', 'r+')
    lines = pointsFile.readlines()
    pointsFile.truncate(0)
    pointsFile.close()

    nameList = []
    for line in lines:
        lineSplit = line.split()
        name = lineSplit[0]
        nameList.append(name)

    if recipient not in nameList:
        with open("points.txt", "a") as f:
            f.write(recipient + " " + str(amount) + "\n")

    elif recipient in nameList:
        for line in lines:
            lineSplit = line.split()
            if recipient == lineSplit[0]:
                pointsFile = open("points.txt", "a")
                person, points = line.split()
                points = int(points)
                # Protection from negative
                if (points + amount) <= 0:
                    points = 0
                else:
                    points = points + amount
                points = str(points)
                pointsFile.write(person + " " + points + "\n")
                pointsFile.close()
                break

    with open("points.txt", "a") as f:
        for line in lines:
            lineSplit = line.split()
            if recipient != lineSplit[0]:
                f.write(line)

#Returns the amount of points a specified user has
def points(username):
    notZero = False
    with open("points.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            name = line.split()[0]
            if username == name:
                points = int(line.split()[1])
                notZero = True

    if notZero == False:
        return 0
    elif notZero == True:
        return points

#Returns how many points the user of the command has, or how many points the specified argument has
def pointsAmount(input):
    if input == message.strip().lower():
        with open("points.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                name = line.split()[0]
                if user == name:
                    points = line.split()[1]
                    sendMessage(s, user + " currently has " + points + (" Croissant." if points == '1' else " Croissants.") + " " + crsnt)
                    cooldown()
                    return
        sendMessage(s, user + " currently has 0 Croissants.")
        cooldown()
    elif input == message.lower().split()[0]:
        try:
            message.lower().split()[2]
            sendMessage(s, "Error: Invalid syntax for the !croissants command. Correct syntax is: !croissants [optional_user]")
            cooldown()
        except IndexError as err:
            arg = message.lower().split()[1]
            with open("points.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    name = line.split()[0]
                    if arg == name:
                        points = line.split()[1]
                        sendMessage(s, arg + " currently has " + points + (" Croissant." if points == '1' else " Croissants.") + " " + crsnt)
                        cooldown()
                        return
            sendMessage(s, arg + " currently has 0 Croissants.")
            cooldown()

#Returns top 3 scores on the point leaderboard along with which users have those scores and any ties
def topThree(input):
    if input == message.lower().strip():
        pointsFile = open("points.txt", "r")
        lines = pointsFile.readlines()
        pointsFile.close()

        leaderboard = {}

        for line in lines:
            lineSplit = line.split()
            leaderboard[lineSplit[0]] = int(lineSplit[1])

        #Get 1st place score and list of users who have it, then delete them from the leaderboard dictionary
        if leaderboard:
            first_score = max(leaderboard.values())
            first_placers = [k for k, v in leaderboard.items() if v == first_score]
            for person in first_placers:
                del leaderboard[person]

        #Get 2nd place score and list of users who have it, then delete them from the leaderboard dictionary
        if leaderboard:
            second_score = max(leaderboard.values())
            second_placers = [k for k, v in leaderboard.items() if v == second_score]
            for person in second_placers:
                del leaderboard[person]

        #Get 3rd place score and list of users who have it
        if leaderboard:
            third_score = max(leaderboard.values())
            third_placers = [k for k, v in leaderboard.items() if v == third_score]

        try:
            third_score
        except NameError as err:
            third_score = None
        try:
            second_score
        except NameError as err:
            second_score = None
        try:
            first_score
        except NameError as err:
            first_score = None

        if third_score:
            sendMessage(s, "1st: " + ", ".join(first_placers) + " (" + str(first_score) + " Croissants). 2nd: " + ", ".join(second_placers) + " (" + str(second_score) + " Croissants). 3rd: " + ", ".join(third_placers) + " (" + str(third_score) + " Croissants).")
        elif second_score:
            sendMessage(s, "1st: " + ", ".join(first_placers) + " (" + str(first_score) + " Croissants). 2nd: " + ", ".join(second_placers) + " (" + str(second_score) + " Croissants).")
        elif first_score:
            sendMessage(s, "1st: " + ", ".join(first_placers) + " (" + str(first_score) + " Croissants).")
        else:
            sendMessage(s, "The leaderboard is currently empty.")

        cooldown()

#Awards a random amount of points to users (between 1 and 5) once per session
def dailyPoints(input):
    if input == message.strip().lower() and user != CHANNEL:
        global dailyList
        if user in dailyList:
            sendMessage(s, "@" + user + " You may only use the !daily command once per day.")

        elif user not in dailyList:
            randomPoints = random.randint(1, 10)

            pointsFile = open('points.txt', 'r+')
            lines = pointsFile.readlines()
            pointsFile.truncate(0)
            pointsFile.close()

            nameList = []
            for line in lines:
                lineSplit = line.split()
                name = lineSplit[0]
                nameList.append(name)

            if user not in nameList:
                with open("points.txt", "a") as f:
                    f.write(user + " " + str(randomPoints) + "\n")
                    sendMessage(s, user + " has received a daily bonus of " + str(randomPoints) + (" Croissant." if randomPoints == 1 else " Croissants."))

            elif user in nameList:
                for line in lines:
                    lineSplit = line.split()
                    if user == lineSplit[0]:
                        pointsFile = open("points.txt", "a")
                        person, points = line.split()
                        points = int(points)
                        points = points + randomPoints
                        points = str(points)
                        pointsFile.write(person + " " + points + "\n")
                        pointsFile.close()
                        sendMessage(s, user + " has received a daily bonus of " + str(randomPoints) + (" Croissant." if randomPoints == 1 else " Croissants."))
                        break

            with open("points.txt", "a") as f:
                for line in lines:
                    lineSplit = line.split()
                    if user != lineSplit[0]:
                        f.write(line)

            #Now add user to the daily list
            dailyList.append(user)
            cooldown()

    elif input == message.strip().lower() and user == CHANNEL:
        sendMessage(s, "@" + user + " The channel owner may not use the !daily command.")
        return

#If user wins the lottery, they double their specified wager of points
def gamblePoints(input):
    if input == message.lower().split()[0] and user != CHANNEL:
        messageSeparated = message.lower().split()
        global gambleList
        now = time.time()
        if user not in gambleList:
            try:
                wager = int(messageSeparated[1])
            except IndexError as err:
                sendMessage(s, "Error: Invalid syntax for the !gamble command. Correct syntax is: !gamble <wager>")
                return
            except ValueError as err:
                if messageSeparated[1] == 'all':
                    wager = 'all'
                else:
                    sendMessage(s, "Error: Invalid syntax for the !gamble command. Correct syntax is: !gamble <wager>")
                    return

            if wager == 'all':
                pass
            else:
                if wager <= 0:
                    sendMessage(s, "Error: Wager must not be zero or negative")
                    cooldown()
                    return

            pointsFile = open("points.txt", "r")
            lines = pointsFile.readlines()
            pointsFile.close()

            nameList = []
            for line in lines:
                lineSplit = line.split()
                name = lineSplit[0]
                nameList.append(name)

            if user not in nameList:
                sendMessage(s, "@" + user + " Insufficient Croissants")
                return
            elif user in nameList:
                for line in lines:
                    lineSplit = line.split()
                    if user == lineSplit[0]:
                        points = lineSplit[1]
                        points = int(points)
                        # if user wrote "all"
                        if wager == 'all':
                            wager = points
                if wager <= points:
                    pass
                elif wager > points:
                    sendMessage(s, "@" + user + " Insufficient Croissants")
                    return

            number = random.randint(1, 2)
            win = False
            if number != 1:
                pass
            elif number == 1:
                win = True

            if win:
                newPoints = points + wager
                pointsFile = open('points.txt', 'r+')
                lines = pointsFile.readlines()
                pointsFile.truncate(0)
                pointsFile.close()
                for line in lines:
                    lineSplit = line.split()
                    if user == lineSplit[0]:
                        pointsFile = open("points.txt", "a")
                        pointsFile.write(user + " " + str(newPoints) + "\n")
                        pointsFile.close()
                        sendMessage(s, "WIN! " + user + " has received " + str(wager) + (" Croissant." if wager == 1 else " Croissants."))
                        break

                with open("points.txt", "a") as f:
                    for line in lines:
                        lineSplit = line.split()
                        if user != lineSplit[0]:
                            f.write(line)
                gambleList.append(user)
                gambleList.append(now)

            elif not win:
                newPoints = points - wager
                pointsFile = open('points.txt', 'r+')
                lines = pointsFile.readlines()
                pointsFile.truncate(0)
                pointsFile.close()
                for line in lines:
                    lineSplit = line.split()
                    if user == lineSplit[0]:
                        pointsFile = open("points.txt", "a")
                        pointsFile.write(user + " " + str(newPoints) + "\n")
                        pointsFile.close()
                        sendMessage(s, "LOSE! " + user + " has lost " + str(wager) + (" Croissant." if wager == 1 else " Croissants."))
                        break

                with open("points.txt", "a") as f:
                    for line in lines:
                        lineSplit = line.split()
                        if user != lineSplit[0]:
                            f.write(line)
                gambleList.append(user)
                gambleList.append(now)

        elif user in gambleList:
            playedAt = gambleList[gambleList.index(user) + 1]
            delta = now - playedAt
            #10min
            if delta >=  600:
                num = gambleList.index(user)
                del gambleList[num]
                del gambleList[num]
                gamblePoints('!gamble')
            else:
                remaining = 600 - delta
                min = divmod(remaining, 60)
                sec = min[1]
                sendMessage(s, "@" + user + " You may gamble again in " + str(int(min[0])) + (" minute, " if min[0] == 1 else " minutes, ") + str(int(sec)) + (" second." if sec == 1 else " seconds."))
        cooldown()

    elif input == message.lower().split()[0] and user == CHANNEL:
        sendMessage(s, "@" + user + " The channel owner may not use the !gamble command.")
        return

#Awards all current viewers 3 points every 15 minutes
def pointTimer(currentTime):
    global pointTimerStartTime
    delta = currentTime - pointTimerStartTime
    #15-min timer
    if delta >= 900:
        recipients = []
        blacklisted = []
        blacklistFile = open("blacklist.txt", "r")
        blacklistedList = blacklistFile.readlines()
        blacklistFile.close()
        for line in blacklistedList:
            blacklisted.append(line.split()[0])

        all_viewers = viewers + vips + moderators
        for person in all_viewers:
            if person not in blacklisted and person != IDENT:
                recipients.append(person)

        pointsFile = open('points.txt', 'r+')
        lines = pointsFile.readlines()
        pointsFile.truncate(0)
        pointsFile.close()

        nameList = []
        for line in lines:
            lineSplit = line.split()
            name = lineSplit[0]
            nameList.append(name)

        for person in recipients:
            if person not in nameList:
                with open("points.txt", "a") as f:
                    f.write(person + " 1\n")

            elif person in nameList:
                for line in lines:
                    lineSplit = line.split()
                    if person == lineSplit[0]:
                        pointsFile = open("points.txt", "a")
                        person, points = line.split()
                        points = int(points)
                        points = points + 3
                        points = str(points)
                        pointsFile.write(person + " " + points + "\n")
                        pointsFile.close()

        with open("points.txt", "a") as f:
            for line in lines:
                lineSplit = line.split()
                if lineSplit[0] not in recipients:
                    f.write(line)
        pointTimerStartTime = time.time()

def pointsBackup():
    if delta > 1800:
        with open('points.txt', 'r') as f:
            lines = f.readlines()
        with open('pointsbackup.txt', 'w') as n:
            n.writelines(lines)


#Bonk
def bonk(input):
    if input in message.lower():
        global bonkTimerStartTime
        delta = time.time() - bonkTimerStartTime
        if ('nicebonk' == message.lower().strip() or 'bonktime' == message.lower().strip()) and (delta > 60):
            responses = ['NiceBonk', 'BonkTime', 'Yamyar']
            number = random.randint(1, len(responses)) - 1
            #3 second delay for realism
            abort_after = 3
            start = time.time()
            while True:
                delta = time.time() - start
                if delta >= abort_after:
                    break
            #Send response
            sendMessage(s, responses[number])
            bonkTimerStartTime = time.time()
            cooldown()

def pyramid(input):
    if isinstance(input, str):
        abort_after = 0

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input + " " + input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input + " " +  input + " " + input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s,  input + " " + input + " " +  input + " " +  input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s,  input + " " +  input + " " +  input + " "  +  input + " "  +  input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input + " " + input + " " +  input + " " +  input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input + " " + input + " " +  input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input + " " + input)

        start = time.time()
        while True:
            delta = time.time() - start
            if delta >= abort_after:
                break
        sendMessage(s, input)

        return

def slots(input):
    if input == message.lower().strip():
        global slotsList
        now = time.time()
        if user not in slotsList:
            prize = slotMachine()
            if prize == 'Jackpot':
                sendMessage(s, "@" + user + " JACKPOT! You won 300 Croissants!")
                if user != CHANNEL and user != IDENT:
                    pointGiver(user, 300)
                    slotsList.append(user)
                    slotsList.append(now)

            elif prize == 'FreePlay':
                sendMessage(s, "@" + user + " You won a Free Play! jigAYAYA Play again!")

            elif prize == 'LosePoints':
                sendMessage(s, "@" + user + " BONK! You lost 100 Croissants! NiceBonk")
                if user != CHANNEL and user != IDENT:
                    pointGiver(user, -100)
                    slotsList.append(user)
                    slotsList.append(now)

            elif prize == 'MiniJackpot':
                sendMessage(s, "@" + user + " WIN! You won 50 Croissants! WellDone")
                if user != CHANNEL and user != IDENT:
                    pointGiver(user, 50)
                    slotsList.append(user)
                    slotsList.append(now)

            elif prize == 'Pyramid':
                if user != CHANNEL and user != IDENT:
                    slotsList.append(user)
                    slotsList.append(now)
                sendMessage(s, "Loading...")
                #Ten second delay
                start = time.time()
                while True:
                    delta = time.time() - start
                    if delta >= 10:
                        break
                pyramid("Mhmm")

            elif prize == 'Item':
                if user != CHANNEL and user != IDENT:
                    slotsList.append(user)
                    slotsList.append(now)
                sendMessage(s, '@' + user + " This reward isn't implemented yet lol :) sorry GetOut")

            else:
                if user != CHANNEL and user != IDENT:
                    slotsList.append(user)
                    slotsList.append(now)

        elif user in slotsList:
            playedAt = slotsList[slotsList.index(user) + 1]
            delta = now - playedAt
            #10min
            if delta >=  600:
                num = slotsList.index(user)
                del slotsList[num]
                del slotsList[num]
                slots('!slots')
            else:
                remaining = 600 - delta
                min = divmod(remaining, 60)
                sec = min[1]
                sendMessage(s, "@" + user + " You may use the slots again in " + str(int(min[0])) + (" minute, " if min[0] == 1 else " minutes, ") + str(int(sec)) + (" second." if sec == 1 else " seconds."))

        cooldown()

def slotMachine():
    options = ['jigAYAYA', 'jigAYAYA', 'jigAYAYA', 'Mhmm', 'Mhmm', 'BonkTime', 'ExpansionPak', 'ExpansionPak', 'ExpansionPak', 'GodsIntendedConsole']
    slot1 = random.choice(options)
    slot2 = random.choice(options)
    slot3 = random.choice(options)
    prize = None
    if (slot1 == slot2) and (slot1 == slot3) and (slot1 == 'jigAYAYA'):
        prize = 'FreePlay'
    elif (slot1 == slot2) and (slot1 == slot3) and (slot1 == 'BonkTime'):
        prize = 'LosePoints'
    elif (slot1 == slot2) and (slot1 == slot3) and (slot1 == 'Mhmm'):
        prize = 'Pyramid'
    elif (slot1 == slot2) and (slot1 == slot3) and (slot1 == 'GodsIntendedConsole'):
        prize = 'Jackpot'
    elif (slot1 == slot2) and (slot1 == slot3) and (slot1 == 'ExpansionPak'):
        prize = 'Item'
    elif (slot1 == slot2 and slot1 == 'GodsIntendedConsole') or (slot1 == slot3 and slot1 == 'GodsIntendedConsole') or (slot2 == slot3 and slot2 == 'GodsIntendedConsole'):
        prize = 'MiniJackpot'
    sendMessage(s, slot1 + " " + slot2 + " " + slot3)
    return prize

#Quits the bot program
def quitCommand(input):
    if input == message.strip().lower() and user == CHANNEL:
        sendMessage(s, "/me has disconnected.")
        quit()
    elif input == message.strip().lower():
        sendMessage(s, "@" + user + " Only the channel owner may use the !quit command.")
        cooldown()

def joinRaffle(input):
    if input == message.lower().strip() and user != CHANNEL and raffleStatus == True:
        global rafflers
        if user not in rafflers:
            rafflers.append(user)
        elif user in rafflers:
            sendMessage(s, "@" + user + " You may only enter the raffle once.")
        cooldown()
        return
    elif input == message.lower().strip() and raffleStatus == False:
        sendMessage(s, "@" + user + " There is no raffle in progress.")
        cooldown()
        return

def pickWinner():
    global rafflers
    if len(rafflers) > 0:
        winner = random.choice(rafflers)
        payout = len(rafflers) * 5
        pointGiver(winner, payout)
        sendMessage(s, "Congratulations, " + winner + "! You won the raffle! (" + str(payout) + " Croissants)")
        rafflers.clear()
        return
    elif len(rafflers) == 0:
        sendMessage(s, "The raffle has now ended. There were absolutely no entrants. How sad.")
        return

def raffleCheck(status):
    global raffleTimerStartTime
    global raffleStatus
    if status == True:
        now = time.time()
        delta = now - raffleTimerStartTime
        if delta >= 120:
            raffleTimerStartTime = 0
            raffleStatus = False
            pickWinner()

def startRaffle(input):
    if input == message.lower().strip() and user == CHANNEL:
        global raffleTimerStartTime
        global raffleStatus
        raffleStatus = True
        raffleTimerStartTime = time.time()
        sendMessage(s, CHANNEL.title() + " has started a raffle! Join with !enter. The winner will be announced in 2 minutes.")
        return

#Start of program
s = openSocket()
joinRoom(s)
readbuffer = ""

#Timers
discordTimerStartTime = time.time()
pointTimerStartTime = time.time()

#Starting lists and variables
dailyList = []
gambleList = []
slotsList = []
chatCount = 0
bonkTimerStartTime = 0
mingyTimer = 0

#Raffle
rafflers = []
raffleTimerStartTime = 0
raffleStatus = False

#Emoji
crsnt = str(u'\U0001f950')
moneybag = str(u'\U0001f4b0')
cry = str(u'\U0001f622')

#Loop that keeps the chat active and updates chatlines.
while True:

    #discordTimer(time.time())
    pointTimer(time.time())
    raffleCheck(raffleStatus)

    readbuffer = s.recv(1024)
    readbuffer = readbuffer.decode()
    temp = readbuffer.split("\n")
    readbuffer = readbuffer.encode()
    readbuffer = temp.pop()


    for line in temp:
        try:
            print(line)
        except OSError as err:
            print('OSError: Invalid symbol')
            continue
        #Prevents afk kick from server.
        if "PING" in line and Console(line):
            msgg = "PONG tmi.twitch.tv\r\n".encode()
            s.send(msgg)
            print(msgg)
            break
        #Prints chat lines (in the console) in a more readable fashion.
        user = getUser(line)
        message = getMessage(line)
        print(user + " said: " + message)

        #List of Chatters, Moderators and VIPs
        response = urlopen('https://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL))
        readable = response.read().decode('utf-8')
        chatlist = loads(readable)
        chatters = chatlist['chatters']
        moderators = chatters['moderators']
        vips = chatters['vips']
        viewers = chatters['viewers']

        #Makes dict of commands from command.txt
        commands = {}
        listCommand = []
        commandFile = open("commands.txt", "r")
        commandList = commandFile.readlines()
        commandFile.close()
        for command in commandList:
            try:
                commandInput, commandOutput = command.split(";")
                commands[commandInput] = commandOutput
            except ValueError as err:
                sendMessage(s, "Error: Invalid command in commands file")
                cooldown()

        #Loops dict through basicCommand function and creates a list of commands.
        for input, output in commands.items():
            basicCommand(input, output)
            listCommand.append(input)

        #Add command functions below.
        getCommands('!commands')
        addCommand('!addcommand')
        addQuote('!addquote')
        quoteCommand('!quote')
        deleteCommand('!deletecommand')
        followAge('!followage')
        upTime('!uptime')
        pointAward('!award')
        pointsAmount('!croissants')
        dailyPoints('!daily')
        gamblePoints('!gamble')
        topThree('!top3')
        slots('!slots')
        startRaffle('!raffle')
        joinRaffle('!enter')
        mingyResponse('mingy')
        bonk('bonk')
        quitCommand('!quit')
        chatCounter()
        continue
