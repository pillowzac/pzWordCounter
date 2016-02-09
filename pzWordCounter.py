#
# An app that counts the instances of words in a given directory
#
import Tkinter, tkFileDialog, Tkconstants, os, ttk, tkMessageBox, tkFont, re

from Tkinter import *

class Application(Frame):
	
	def __init__(self, master):
		Frame.__init__(self,master,bg="#f2f2f2")
		self.pack(side=TOP)
		self.place(relwidth=1,relheight=1)
		self.button_clicks = 0 #holder for click count
		self.fname = ""
		self.caseCheckbuttonSensitive = IntVar()
		self.create_widgets()
		
	def create_widgets(self):
		#create over/under paned window
		self.panel = PanedWindow(orient=VERTICAL)
		self.panel.pack(fill=BOTH, expand=1)
		self.panel.place(relwidth=1,relheight=1)
		
		# TOP FRAME
		# Populate the top pane
		self.listFrame = Frame(self.panel)
		self.listFrame.pack(side=TOP)
		self.listFrame.place(relwidth=1.0,height=126)
		self.panel.paneconfigure(self.listFrame, height=126, minsize=126)
		
		# SEARCH PATH
		#label to describe search directory
		self.pathLabel = Label(self.listFrame,text="Search Directory:", anchor=E)
		self.pathLabel.pack(side=LEFT)
		self.pathLabel.place(relwidth=0.2,height=28,y=10)
		#entry to hold directory path
		self.path = Entry(self.listFrame,bg="#f2f2f2",justify="center")
		self.path.insert(END,"")
		self.path.pack(side=LEFT)
		self.path.place(relwidth=0.6,relx=0.2,height=28,y=10)
		#button to browse for search directory
		self.pathButton = Button(self.listFrame,bg="#f2f2f2",relief=GROOVE, text="Select Directory")
		self.pathButton["command"] = self.askdirectory
		self.pathButton.pack(side=LEFT)
		self.pathButton.place(relwidth=0.19,relx=0.804,height=28,y=10)
		
		# WORDS TO SEARCH
		#label to describe words to search
		self.wordLabel = Label(self.listFrame,text="Words to Count:", anchor=E)
		self.wordLabel.pack(side=LEFT)
		self.wordLabel.place(relwidth=0.2,height=28,y=38)
		#entry to hold the space-delimited words to search for
		self.words = Entry(self.listFrame,bg="#f2f2f2",justify="center")
		self.words.insert(END,"")
		self.words.pack(side=LEFT)
		self.words.place(relwidth=0.6,relx=0.2,height=28,y=38)
		#label to describe how to format search word entry
		self.spaceLabel = Label(self.listFrame,text="(separate search words with a space)", anchor=N)
		self.spaceLabel.pack(side=LEFT)
		self.spaceLabel.place(relwidth=1,height=28,y=68)
		
		#case sensitive compare check
		self.caseCheckbutton = Checkbutton(self.listFrame, text="Case Sensitive",variable=self.caseCheckbuttonSensitive)
		self.caseCheckbutton.pack(side=LEFT)
		self.caseCheckbutton.place(relx=0.8,relwidth=0.2,height=28,y=40)
		
		# GO and OPEN OUTPUT buttons
		#button to kick off the search
		self.goButton = Button(self.listFrame,relief=GROOVE, text="Start!")
		self.goButton["command"] = self.do_count
		self.goButton.pack(side=LEFT)
		self.goButton.place(relwidth=0.19,relx=0.804,height=28,y=68)
		#button to open the output csv file
		self.csvButton= Button(self.listFrame,text=self.fname,fg="blue")
		self.csvButton["command"] = self.open_ouput_file
		self.csvButton.pack(side=LEFT)
		self.csvButton.place(relwidth=0,relx=0.2,height=28,y=96)

		#plop the interface elements into the top frame
		self.panel.add(self.listFrame)
		#forget method to initialize showing of button after output is created
		self.csvButton.pack_forget()
		
		# BOTTOM FRAME
		# Populate the bottom pane with a tree to show our search result count
		self.wordFrame = Frame(self.panel,bg="#f2f2f2")
		self.wordFrame.pack(fill=X, padx=5, pady=5)
		#create the tree and scroll bars
		self.resultsTree = ttk.Treeview(self.wordFrame, show="headings")
		ysb = Scrollbar(self.wordFrame, orient='vertical', command=self.resultsTree.yview)
		xsb = Scrollbar(self.wordFrame, orient='horizontal', command=self.resultsTree.xview)
		self.resultsTree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
		ysb.pack(side=RIGHT,fill=Y)
		xsb.pack(side=BOTTOM,fill=X)
		self.resultsTree.pack(fill=X,side=LEFT)
		self.resultsTree.place(relwidth=1,relheight=1)
		#add the tree to the lower panel
		self.panel.add(self.wordFrame)
		
