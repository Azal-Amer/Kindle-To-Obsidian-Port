# %%
# open the file'
import datetime
import re
from itertools import groupby
import shutil
import os
# %%
class Quote:
    def __init__(self, title, author, content, location,date,page = 'na',note = False):
        self.title = title
        self.author = author
        self.content = content
        self.location = location
        self.date = date
        self.page = page
        self.note = note
    def __str__(self):
        return f"{self.title} by {self.author} \n {self.content} \n {self.location} \n {self.date} \n {self.page} \n {self.note} \n"
    def markdownBody(self):
        # develop later once we have come up with a markdown format
        # what we want to do is open the markdown file, and replace the content in curly brackets, with the content of the quote
        template = ''
        with open('/Users/amer_/Desktop/KindleProject/Book Template.md','r') as file:
            template = file.read()
            
            file.close()
        template = template.split('<!-- End of Properties -->')[1]
        template = template.replace('{Quote}',self.content)
        markdownNote = ''
        if(self.note !=False and self.note != True):
            markdownNote = f"\n- {self.note}"
        template = template.replace('{Note}',markdownNote)
        if self.page == 'na':
            template = template.replace('{locationData}',self.location)
        else:
            template = template.replace('{locationData}',f"Page {self.page}")
        template = template.replace('{time}',self.date)
        
        formattedDate = datetime.datetime.strptime(self.date, '%A, %B %d, %Y %I:%M:%S %p').strftime('%Y-%m-%d')
        template = template.replace('dateFormat',formattedDate)
        return template
    def markdownTitle(self):
        template = ''
        with open('/Users/amer_/Desktop/KindleProject/Book Template.md','r') as file:
            template = file.read()
            
            file.close()
        template = template.split('<!-- End of Properties -->')[0]
        template = template.replace('{author}',self.author)
        return template


# %%


# %%
def drop_empty(quotes):
    return [quote for quote in quotes if (quote.strip() != '' and quote.strip() != [])]

# %%


# %%

# given a string, extract all the strings enclosed in parenthesis
def extract_author_name(text):
    parenthesisGroup = re.findall(r'\((.*?)\)', text)
    authorBlock = parenthesisGroup[-1]
    author = ''
    if ',' in authorBlock:
        author= (authorBlock.split(',')[1]+' ' +authorBlock.split(',')[0])[1:]
    else:
        author = authorBlock
    # return the string without any of the stuff in parenthesis
    # delete all parts of the string in the parenthesisGroup
    for part in parenthesisGroup:
        text = text.replace(f'({part})', '')
    return author, text[:-1]


# %%
def extractLocationDate(text):
    locationDate = text.split('|')
    page = locationDate[0]
    # remove the 'Your Highlight on page' part
    note = False
    date = ''
    # NOTE THIS IS NOT GOING TO WORK IF WE WANT THE NOTES TOO
    page = page.split('- Your Highlight on page ')
    if len(page) <= 1:

        page = page[0].split('- Your Note on page ')
        # print(page)
        if len(page)<=1:
            page = 'na'
        else:
            page = page[1]
        
        note = True
    else:
        note = False
        page = page[1]
    # Above is for the note condition
    if(page!= 'na'):
        page = int(page)

    
    if(page!= 'na'):
        location = locationDate[1]
        date = locationDate[2].replace('Added on ', '')[1:]
    else:
        location = locationDate[0]
        date = locationDate[1].replace('Added on ', '')[1:]
    
    # NOTE turn the date into a datetime obj for tagging by the day

    return {'page':page,'location':location,'date': date,'isNote':note}
#Format is as follows
# 'Your Highlight on page {location} | Location {null} | Added on {date}'


# is the second index of the quote always the content?
# we'll update this when we add a note to this


# the author title will be the last string with () in it


# %%

# check if "Your Bookmark on " is in the array, make function boolean
def ifBookmark(quote):
    isBookmark = False
    for line in quote:
        if 'Your Bookmark on' in line:
            isBookmark = True
    return isBookmark
# we want to split up the data in the quote into blocks FIRST
def kindleProcessing(data):
    data =data.replace('\\xef\\xbb\\xbf','')
    data = data.replace('\ufeff','')
    quotes = data.split('==========')
    quotes = [drop_empty(quote.split('\n')) for quote in quotes ]
    quoteObjects = []
    for i in range(len(quotes)):
        if(quotes[i]!=[] and ifBookmark(quotes[i])==False ):
            author,title = extract_author_name(quotes[i][0])
            content = quotes[i][2]
            locationDateTime= extractLocationDate(quotes[i][1])
            page = locationDateTime['page']
            location = locationDateTime['location']
            date = locationDateTime['date']
            isNote = locationDateTime['isNote']
            quoteObjects.append(Quote(title,author,content,location,date,page = page,note = isNote))
    return quoteObjects
textDirectory = '/Users/amer_/Desktop/My Clippings.txt'
data = ''
with open(textDirectory, 'r') as file:
    # read the file
    data = file.read()
    # print the data
    file.close()
newQuoteObjects = kindleProcessing(data)

# open up the existing version of the clippings, 
previousDirectory = '/Users/amer_/Documents/Obsidian Vault/Personal/Books/My Clippings.txt'



