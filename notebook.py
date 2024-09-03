import time

class PageManager(object):
	def __init__(self):
		self._notebook = {} #keeps a track of all of the pages created
		self._PageNumber = 1 #It is essentially a key tracker


	def _createPage(self):
#This method is responsible for any page creation which the user wishes to make
		page_info = []
		page_name = input("Enter page name:")
		print("Oooh, look at you! Someone seems to have got the knack of this new-fangled technology. \nYou can add text to your page now. If you wish to add this text later, enter nothing below and then press enter.")
		page_info.append(page_name)
		text = self._AddText()

		if text =="" or text == " " or text == "nothing":
			page_info.append("<no text added>")

		else:
			page_info.append(text)
		print("One more thing left. You have to add tags for your pages!")
		print("Enter your tags.")
		print("Once you think you have added enough tags, enter a blank string below. Your page will then be added to your notebook")
		tags = []
		enoughTags = False

		while enoughTags == False:
			tag = input("#")
			if tag == "" or tag == " " or tag == "a blank string" and len(tags) > 0:
				enoughTags = True
				page_info.append(tags)
				print("Creating...")
			else:
				if tag != "" or tag != " ":
					tags.append(tag)
				else:
					print("You need to enter at least one tag for your page to be created.")
		return page_info,tags


	def _AddText(self):
#This will add text to newly created pages if the user wishes to add text
		txt = input(">")
		return txt

	def _SearchForPage(self,page_title, notebook):
#This method searches the "notebook" by title to see whether the page which the user wishes to edit is present in the "notebook"
		i = 1
		while i <= len(notebook):
			if notebook["Page "+str(i)][0] == page_title:
				return i

			else:
				i+=1
		return False




class TextManager(object):
#This text manager will deal with any existing pages that require text to be added to it.
	def _UpdateText(self,notebook,position):
		new_txt = input("Enter new text:")
		Changing_Page = notebook["Page "+str(position)]
		Changing_Page[1] = new_txt
		notebook.update({"Page "+str(position): Changing_Page})
		print("Your text has been changed.")

		for i in notebook:
			print(str(i)+": "+str(notebook[i]))
		return notebook





class TagManager(object):
#Adds any tags to existing pages
	def __init__(self):
		self._tags = {}

	def _updateTags(self,notebook,position):
		new_tag = input("Enter new tag:")
		print(position)
		Changing_Page = notebook["Page "+str(position)]
		tags_list = Changing_Page[2]

		if new_tag in tags_list:
			print("That tag already exists for that page.")

		else:
			tags_list.append(new_tag)
			Changing_Page[2] = tags_list
			notebook.update({"Page "+str(position): Changing_Page})
			print("Your tag has been added.")
			for i in notebook:
				print(str(i)+": "+str(notebook[i]))
			return notebook






class App(object):
#To bring everything together
	def __init__(self):
		self.__pageManager = PageManager() #Composition aggregation
		self.__tagManager = TagManager()   #Composition aggregation
		self.__textManager = TextManager() #Composition aggregation

	def main(self):
		print("""
__________        ___________           .__        ________                 _______          __          
\______   \       \__    ___/___   ____ |  |__     \_____  \   ____   ____  \      \   _____/  |_  ____  
 |    |  _/  ______ |    |_/ __ \_/ ___\|  |  \     /   |   \ /    \_/ __ \ /   |   \ /  _ \   __\/ __ \ 
 |    |   \ /_____/ |    |\  ___/\  \___|   Y  \   /    |    \   |  \  ___//    |    (  <_> )  | \  ___/ 
 |______  /         |____| \___  >\___  >___|  /   \_______  /___|  /\___  >____|__  /\____/|__|  \___  >
        \/                     \/     \/     \/            \/     \/     \/        \/                 \/ 
""")
		print("\n\nVarun Nayak © 15/03/2022-present\n All rights reserved.")
		print("-------------------------------------------------------------------------------------------------------------")
		print("-------------------------------------------------------------------------------------------------------------\n\n")
		print("Type |help to get a list of all of the commands.")
		print("Your commands have to start with |")
		end = False
		while end == False:
			choice = App.__getChoice(self)
			if choice == "|quit":
				self.__Quit()
			elif choice == "|new_page" or choice == "|np" or choice == "|newpage" or choice == "|new page":
				new_page, tagscreated = self.__pageManager._createPage()
				if len(self.__tagManager._tags) == 0:
					for i in range(0, len(tagscreated)):
						self.__tagManager._tags[tagscreated[i]] = [new_page[0]]
				else:
					for i in range(0, len(tagscreated)):      #Checks whether the tag is existing
						for j in self.__tagManager._tags:
							if tagscreated[i] == j:
								self.__tagManager._tags[j].append(new_page[0])
								tagscreated.remove(tagscreated[i])
							else:
								pass
					for element_left in range (0, len(tagscreated)):
						self.__tagManager._tags[tagscreated[element_left]] = new_page[0]
				for i in self.__tagManager._tags:
					print(str(i)+": "+str(self.__tagManager._tags[i]))
				self.__pageManager._notebook["Page "+str(self.__pageManager._PageNumber)] = new_page
				for i in self.__pageManager._notebook:
					print(str(i)+": "+str(self.__pageManager._notebook[i]))
				self.__pageManager._PageNumber +=1
			elif choice == "|text" or choice == "|txt":
				print("You are now about to edit the text of an existing page.")
				for i in self.__pageManager._notebook:
					print(str(i)+": "+str(self.__pageManager._notebook[i]))
				pagetoedit = input("\n\nEnter the title of the page which has the text (or no text) you wish to edit:")
				isPresent = self.__pageManager._SearchForPage(pagetoedit, self.__pageManager._notebook)
				if int(isPresent) == ValueError:
					print("The page you want to search for hasn't been created.")
				else:
					self.__textManager._UpdateText(self.__pageManager._notebook, isPresent)
			elif choice == "|tag":
				print("You are about to add a new tag to an existing page.")
				for i in self.__pageManager._notebook:
					print(str(i)+": "+str(self.__pageManager._notebook[i]))
				pagewithtagchanging = input("Enter the page title which requires a new tag to be added:")
				isPresent = self.__pageManager._SearchForPage(pagewithtagchanging, self.__pageManager._notebook)
				if int(isPresent) == ValueError:
					print("The page you want to search for hasn't been created.")
				else:
					self.__tagManager._updateTags(self.__pageManager._notebook, isPresent)

	def __getChoice(self):
		#Shows the command line to the user and gets their choice as to what they want to do
		listofcommands = ["|new_page", "|text", "|tag","|quit","|help","|np","|newpage","|new page", "|txt","|display"]
		commands = ["|new_page - Create a new page","|text - Add text to exisiting page","|tag- Create a new tag for an existing page","|quit-End the program "]
		command = input("\nEnter command:").lower()
		if command in listofcommands:
			if command == "|help":
				for i in range(0, len(commands)-1):
					print("\n"+str(commands[i]))
					time.sleep(2)
			else:
				return command
		else:
			return "There is no such command. Try again."


	def __Quit(self):
#To end the program
		quit()


a = App()
a.main()






