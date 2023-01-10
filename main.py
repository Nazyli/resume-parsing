import os
from pdfminer.high_level import extract_text
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
import re

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
                person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))

    return person_names

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        return number
        # if resume_text.find(number) >= 0 and len(number) < 16:
        #     return number
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
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
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



onlyfiles = [os.path.join(PATH_DIR, f) for f in os.listdir(PATH_DIR) if os.path.isfile(os.path.join(PATH_DIR, f))]
for x in onlyfiles:
    dataCV = extract_text_from_pdf(x)
    names = extract_names(dataCV)
    phone = extract_phone_number(dataCV)
    emails = extract_emails(dataCV)
    skills = extract_skills(dataCV)
    education = extract_education(dataCV)
    print(names)
    print(phone)
    print(emails)
    print(skills)
    print(education)
