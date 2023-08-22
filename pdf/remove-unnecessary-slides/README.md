
# Slide Deck Filter Script

## Description
This script filters a slide deck (in PDF format) to remove consecutive slides that build upon each other, keeping only the last slide in a series. It's particularly useful for presentations where information is progressively revealed across multiple slides, and you only want to retain the final, comprehensive slide.

## Requirements
- Python 3.x
- Libraries: 
  - `PyPDF2`
  - `scikit-learn`

You can install the required libraries using pip:
```
pip install PyPDF2 scikit-learn
```

## Usage
To use the script, navigate to the directory containing the script and run:
```
python filter_slides.py <input_slide_deck_path> <output_path>
```
Replace `<input_slide_deck_path>` with the path to your slide deck and `<output_path>` with the desired path for the filtered slide deck.

## How It Works
The script first extracts textual content from each slide. It then uses the Term Frequency-Inverse Document Frequency (TF-IDF) method to convert the slide contents into vectors. The cosine similarity between these vectors is computed for consecutive slides to determine their similarity. Slides with a similarity score above a certain threshold (e.g., 0.9) are considered similar. The script retains only the last slide in a series of similar consecutive slides.

## License
This script is released under the MIT License. Feel free to use, modify, and distribute as you see fit, but please provide attribution.
