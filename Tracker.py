from datetime import date

class DailyActivityTracker:
	def __init__(self):
		# Log holds all the spent time so far on each activity during the day
		self.log = {'Work':0, 'Sleep':0, 'EE':0, 'Workout':0, 'Self-care':0}
		# Standards holds all the time remaining for each activity 
		self.standards = {'Work': 8, 'Sleep':9, 'EE':3,'Workout':3, 'Self-care':1}
		self.day = date.today()
		try: 
			self.file = open("dailyactivities.txt","x")
		except FileExistsError:
			self.file = open("dailyactivities.txt","a")

	def reset(self):
		self.log = {'Work':0, 'Sleep':0, 'EE':0, 'Workout':0, 'Self-care':0}
		self.standards = {'Work': 8, 'Sleep':9, 'EE':3,'Workout':3, 'Self-care':1}
		self.day = date.today()
		self.print_log()

	def new_day(self):
		self.write_to_file()
		self.reset()
	
	def record(self, activity, time):
		if (time > 0):
			# Ask for replacement from a different activity if remaining time for that activity is run out
			self.log[str(activity)] += time
			self.standards[str(activity)] -= time
			# Calculate the amount of exceeded time by this activity
			total = sum([x if x > 0 else 0 for x in self.standards.values()]) + sum(
				[abs(x) for x in self.log.values()])
			self.print_log()
			if (total != 24):
				print("You exceeded the expected time for", str(activity), "by", str(total - 24), "hours")
			while (total != 24):	
				reduced = input("Please reduce the expected time of another activity:")
				act = str(reduced).split(",")
				if (act[0] == 'reset'):
					tracker.reset()
				elif (act[0] == 'q'):
					exit(0)
				else:
					if (self.standards[str(act[0])] > 0 and float(act[1]) < 0): # only reduce if the activity still has remaining time
						self.standards[str(act[0])] += float(act[1])
						total -= abs(float(act[1]))
					self.print_log()
					if (total != 24):
						print(float(total - 24), "hours still needed to be reduced")

	def print_log(self):
		print("\nWORK:", self.log['Work'] ,"hours.", "Remain:", self.standards['Work'], "hours")
		print("SLEEP:", self.log['Sleep'] ,"hours.", "Remain:", self.standards['Sleep'], "hours")
		print("EAT/ENTERTAINMENT:", self.log['EE'] ,"hours.", "Remain:", self.standards['EE'], "hours")
		print("WORKOUT:", self.log['Workout'] ,"hours.", "Remain: ", self.standards['Workout'], "hours")
		print("SELF-CARE:", self.log['Self-care'] ,"hours.", "Remain:", self.standards['Self-care'], "hours\n")

	def write_to_file(self):
		self.file.write(str(self.day))
		self.file.write("\n")
		self.file.write(str(self.log))
		self.file.write("\n")
		self.file.close()
		self.file = open("dailyactivities.txt","a")

tracker = DailyActivityTracker()
print("Welcome to Daily Activity Tracker")
print("Date today:", tracker.day)
print("Let's have an awesome day today!")
while (True):
	if (tracker.day == date.today()):
		activity = input("Enter your activity and end time as of now: ")
		code = str(activity).split(',')
		if (code[0] == 'reset'):
			tracker.reset()
		elif (code[0] == 'q'):
			exit(0)
		else:
			tracker.record(code[0], float(code[1]))
	else: # Automatically switch to new day and write out past day to log
		tracker.new_day()
		print("Welcome to Daily Activity Tracker")
		print("Date today:", tracker.day)
		print("Let's have an awesome day today!")
		tracker.print_log()

