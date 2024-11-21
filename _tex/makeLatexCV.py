import yaml
import os
import bibtexparser
import subprocess
import shutil

from Templates.ModernCVTemplate import ModernCVTemplate


class Bibliography:

    def __init__(self, bibfile):

        self.library = bibtexparser.parse_file(bibfile)

    def getBibItems(self, andKwrds=[], orKwrds=[], orderByYear=False, orderByAuthor=False):

        bib = []

        for entry in self.library.entries:
            item = dict()

            haveAndKwrds = (
                not andKwrds or
                ('keywords' in entry.fields_dict and
                all(s in entry.fields_dict['keywords'].value for s in andKwrds))
            )

            haveOrKwrds = (
                not orKwrds or
                ('keywords' in entry.fields_dict and
                any(s in entry.fields_dict['keywords'].value for s in orKwrds))
            )
            
            if haveAndKwrds and haveOrKwrds:
                for field in entry.fields_dict:
                    item[field] = entry.fields_dict[field].value
                
                item['_type'] = entry.entry_type
                
                bib.append(item)

        sortFunc = None
        reverse = None
        # Order by year in reverse order
        if orderByYear:
            sortFunc = lambda item : item['year']
            reverse = True
        
        # Order by authors
        if orderByAuthor:
            sortFunc = lambda item : [auth.split(",")[0].strip() for auth in item['author'].split("and")]
            reverse = False
        
        # Sort
        if sortFunc:
            bib = sorted(bib, key=sortFunc, reverse=reverse)                           
        
        return bib


def writeToFile(filename, data, template):
        with open(filename, 'w') as file:
            file.write(template.getPreamble())
            file.write(template.getPersonalData(data['personal information']))
            file.write(template.getBeginDocument())
            file.write(template.getProfessionalExperience(data['professional experience']))
            file.write(template.getEducation(data['education']))
            file.write(template.getSoftware(data['software']))
            file.write(template.getPublications(data['refPubs'], secTitle='refereed publications'))
            file.write(template.getPublications(data['wipPubs'], secTitle='technical reports and publications in review'))
            file.write(template.getPublications(data['talks'], secTitle='conference presentations and talks'))
            file.write(template.getEndDocument())

def buildPDF(sourceTex, targetFile="cv.pdf", targetDir="."):
    # Ensure source file exists
    if not os.path.isfile(sourceTex):
        raise FileNotFoundError(f"Source file not found: {sourceTex}")

    # Ensure target directory exists
    if not os.path.exists(targetDir):
        raise FileNotFoundError(f"Target directory not found: {targetDir}")

    # Determine base name and build directory
    sourceDir = os.path.dirname(os.path.abspath(sourceTex))
    sourceBase = os.path.basename(sourceTex)
    sourceName, _ = os.path.splitext(sourceBase)
    buildDir = os.path.join(sourceDir, "build")

    try:
        # Compile with latexmk
        print(f"Compiling {sourceTex}...")
        subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", f"-output-directory={buildDir}", sourceTex],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Move the PDF to the target location
        sourcePDF = os.path.join(buildDir, f"{sourceName}.pdf")
        targetPath = os.path.join(targetDir, targetFile)

        if os.path.exists(sourcePDF):
            shutil.move(sourcePDF, targetPath)
            print(f"PDF successfully created at: {targetPath}")
        else:
            print("Error: PDF not found after compilation.")
            return None

        return targetPath

    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
        return None

    finally:
        # Delete the build directory
        if os.path.exists(buildDir):
            shutil.rmtree(buildDir)
            print(f"Deleted build directory: {buildDir}")

if __name__ == "__main__":
            
    # CV in YAML
    yamlCvPath = os.path.join(".", "_data", "cv.yml")

    # BibTeX
    paperBibPath = os.path.join(".", "_bibliography", "papers.bib")
    talksBibPath = os.path.join(".", "_bibliography", "talks.bib")

    outSourceCvTex = "Battista_F_CV.tex"
    targetCvPdf = os.path.join(".", "assets", "pdf")

    template = ModernCVTemplate()

    # Read YAML file
    with open(yamlCvPath, 'r') as file:
        data = yaml.safe_load(file)
    
    data['personal information']['firstName'] = "Federico"
    data['personal information']['lastName']  = "Battista"
    data['personal information']['title']     = "Curriculum Vit\\ae{}"

    papers = Bibliography(paperBibPath)
    talks  = Bibliography(talksBibPath)
    
    orKwrds = ['preprint', 'wip']

    data['refPubs'] = papers.getBibItems(orderByYear=True)
    data['wipPubs'] = papers.getBibItems(orderByYear=True, orKwrds=orKwrds)

    data['talks']   = talks.getBibItems(orderByYear=True)
    
    writeToFile(outSourceCvTex, data, template)
    buildPDF(outSourceCvTex, targetFile="Battista_F_CV.pdf", targetDir=targetCvPdf)


