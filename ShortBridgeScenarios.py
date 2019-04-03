from bridges import *
from car import *

from random import randint
from re import match

def main():
	#thanks to http://patorjk.com/software/taag/
	banner = """
   ▄▄▄▄▄    ▄  █ ████▄ █▄▄▄▄    ▄▄▄▄▀     ███   █▄▄▄▄ ▄█ ██▄     ▄▀  ▄███▄
  █     ▀▄ █   █ █   █ █  ▄▀ ▀▀▀ █        █  █  █  ▄▀ ██ █  █  ▄▀    █▀   ▀
▄  ▀▀▀▀▄   ██▀▀█ █   █ █▀▀▌      █        █ ▀ ▄ █▀▀▌  ██ █   █ █ ▀▄  ██▄▄
 ▀▄▄▄▄▀    █   █ ▀████ █  █     █         █  ▄▀ █  █  ▐█ █  █  █   █ █▄   ▄▀
              █          █     ▀          ███     █    ▐ ███▀   ███  ▀███▀
             ▀          ▀                        ▀
"""
	#Art by David Palmer, thanks to https://www.asciiart.eu/vehicles/cars
	carArt="""

                    ___..................____
           _..--''~_______   _____...----~~~\\
       __.'    .-'~       \\~      [_`.7     \\
 .---~~      .'            \\           __..--\\_
/             `-._          \\   _...~~~_..---~  ~~~~~~~~~~~~--.._
\              /  ~~~~~~----_\`-~_-~~__          ~~~~~~~---.._    ~--.__
 \     _       |==            |   ~--___--------...__          `-   _.--\"\"\"|
  \ __/.-._\   |              |            ~~~~--.  `-._ ___...--~~~_.'|_Y |
   `--'|/~_\\  |              |     _____           _.~~~__..--~~_.-~~~.-~/
     | ||| |\\_|__            |.../.----.._.        | Y |__...--~~_.-~  _/
      ~\\\ || ~|..__---____   |||||  .'~-. \\       |_..-----~~~~   _.~~
        \`-'/ /     ~~~----...|'''|  |/"_"\ \\   |~~'           __.~
         `~~~'                 ~~-:  ||| ~| |\\  |        __..~~
                                   ~~|||  | | \\/  _.---~~
                                     \\\  //  | ~~~
                                      \`-'/  /
                                       `~~~~'
	"""
	print(banner)
	print(carArt)

	#Bridge selection
	choice = ''
	while (not match("[1-4]", choice) or int(choice) not in range(1,5)):
		print('\n' + '#' * 32 + '[ Bridge Scenarios ]' + '#' * 32 + '\n')

		#Scenarios description
		print('\t' * 4 + '1. Unsafe & Unfair')
		print('\t' * 4 + '2. Safe & Unfair')
		print('\t' * 4 + '3. Safe & Fair (Strict mode)')
		print('\t' * 4 + '4. Safe & Fair (Adaptive mode)')

		choice = input('\n' + '\t' * 3 + 'Choose a scenario: ')

	#Input handling
	if int(choice) == 1:
		bridge = UnsafeUnfairBridge()
	elif int(choice) == 2:
		bridge = SafeUnfairBridge()
	elif int(choice) == 3:
		bridge = SafeFairStrictBridge()
	elif int(choice) == 4:
		bridge = SafeFairAdaptiveBridge()


	#Sample size selection
	choice = '0'
	while (not match("[1-7]", choice) or int(choice) not in range(1,8)):
		print('\n' + '#' * 36 + '[ Samples ]' + '#' * 36 + '\n')

		#Samples description
		print('\t' * 3 + '1. Small (5 red + 5 blue cars)')
		print('\t' * 3 + '2. Big (50 red + 50 blue cars)')
		print('\t' * 3 + '3. Huge (500 red + 500 blue cars)')
		print('\t' * 3 + '4. Enormous (5000 red + 5000 blue cars)')
		print('\t' * 3 + '5. Random x (x red + x blue cars)')
		print('\t' * 3 + '6. Random x,y (x red + y blue cars)')
		print('\t' * 3 + '7. Manual x,y (x red + y blue cars)')

		choice = input('\n' + '\t' * 2 + 'Choose a sample size: ')

	#Input handling
	if int(choice) == 1:
		nR = nB = 5
	elif int(choice) == 2:
		nR = nB = 50
	elif int(choice) == 3:
		nR = nB = 500
	elif int(choice) == 4:
		nR = nB = 5000
	elif int(choice) == 5:
		nR = nB = randint(1, 5000)
	elif int(choice) == 6:
		nR = randint(1, 5000)
		nB = randint(1, 5000)
	elif int(choice) == 7:
		nR = '-1'
		nB = '-1'
		while (not match("[0-9]", nR) or int(nR) < 0):
			nR = input('\n' + '\t' * 2 + 'Choose the number of Red cars: ')
		while (not match("[0-9]", nB) or int(nB) < 0):
			nB = input('\n' + '\t' * 2 + 'Choose the number of Blue cars: ')

	#Show bridge headers
	print('\n' + '#' * 34 + '[ Simulation ]' + '#' * 35 + '\n')
	print(bridge)

	#Car threads list
	cars = []

	#Assigning cars to threads whose purpose is to cross the bridge (each car knows it's destination upon creation)
	for i in range(int(nR)):
		red = Car(i, 'Red', bridge)
		cars.append(red)
		red.start()

	for i in range(int(nB)):
		blue = Car(i, 'Blue', bridge)
		cars.append(blue)
		blue.start()

	#Joining each car on main thread execution
	for car in cars:
		car.join()

	#Printing statistics
	print('\n' + '#' * 34 + '[ Statistics ]' + '#' * 35 + '\n')
	print('Total Red cars: ' + str(nR))
	print('Total Blue cars: ' + str(nB))
	print('Total collisions: ' + str(bridge._totalCollisions) + ' (' + str(round(bridge._totalCollisions/(int(nR)+int(nB)) * 100, 2)) + '% of total cars)' )

if __name__ == '__main__':
	main()
