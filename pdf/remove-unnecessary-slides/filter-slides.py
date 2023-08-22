import re
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def filter_slide_deck(input_path, output_path):
    """ 
    Filters a slide deck to remove consecutive slides that build upon each other, 
    keeping only the last slide in the series.
    
    Args:
    - input_path (str): Path to the input slide deck (PDF file).
    - output_path (str): Path to save the filtered slide deck.
    """
    try:
        # Extract content from each slide
        pdf = PdfFileReader(input_path)
        
        # Check if the PDF has any pages
        if not pdf.pages:
            print("The provided PDF does not contain any slides.")
            return
        
        slide_contents = [page.extract_text() or "NO_TEXT_CONTENT_PLACEHOLDER" for page in pdf.pages]
        cleaned_slide_contents = [re.sub('\s+', ' ', content).strip() for content in slide_contents]

        # Convert slide contents into TF-IDF vectors and compute similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(cleaned_slide_contents)
        similarities = [cosine_similarity(tfidf_matrix[i], tfidf_matrix[i + 1])[0][0] for i in range(len(cleaned_slide_contents) - 1)]

        # Determine slides to keep
        similarity_threshold = 0.9
        slides_to_keep = [i for i, similarity in enumerate(similarities) if similarity < similarity_threshold]
        slides_to_keep.append(len(cleaned_slide_contents) - 1)

        # Create a new PDF with the selected slides
        output_pdf = PdfFileWriter()
        with open(input_path, "rb") as file:
            reader = PdfFileReader(file)
            for index in slides_to_keep:
                output_pdf.addPage(reader.getPage(index))
            with open(output_path, "wb") as output_file:
                output_pdf.write(output_file)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python filter_slides.py <input_path> <output_path>")
        sys.exit(1)
    
    input_pdf_path = sys.argv[1]
    output_pdf_path = sys.argv[2]
    filter_slide_deck(input_pdf_path, output_pdf_path)
    print(f"Filtered slide deck saved to: {output_pdf_path}")
