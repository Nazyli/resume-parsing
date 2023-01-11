import os
from pdfminer.high_level import extract_text
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
import re
import xlsxwriter


# constant
PATH_DIR = 'input'
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'english',
    'programming',
    'matlab'
]
RESERVED_WORDS = [
    'school',
    'college',
    'univers',
    'academy',
    'faculty',
    'institute',
    'faculdades',
    'Schola',
    'schule',
    'lise',
    'lyceum',
    'lycee',
    'polytechnic',
    'kolej',
    'ünivers',
    'okul',
]


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))

    return person_names


def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        return phone
        # number = ''.join(phone[0])
        # return number
        # # if resume_text.find(number) >= 0 and len(number) < 16:
        # #     return number
    return None


def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)


def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(
        map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
    # create a set to keep the results in.
    found_skills = set()
    # search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
    # search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)

    return found_skills


def extract_education(input_text):
    organizations = []
    # first get all the organization names using nltk
    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
    # we search for each bigram and trigram for reserved words
    # (college, university etc...)
    education = set()
    for org in organizations:
        for word in RESERVED_WORDS:
            if org.lower().find(word) >= 0:
                education.add(org)

    return education


def create_header_excel(workbook, worksheet):
    cell_format_header = workbook.add_format()
    cell_format_header.set_align('center')
    cell_format_header.set_align('vcenter')
    cell_format_header.set_bold()
    cell_format_header.set_border(2)
    header = ['No', 'Extract Names', 'Extract Phone Number',
              'Extract Emails', 'Extract Skills', 'Extract Education']
    for x in range(len(header)):
        worksheet.write(0, x, header[x], cell_format_header)

    worksheet.set_row(0, 20)
    worksheet.set_column(1, 2, 40)
    worksheet.set_column(2, 2, 20)
    worksheet.set_column(3, 5, 30)

def create_body_excel(workbook, worksheet, row, dataCV):
    names = extract_names(dataCV)
    phone = extract_phone_number(dataCV)
    emails = extract_emails(dataCV)
    skills = extract_skills(dataCV)
    education = extract_education(dataCV)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('left')
    cell_format.set_align('vcenter')
    worksheet.write(row, 0, row, cell_format)
    worksheet.write(row, 1, ', '.join(names), cell_format)
    worksheet.write(row, 2, ', '.join(phone), cell_format)
    worksheet.write(row, 3, ', '.join(emails), cell_format)
    worksheet.write(row, 4, ', '.join(skills), cell_format)
    worksheet.write(row, 5, ', '.join(education), cell_format)



onlyfiles = [os.path.join(PATH_DIR, f) for f in os.listdir(PATH_DIR) if os.path.isfile(os.path.join(PATH_DIR, f))]
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()
create_header_excel(workbook, worksheet)
row = 1
for x in onlyfiles:
    dataCV = extract_text_from_pdf(x)
    create_body_excel(workbook, worksheet, row, dataCV)
    row += 1

workbook.close()
