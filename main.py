import os
from pdfminer.high_level import extract_text
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(' '.join(chunk_leave[0] for chunk_leave in chunk.leaves()))

    return person_names


pathDir = 'input'
onlyfiles = [os.path.join(pathDir, f) for f in os.listdir(
    pathDir) if os.path.isfile(os.path.join(pathDir, f))]
for x in onlyfiles:
    dataCV = extract_text_from_pdf(x)
    names = extract_names(dataCV)
    print(names)
