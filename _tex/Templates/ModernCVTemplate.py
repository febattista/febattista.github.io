import textwrap
from datetime import datetime

class ModernCVTemplate:
    def __init__(self, geometryScale=0.85, themeStyle='classic', themeColor='burgundy'):
        self.geometryScale = geometryScale
        self.themeStyle    = themeStyle
        self.themeColor    = themeColor

    def getPreamble(self):
        preamble = r"""
        \documentclass[11pt,a4paper,sans]{moderncv}

        % moderncv themes
        \moderncvstyle{""" + f"{self.themeStyle}" + r"""}
        \moderncvcolor{""" + f"{self.themeColor}" + r"""}
        %\renewcommand{\familydefault}{\sfdefault}
        %\nopagenumbers{}

        % adjust the page margins
        \usepackage[scale=""" + f"{self.geometryScale}" + r"""]{geometry}
        \setlength{\footskip}{136.00005pt}
        %\setlength{\hintscolumnwidth}{3cm}
        %\setlength{\makecvheadnamewidth}{10cm}

        % font loading
        % for luatex and xetex, do not use inputenc and fontenc
        % see https://tex.stackexchange.com/a/496643
        \ifxetexorluatex
        \usepackage{fontspec}
        \usepackage{unicode-math}
        \defaultfontfeatures{Ligatures=TeX}
        \setmainfont{Latin Modern Roman}
        \setsansfont{Latin Modern Sans}
        \setmonofont{Latin Modern Mono}
        \setmathfont{Latin Modern Math} 
        \else
        \usepackage[T1]{fontenc}
        \usepackage{lmodern}
        \fi

        % document language
        \usepackage[english]{babel}

        % bibliography adjustments (only useful if you make citations in your resume, or print a list of publications using BibTeX)
        %   to show numerical labels in the bibliography (default is to show no labels)
        %\makeatletter\renewcommand*{\bibliographyitemlabel}{\@biblabel{\arabic{enumiv}}}\makeatother
        \renewcommand*{\bibliographyitemlabel}{[\arabic{enumiv}]}
        %   to redefine the bibliography heading string ("Publications")
        %\renewcommand{\refname}{Articles}

        % bibliography with mutiple entries
        %\usepackage{multibib}
        %\newcites{book,misc}{{Books},{Others}}
        """
        return textwrap.dedent(preamble)
    

    def getBeginDocument(self):

        beginDoc  = "" 
        beginDoc += "%----------------------------------------------------------------------------------\n"
        beginDoc += "%            content\n"
        beginDoc += "%----------------------------------------------------------------------------------\n"
        beginDoc += "\\begin{document}\n"
        beginDoc += "\\makecvtitle\n"
        beginDoc += "\n"
        
        return beginDoc
    

    def getEndDocument(self):

        endDoc  = "\end{document}" 
        
        return endDoc


    def getPersonalData(self, personalData = dict()):

        personalDataStr = "% personal data\n"

        if 'firstName' in personalData and 'lastName' in personalData:
            personalDataStr += "\\name{" + f"{personalData['firstName']}" + "}{" + f"{personalData['lastName']}" + "}\n"
        
        if 'title' in personalData:
            personalDataStr += "\\title{" + f"{personalData['title']}" + "}\n"

        if 'dateOfBirth' in personalData:
            # Convert string to datetime object
            date_obj = datetime.strptime(personalData['dateOfBirth'], '%Y-%m-%d')

            # Convert datetime object to the desired format
            formatted_date = date_obj.strftime('%d %B %Y')
            personalDataStr += "\\born{" + f"{formatted_date}" + "}\n"

        if 'address' in personalData:
            address = personalData['address'].split(",") 
            street_and_number = ','.join(address[0: 2])
            zipcode_city = ','.join(address[2: 4])
            country = address[4]
            personalDataStr += "\\address{" + f"{street_and_number}" + "}{" + f"{zipcode_city}" + "}{" + f"{country}" + "}\n"

        if 'mobile' in personalData:
            pass

        if 'email' in personalData:
            personalDataStr += "\\email{" + f"{personalData['email']}" + "}\n"

        if 'url' in personalData:
            url = personalData['url'].replace('https://', '')
            personalDataStr += "\\homepage{" + f"{url}" + "}\n"

        return personalDataStr
    
    def getProfessionalExperience(self, profExp = []):

        profExpStr  = "% professional experience\n"
        profExpStr += "\section{Professional experience}\n"

        # Sort Experiences by date
        sorted_experiences = sorted(profExp, 
                           key=lambda x: datetime.strptime(x['startDate'], '%Y-%m-%d'), 
                           reverse=True)
        
        for exp in sorted_experiences:
            
            position  = exp['position']
            location  = exp['location']
            name      = exp['name']

            if 'advisor' in exp:
                if len(exp['advisor'].split(',')) > 1:
                    advisor   = ("Advisors: " + exp['advisor'])
                else:
                    advisor   = ("Advisor: " + exp['advisor'])
            else:
                advisor = ''
            
            summary   = exp['summary'] if 'summary' in exp else ''
            startDate = datetime.strptime(exp['startDate'], '%Y-%m-%d').strftime('%Y.%m')
            endDate   = datetime.strptime(exp['endDate'], '%Y-%m-%d').strftime('%Y.%m') if 'present' not in exp['endDate'].lower() else exp['endDate']
            
            profExpStr += "\cventry{from " + f"{startDate}" + " to " + f"{endDate}" + "}"
            profExpStr += "{" + f"{position}" + "}"
            profExpStr += "{\\textcolor{violet}{" + f"{name.split(',')[1]}" + "}, "  + f"{name.split(',')[0]}" + "}"
            profExpStr += "{" + f"{location}" + "}" 
            profExpStr += "{\\newline{}" + f"{advisor}" + "}" 
            profExpStr += "{" + f"{summary}" + "}\n" 

        return profExpStr
    
    def getEducation(self, educations=[]):

        eduStr  = "% education\n"
        eduStr += "\section{Education}\n"

        # Sort Experiences by date
        sorted_educations = sorted(educations, 
                           key=lambda x: datetime.strptime(x['startDate'], '%Y-%m-%d'), 
                           reverse=True)
        
        for edu in sorted_educations:
            
            if 'advisor' in edu:
                if len(edu['advisor'].split(',')) > 1:
                    advisor   = ("Supervisors: " + edu['advisor'])
                else:
                    advisor   = ("Supervisor: " + edu['advisor'])
            else:
                advisor = ''

            institution  = edu['institution']
            location     = edu['location']
            studyType    = edu['studyType']
            thesis       = edu['thesis'].replace("(", "").replace(")", "")
            grade        = edu['grade'] if 'grade' in edu else ''
            startDate    = datetime.strptime(edu['startDate'], '%Y-%m-%d').strftime('%Y.%m')
            endDate      = datetime.strptime(edu['endDate'], '%Y-%m-%d').strftime('%Y.%m') if 'present' not in edu['endDate'].lower() else exp['endDate']
            
            eduStr += "\cventry{from " + f"{startDate}" + " to " + f"{endDate}" + "}"
            eduStr += "{" + f"{studyType}" + "}"
            eduStr += "{\\textcolor{violet}{" + f"{institution}" + "}}"
            eduStr += "{" + f"{location}" + "}" 
            eduStr += "{\\textbf{Thesis: }" + f"{thesis}" + "}"
            eduStr += "{" + f"{advisor}" + (("\\newline{}Final mark: " + f"{grade}" + "}\n") if grade else "}\n")

        return eduStr
    
    def getSoftware(self, softwares=[]):

        softStr = "% software\n"
        softStr += "\\section{Software}\n"

        for soft in softwares:

            name       = soft['name'].replace("_", "\\_")
            url        = soft['url'].replace("_", "\\_")
            role       = soft['role']
            highlights = ','.join(soft['highlights'])
            summary    = soft['summary'].strip()

            softStr += "\cventry{" + f"{role}" + "}"
            softStr += "{" + f"{name}" + "}"
            softStr += "{\\footnotesize \\texttt{" + f"{highlights}" + "}}"
            softStr += "{}"
            softStr += "{}"
            softStr += "{\\url{" + f"{url}" + "}\\newline{}" + f"{summary}" + "}\n"
        
        return softStr
    
    def getPublications(self, bib, secTitle="publications"):
        bibStr  = "% " + f"{secTitle}" +"\n"
        secTitle = secTitle.capitalize()
        bibStr += "\\section{" + f"{secTitle}" +"}\n"

        lastYear = None
        for item in bib:
            year = item['year'] if not lastYear or lastYear != item['year']  else ""
            lastYear = item['year']
            title = item['title']

            if item['_type'] == "article":
                journal = item['journal']
            elif item['_type'] == "phdthesis":
                journal = "Ph.D. Thesis, " + item['school']
            else:
                journal = ""

            if 'address' in item:
                journal += ", " + item['address']
            
            if 'doi' in item:
                url = item['doi'] if "https://" in item['doi'] or "http://" in item['doi'] else "https://doi.org/%s" % (item['doi'])
            else:
                url = ""

            authors = ""
            for auth in item['author'].split("and"):
                lastName, firstName = auth.split(",")[0:2]
                lastName = lastName.strip()
                firstName = firstName.strip()[0].upper() + "."
                authors += firstName + " " + lastName + ", "

            bibStr += "\\cvitem{" + f"{year}" + "}"
            bibStr += "{" + f"{authors}"
            bibStr += "\\textbf{" + f"{title}" +"}, "
            if journal:
                bibStr += "\\textit{" + f"{journal}" +"}, "

            if url:
                bibStr += "\\url{" + f"{url}" + "}"
           
            bibStr = bibStr.strip(" ,") + "}\n"

        return bibStr