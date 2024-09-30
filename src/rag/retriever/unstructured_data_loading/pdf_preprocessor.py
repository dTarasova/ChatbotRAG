
import pymupdf
import re
#
def process_pdf(input_pdf_path: str, output_pdf_path: str = "") -> str:
    if not output_pdf_path or output_pdf_path == "":
        filename = input_pdf_path.split("/")[-1]
        output_pdf_path = "data/processed_texts/input" + (filename.replace(".pdf", ".txt"))
    text = extract_paragraphs_from_pdf(input_pdf_path)
    wo_ref_paragraphs = remove_ref_paragraphs(text)
    cleaned_paragraphs = filter_text(wo_ref_paragraphs)
    final_text = save_paragraphs_to_txt(cleaned_paragraphs, output_pdf_path)
    return final_text

def extract_paragraphs_from_pdf(pdf_path: str) -> list[str]:
    document = pymupdf.open(pdf_path)
    paragraphs = []
    doc_len = len(document)
    for page_num in range(doc_len):
        page = document.load_page(page_num)
        blocks = page.get_text("blocks")
        text_elements = [block[4].lower() for block in blocks]
        paragraphs.extend(text_elements)
    return paragraphs


def remove_ref_paragraphs(paragraphs: list[str]) -> list[str]:
    for i, paragraph in enumerate(reversed(paragraphs)):
            paragraph_text = paragraph.strip().lower()
            if paragraph_text == "references" or paragraph_text == "bibliography":
                cut_index = len(paragraphs) - i - 1
                return paragraphs[:cut_index]
    return paragraphs



def save_text_to_txt(text: str, file_path: str):
    try: 
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"An error occurred: {e}")

def save_paragraphs_to_txt(paragraphs, file_path) -> str:
    paragraphs_text = ''
    for paragraph in paragraphs:
        # paragraphs_text += paragraph + '\n\n'
        paragraphs_text += paragraph
    save_text_to_txt(paragraphs_text, file_path)
    return paragraphs_text




def filter_text(paragraphs: list[str]) -> list[str]:
    # Define the pattern to match unwanted lines
    content_pattern = re.compile(r'(.*\..*){4,}')
    numeric_only_pattern = re.compile(r'^\s*[\d\.\s]+$')  # Matches paragraphs made up only of numbers, spaces, and periods
    image_titles_pattern = re.compile(r'fig\.\s?\d+', re.IGNORECASE)  # Matches image titles like "fig. 4"

    filtered_paragraphs = []

    # Split the text into lines
    for p in paragraphs:
        lines = p.split('\n')

        # Filter out lines that match the pattern
        filtered_lines = [
            line for line in lines 
            if not (numeric_only_pattern.match(line) or 
                    image_titles_pattern.search(line)
                    or content_pattern.match(line))
        ]

        if filtered_lines:
            filtered_text = '\n'.join(filtered_lines)
            filtered_paragraphs.extend([filtered_text])


    return filtered_paragraphs



# rag_model = RAGModel(type='step-back')
# answer, retrieved_docs = rag_model.query("Is requirement 'System should be fast' a good requirement?")
# print("\n\nAnswer:\n\n", answer)
# print("\n\nRetrieved Documents:\n\n", retrieved_docs)

# FILE1 = 'data/first_batch/Rapid quality assurance with Requirements Smells.pdf'
# # FILE2 = 'data/Naming the Pain in Requirements Engineering Contemporary Problems, Causes, and Effects in Practice.pdf'


# pdf = pdfplumber.open(FILE1)
# page = pdf.pages[6]
# table = page.extract_table()
# text = page.extract_text()
# lines = page.extract_text_lines()
# for line in lines: 
#     print(line)


# page = pdf.pages[5]
# table = page.extract_table()
# text = page.extract_text()
# lines = page.extract_text_lines()
# for line in lines: 
#     print(line)

# document = pymupdf.open(FILE1)
# paragraphs = []
# doc_len = len(document)
# page = document.load_page(6)

# blocks = page.get_text("blocks")
# for block in blocks: print(block, '\n\n' )

# textpage = page.get_textpage
# print("textpage: ", textpage)

# text = page.get_textbox()
# print("text: ", text)