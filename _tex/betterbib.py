import bibtexparser
from rapidfuzz import fuzz
import re
import unicodedata

bib_old_source = 'refs.bib'
bib_new_source = 'BilevelOptimization.bib'

citeCommands = ["\\cite", "\\citt", "\\citp", "\\citep", "\\citet"]

skipWordsTex = ["\\newcommand"]

regexLatexAccents = r"\\['^`\"~cuvH=rkb.\d\t]?(?:\{(.)\}|([a-zA-Z]))"

regexLatexMath = r'\$.*?\$'


def getCleanBibTitle(title):
    # Remove math mode content within $...$
    # title = re.sub(regexLatexMath, '', title)
    title = title.replace("$", "")

    # Remove LaTeX accent commands and keep only the base letter
    title = re.sub(regexLatexAccents, r"\1\2", title)
    
    # Normalize the string to decompose combined characters
    title = unicodedata.normalize('NFKD', title)
    
    # Remove any diacritical marks (accents) that remain after normalization
    title = ''.join(c for c in title if unicodedata.category(c) != 'Mn')
    
    # Remove braces
    title = title.replace('{', '').replace('}', '')

    # Remove tabs, new lines, etc.
    title = re.sub(r'\s+', ' ', title).strip()
    
    title = " ".join(title.lower().split())

    # Return the list of words split by spaces
    return title


def getAuthorsNames(author, authSep='and', fullNameSep=','):
    # Remove math mode content within $...$
    author = re.sub(regexLatexMath, '', author)

    # Remove LaTeX accent commands and keep only the base letter
    author = re.sub(regexLatexAccents, r"\1\2", author)
    
    # Normalize the string to decompose combined characters
    author = unicodedata.normalize('NFKD', author)
    
    # Remove any diacritical marks (accents) that remain after normalization
    author = ''.join(c for c in author if unicodedata.category(c) != 'Mn')
    
    # Remove braces
    author = author.replace('{', '').replace('}', '')
    
    # Remove author separator
    author = author.replace(authSep, ' ')

    # Remove full name separator
    author = author.replace(fullNameSep, ' ')

    # Remove tabs, new lines, etc.
    author = re.sub(r'\s+', ' ', author).strip()

    author = " ".join(author.lower().split())

    # Return the list of words split by spaces
    return author


def getMappingCitationKeys(library_old, library_new):
    citeKeyMapping = {}
    citeKeyNotFound = []

    ordTitlesOld, ordAuthorsOld = processLibrary(library_old)
    ordTitlesNew, ordAuthorsNew = processLibrary(library_new)

    # For each item in library_old try to find the
    # corresponding key in library_new
    for idx, entry in enumerate(library_old.entries):
        titleOld = ordTitlesOld[idx]
        authorsOld = ordAuthorsOld[idx]

        if titleOld in ordTitlesNew:
            # title matches
            idxMatch = ordTitlesNew.index(titleOld)
            citeKeyMapping[entry.key] = library_new.entries[idxMatch].key

            # if authorsOld == ordAuthorsNew[idxMatch]:
            #     # authors matches
            #     citeKeyMapping[entry.key] = library_new.entries[idxMatch].key
            # else:
            #     print("WARNING: Title matches but Authors don't!!")
            #     print("   old Title  : ", titleOld)
            #     print("   old Authors: ", authorsOld)
            #     print("   new Title  : ", ordTitlesNew[idxMatch])
            #     print("   new Authors: ", ordAuthorsNew[idxMatch])
        else:
            print("WARNING: Match for Bibitem {} not found".format(entry.key))
            citeKeyNotFound.append((idx, entry.key))
    
    return citeKeyMapping, citeKeyNotFound

def getMappingCitationKeysNew(library_old, library_new):
    citeKeyMapping = {}
    citeKeyNotFound = []

    # For each item in library_old try to find the
    # corresponding key in library_new
    for idxOld, entryOld in enumerate(library_old.entries):
        titleOld = getCleanBibTitle(entryOld.fields_dict['title'].value)
        authOld = getAuthorsNames(entryOld.fields_dict['author'].value)
        
        for idxNew, entryNew in enumerate(library_new.entries):
            titleNew = getCleanBibTitle(entryNew.fields_dict['title'].value)
            authNew = getAuthorsNames(entryNew.fields_dict['author'].value)
            titlesRatio = fuzz.ratio(titleOld, titleNew)
            authRatio = fuzz.ratio(authOld, authNew)

            if titlesRatio > 95 and authRatio > 90:
                print("Old Title: ", titleOld)
                print("New Title: ", titleNew)
                print("Similarity Titles: ", titlesRatio)
                print("Old Auth: ", authOld)
                print("New Auth: ", authNew)
                print("Similarity Auth: ", authRatio)
                print("")

                citeKeyMapping[entryOld.key] = entryNew.key
                break
    
    print(citeKeyMapping)

    #     if titleOld in ordTitlesNew:
    #         # title matches
    #         idxMatch = ordTitlesNew.index(titleOld)
    #         citeKeyMapping[entry.key] = library_new.entries[idxMatch].key

    #         # if authorsOld == ordAuthorsNew[idxMatch]:
    #         #     # authors matches
    #         #     citeKeyMapping[entry.key] = library_new.entries[idxMatch].key
    #         # else:
    #         #     print("WARNING: Title matches but Authors don't!!")
    #         #     print("   old Title  : ", titleOld)
    #         #     print("   old Authors: ", authorsOld)
    #         #     print("   new Title  : ", ordTitlesNew[idxMatch])
    #         #     print("   new Authors: ", ordAuthorsNew[idxMatch])
    #     else:
    #         print("WARNING: Match for Bibitem {} not found".format(entry.key))
    #         citeKeyNotFound.append((idx, entry.key))
    
    # return citeKeyMapping, citeKeyNotFound