#-- END Create Widgets
		
	#get the directory to search
	def askdirectory(self):
		filename = tkFileDialog.askdirectory(parent=self,initialdir=self.path.get(),title='Select a directory of files to search')
		if filename:
			self.path.delete(0,END)
			self.path.insert(0,filename)
    		return
	
	#open the output file
	def open_ouput_file(self):
		if len(self.fname)>0:
			os.system("open -e " + self.fname)		
		
	#perform the word count
	def do_count(self):
		#clear the tree
		x = self.resultsTree.get_children()
		for item in x:
			self.resultsTree.delete(item)
		
		#get the path and the words
		path = self.path.get()
		words = self.words.get()
		
		#return if not filled out
		if (path=='') or (words==''):
			headers = ["warning","description"]
			self.resultsTree["columns"] = headers
			self.resultsTree.heading("warning",text="Alert")
			self.resultsTree.heading("description",text="Description")
			alertWidth = tkFont.Font().measure("WARNING") + 20
			descWidth = self.resultsTree.winfo_width() - alertWidth
			descWidthMinWidth = 0
			
			if (path==''):
				self.resultsTree.insert("" , 0,  text="WARNING", values=(['WARNING','No directory selected.']))
				descWidthMinWidth = tkFont.Font().measure('No directory selected.')
			if (words==''):
				self.resultsTree.insert("" , 0,  text="WARNING", values=(['WARNING','No words to search for.']))
				descWidthMinWidth = tkFont.Font().measure('No words to search for.')

			self.resultsTree.column('warning',minwidth=alertWidth,width=alertWidth, anchor=E, stretch=YES)
			self.resultsTree.column('description',minwidth=descWidthMinWidth,width=descWidth, anchor=W, stretch=YES)

			return

		#the file extensions that we can search
		ext = ["txt","m","h","mm","js","csv","tab","html","py","htm"]
		
		#create the search objects
		searchWords = words.split()
		count = []
		headline = []
		headline.append("File")
		
		#open the directory and iterate each file
		listing = os.listdir(path)
		
		for infile in listing:
			#get the file extension
			extension = os.path.splitext(infile)[1][1:]
			#can we read it?
			if	extension in ext:
				#we can!
			   	#open it
				if self.caseCheckbuttonSensitive.get() == 1:			   	
					file  = open(path+'/'+infile, 'r').read()
				else:
					file  = open(path+'/'+infile, 'r').read().lower()
				
				fcount = []
			   	fcount.append(infile)
				for word in searchWords:
					if self.caseCheckbuttonSensitive.get() == 1:
						regex = r'\s%s\b' % re.escape(word)
					else:
						regex = r'\s%s\b' % re.escape(word.lower())

					#regular expression to match the whole word
					matches = re.finditer(regex, file)
					wcount = 0
					for match in re.finditer(regex, file):
						wcount += 1
			   		#wcount = file.count(word)
					fcount.append(str(wcount))
				count.append(fcount)
		
		#set up the headers
		headers = ["File"]
		for	w in searchWords:
			headers.append(w)
			
		self.resultsTree["columns"] = headers
		
		#create the csv output string
		foutput = 'File, ' + ', '.join(searchWords)
		
		# get the minimum width of the first column (holds the filename)
		fileWidth = tkFont.Font().measure("File") + 20
		
		#iterate the entries and add them to our csv output string
		for entry in count:
			out = ', '.join(entry)
			foutput += "\n" + out
			#update the minimum width of the file column
			t = entry[0]
			tw = tkFont.Font().measure(t) + 20
			if tw>fileWidth:
				fileWidth = tw
			#insert the entry into our UI tree
			self.resultsTree.insert("" , 0,  text="", values=(entry))
			
		#layout the UI tree - update column widths to fill the interface window
		self.resultsTree.column("#0", width=0)
		for hword in headers:
			self.resultsTree.heading(hword, text=hword)
			mw = tkFont.Font().measure(hword) + 20
			w = (self.resultsTree.winfo_width() - fileWidth)/(len(headers)-1)
			if hword == "File":
				#file column
				self.resultsTree.column(hword,minwidth=fileWidth,width=fileWidth, anchor=E, stretch=YES)
			else:
				#search word column
				self.resultsTree.column(hword,minwidth=mw,width=w, anchor=S, stretch=YES)

        #save the output to csv
		self.fname = os.path.basename(os.path.normpath(path)) + '.csv'
		outfile = open(self.fname, 'w+')
		outfile.write(foutput)
		
		#update and show the button that opens our output csv file		
		self.csvButton["text"] = "Open " + self.fname		
		self.csvButton.place(relwidth=0.6,height=28,y=96)
		
# Main Loop
if __name__ == "__main__":
	#create the window
	root = Tk()
	root.title("Word Counter")
	root.geometry("800x600")
	root.minsize(640, 480)
	
	# Instantiate the App
	app = Application(root)

	# Kick off the run loop
	root.mainloop()