# %%
def find_updates(old_list, new_list, unique_key):
    old_dict = {obj.__dict__[unique_key]: obj for obj in old_list}
    new_dict = {obj.__dict__[unique_key]: obj for obj in new_list}

    added = [new_dict[key] for key in set(new_dict.keys()) - set(old_dict.keys())]
    removed = [old_dict[key] for key in set(old_dict.keys()) - set(new_dict.keys())]
    modified = [new_dict[key] for key in set(new_dict.keys()) & set(old_dict.keys()) if old_dict[key] != new_dict[key]]

    return added, removed, modified

# %%
# check if the file exists, if it does proceed
if os.path.exists(previousDirectory):
    with open(previousDirectory, 'r') as file:
        # read the file
        previousData = file.read()
        # print the data
        file.close()
    previousQuoteObjects = kindleProcessing(previousData)


    added, removed, modified = find_updates(previousQuoteObjects, newQuoteObjects, 'content')
    quoteObjects=added
else:
    quoteObjects = newQuoteObjects

# %%
unique_titles = set()
for quote in quoteObjects:
    unique_titles.add(quote.title)
unique_titles

# %%

# Okay now we want to group each of the quote objects by title
# Sort the quote objects by title
quoteObjects.sort(key=lambda x: x.title)

# Group the quote objects by title
grouped_quotes = {title: list(quotes) for title, quotes in groupby(quoteObjects, key=lambda x: x.title)}

# %%
unique_titles = set()
for quote in quoteObjects:
    unique_titles.add(quote.title)
unique_titles

# %%
# if a note and a quote have the same location, then make the content of the note object, inside the note section of the quote
#  they will be in the same book so it narrows it down

# first find all the objects that are a note
def withinRange(quote,note):
    stringRange = quote.location.replace('Location ','').split('-')

    lowerBound = int(stringRange[0])
    
    upperBound = int(stringRange[1].replace(' ',''))
    noteLocation = int(note.location.replace('Location ','').split('-')[0])
    boundingCondition = noteLocation >= lowerBound and noteLocation <= upperBound
    if boundingCondition:
        print(lowerBound,noteLocation,upperBound,)
    return boundingCondition

note_objects = [quote for quote in quoteObjects if quote.note]
for note in note_objects:
    for quote in grouped_quotes[note.title]:
        if quote.note == False:
            if withinRange(quote,note):
                quote.note = note.content
                print(quote.__str__())
quoteObjects = [quote for quote in quoteObjects if quote.note == False or quote.note == True]

# %%
# With all this done, we should make a markdown template for it to adapt

# %%
# find all the distict titles


# %%
# given a mapping directory in Obsidian, open it up and construct a dictionary to map our titles from one to another. This is particularly useful if we want to change the title of a book automatically
mapDir = '/Users/amer_/Documents/Obsidian Vault/Personal/Main Book Overview.md'

with open(mapDir,'r') as file:
    mapData = file.read()
    file.close()
mapTable = mapData.split('# Map Table')[1]
mapTable = mapTable.split('\n')
mapTable = [line for line in mapTable if line != '']
# Isolating the Table
mapTable = [line.split('|')[1:3] for line in mapTable ]
# for every item in this 2d array, we want to remove the whitespaces
mapTable = [[item.strip() for item in line] for line in mapTable][2:]
mapTable
# make a dictionary out of this
mapDict = {line[0]:line[1] for line in mapTable}
print(mapDict)
for quote in quoteObjects:
    if quote.title.strip() in mapDict:
        quote.title = mapDict[quote.title.strip()]
quoteObjects.sort(key=lambda x: x.title)
# # Group the quote objects by title
grouped_quotes = {title: list(quotes) for title, quotes in groupby(quoteObjects, key=lambda x: x.title)}

# %%
print(grouped_quotes.keys())

# %%
import os
# Now we want to make the author markdown file
# Make a new file and write the markdown to it

# this is the directory we want to drop the new markdown files into
directory = '/Users/amer_/Documents/Obsidian Vault/Personal/Books/'
files = os.listdir(directory)
existingTitles = []
print(files)
for file in files:
    file = file.replace('.md','').strip()
    existingTitles.append(file)




# %%
existingTitles
# if any of the existing titles is in the mapDict, then we want to rename the file to the new title
for existingTitle in existingTitles:
    if existingTitle.strip() in mapDict:
        os.rename(f'{directory}{existingTitle}.md',f'{directory}{mapDict[existingTitle]}.md')
        print(f'{directory}{existingTitle}.md',f'{directory}{mapDict[existingTitle]}.md')

# %%
# make a copy of the original text file into a new directory
for title in grouped_quotes.keys():
    print(title)
    currentTitle = grouped_quotes[title]
    # check if the title already exists, if it does then don't add this
    # see all the files in the directory
    if title.strip() in existingTitles:
        currentMarkdown = ''
        writeMode = 'a'
        
    else:
        writeMode = 'w'
        currentMarkdown = currentTitle[0].markdownTitle()
    for quote in currentTitle:
        currentMarkdown+= quote.markdownBody()
    # for a given 
    file_path = directory+f"{title}.md"
    print(currentMarkdown)
    

    with open(file_path, writeMode) as file:
        file.write(currentMarkdown)
        file.close()

shutil.copy(textDirectory, previousDirectory)