def processLibrary(library):
    ordTitles = []
    ordAuthors = []

    for entry in library.entries:
        # Process title
        ordTitles.append(getCleanBibTitle(entry.fields_dict['title'].value))
        # Process authors
        ordAuthors.append(getAuthorsNames(entry.fields_dict['author'].value))

    return ordTitles, ordAuthors


def getCitations(tex_filename, cite_commands=["\\cite"]):
    citation_data = []
    
    # Sort cite commands by length in descending order for longest match first
    sorted_cite_commands = sorted(cite_commands, key=len, reverse=True)

    # Create a regex pattern that matches any of the cite commands
    cite_pattern = '|'.join(re.escape(cmd) for cmd in sorted_cite_commands)
    pattern = re.compile(rf"({cite_pattern})\{{([^}}]+)\}}")
    
    # Open and read the file line by line
    with open(tex_filename, 'r') as tex_file:
        for line_num, line in enumerate(tex_file, start=1):
            # Check for skip words (e.g., for preamble commands)
            if any(s in line for s in skipWordsTex):
                continue
            # Search for cite commands in the line
            matches = pattern.findall(line)
            if matches:
                for cite_cmd, keys in matches:
                    # Split citation keys by commas and strip whitespace
                    citation_keys = [key.strip() for key in keys.split(',')]
                    # Append line number, command, and found keys to citation data
                    citation_data.append({
                        'line_number': line_num,
                        'cite_command': cite_cmd,
                        'citations': citation_keys
                    })
    
    return citation_data


def replaceCitations(texFilename, allCitations, citeKeyMapping):
    totCitations = 0
    countCitationsReplaced = 0
    lines = []
    with open(texFilename, 'r') as texFile:
        lines = texFile.readlines()
        for cit in allCitations:
            line = lines[cit['line_number'] - 1]
            for ref in cit['citations']:
                if ref in citeKeyMapping:
                    line = line.replace(ref, citeKeyMapping[ref])
                    countCitationsReplaced += 1
                else:
                    print("WARNING: Citation not found")
                totCitations += 1

            lines[cit['line_number'] - 1] = line

    print("Total citations: ", totCitations)
    print("Citations replaced: ", countCitationsReplaced)
    
    with open(texFilename, 'w') as texFile:
        texFile.writelines(lines)
    


allCitations = getCitations('main.tex', cite_commands=citeCommands)

for cite in allCitations: 
    print(cite)

# Read the BibTeX file
library_old = bibtexparser.parse_file(bib_old_source)
library_new = bibtexparser.parse_file(bib_new_source)

# Access entries
print(f"Parsed {len(library_old.blocks)} blocks, including:"
  f"\n\t{len(library_old.entries)} entries"
    f"\n\t{len(library_old.comments)} comments"
    f"\n\t{len(library_old.strings)} strings and"
    f"\n\t{len(library_old.preambles)} preambles")

if len(library_old.failed_blocks) > 0:
    print("Some blocks failed to parse. Check the entries of `library.failed_blocks`.")
else:
    print("All blocks parsed successfully")

print(f"Parsed {len(library_new.blocks)} blocks, including:"
  f"\n\t{len(library_new.entries)} entries"
    f"\n\t{len(library_new.comments)} comments"
    f"\n\t{len(library_new.strings)} strings and"
    f"\n\t{len(library_new.preambles)} preambles")

if len(library_new.failed_blocks) > 0:
    print("Some blocks failed to parse. Check the entries of `library.failed_blocks`.")
else:
    print("All blocks parsed successfully")

# for entry in library_old.entries:
#     print(getCleanBibTitle(entry.fields_dict['title'].value))
#     print(getAuthorsNames(entry.fields_dict['author'].value))
#     print("")

# print('='*10)

# for entry in library_new.entries:
#     print(getCleanBibTitle(entry.fields_dict['title'].value))
#     print(getAuthorsNames(entry.fields_dict['author'].value))
#     print("")


getMappingCitationKeysNew(library_old, library_new)

# citeKeyMapping, citeKeyNotFound = getMappingCitationKeys(library_old, library_new)
# replaceCitations('main.tex', allCitations, citeKeyMapping)