import asyncio
import discord
from datetime import datetime

TOKEN = 'Ide írd a token-t'
client = discord.Client()
running = True
csengok = list()

class Csengo():
    def __init__(self, channel_id, class_string):
        self.channel_id = channel_id
        self.class_string = class_string.strip()

async def loop_thread():
    cooldown = 0
    while running:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        day = now.strftime("%a")
        if (day != 'Sat') or (day != 'Sun'):
            day_prefix = ''

            if cooldown > 0:
                cooldown -= 1
            else:
                if current_time in lesson_start:
                    cooldown = 10
                    for csengo in csengok:
                        channel = client.get_channel(csengo.channel_id)
                        try:
                            count = lesson_start[day_prefix + current_time]
                            if csengo.class_string == '-':
                                await channel.send('Elkezdődött a(z) {}. óra!'.format(count))
                            else:
                                lesson = timetable[csengo.class_string][day][count]
                                await channel.send('Elkezdődött a(z) {}. óra: {}!'.format(count, lesson))
                        except:
                            print(csengo.class_string, 'not found')
                if current_time in lesson_end:
                    cooldown = 10
                    for csengo in csengok:
                        channel = client.get_channel(csengo.channel_id)
                        try:
                            count = lesson_end[day_prefix + current_time]
                            if csengo.class_string == '-':
                                await channel.send('Vége a(z) {}. órának!'.format(count))
                            else:
                                print(timetable[csengo.class_string][day][count])
                                await channel.send('Vége a(z) {}. órának!'.format(count))
                                lesson = timetable[csengo.class_string][day][str(int(count)+1)]
                                await channel.send('Következik a(z) {}!'.format(lesson))
                        except:
                            print(csengo.class_string, 'not found')

        await asyncio.sleep(10)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await loop_thread()

#Ezt kell átírni
timetable = {
    '12.A': {
        'Mon': {
            '2': 'Irodalom',
            '3': 'Töri',
            '4': 'Matek',
            '5': 'Biológia',
            '6': 'Média',
            '7': 'Angol'
            },
        'Tue': {
            '1': 'Matek fakt',
            '2': 'Matek fakt',
            '3': 'Angol',
            '4': 'Angol',
            '5': '2. nyelv',
            '6': 'Biológia',
            '7': 'Osztályfőnöki'
            },
        'Wed': {
            '1': '2. nyelv',
            '2': 'Matek',
            '3': 'Irodalom',
            '4': 'Média',
            '5': 'Töri',
            '6': 'Nyelvtan'
            },
        'Thu': {
            '0': 'Tesi',
            '1': 'Tesi',
            '2': 'Matek',
            '3': 'Angol',
            '4': '2. nyelv',
            '5': 'Töri',
            '6': 'Filozófia'
            },
        'Fri': {
            '2': '2. nyelv',
            '3': 'Tesi',
            '4': 'Életvitel',
            '5': 'Irodalom'
            }
        }
    }

lesson_start = {
        '07:25': '0',
        '08:15': '1',
        '09:15': '2',
        '10:15': '3',
        '19:08': '3',
        '11:15': '4',
        '12:25': '5',
        '13:20': '6',
        '14:15': '7'
        }

lesson_end = {
        '08:10': '0',
        '09:00': '1',
        '10:00': '2',
        '11:00': '3',
        '19:12': '3',
        '12:00': '4',
        '13:10': '5',
        '14:05': '6',
        '15:00': '7',
        }

def save_csengok():
    save_file = open('csengok.txt', 'w')
    for csengo in csengok:
        print(str(csengo.channel_id) + ' ' + csengo.class_string + '\n')
        save_file.write(str(csengo.channel_id) + ' ' + csengo.class_string + '\n')
    save_file.close()

def load_csengok():
    save_file = open('csengok.txt')
    for line in save_file:
        split_line = line.split(' ')
        csengok.append(Csengo(int(split_line[0]), split_line[1].strip()))
    save_file.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!stop_csengo'):
        for csengo in csengok:
            if csengo.channel_id == message.channel.id:
                await message.channel.send('Csengő kikapcsolva.')
                csengok.remove(csengo)
                break
        save_csengok()

    if message.content.startswith('!start_csengo'):
        split_command = message.content.split(' ')
        if len(split_command) > 2:
            await message.channel.send('Csak ebben a formátumban adhatsz meg osztályt: "!start_csengo 12.A"')

        if len(split_command) < 2:
            await message.channel.send('Adj meg osztályt is! pl.: "!start_csengo 12.A"')

        for csengo in csengok:
            if csengo.channel_id == message.channel.id:
                await message.channel.send('A csengő itt már be van kapcsolva!')
                return

        csengo = Csengo(message.channel.id, split_command[1].strip())
        csengok.append(csengo)
        save_csengok()
        print('added channel:', message.channel.name)
        await message.channel.send('Csengő bekapcsolva a "{}" csatornában.'.format(message.channel.name))

try:
    load_csengok()
except:
    print('Error while loading file.')
client.run(TOKEN)

