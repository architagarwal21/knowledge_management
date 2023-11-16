import re
import nltk
from nltk.tokenize import sent_tokenize
import pandas as pd



def extract_concatenated_notes(notes_str):
    # Splitting at each point before a capital letter, but not at the start of the string
    notes = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', notes_str)
    return notes

def extract_top_notes(perfume_description):
    # Define the regex pattern to match the top notes section
    pattern = r"Top Notes(.*?)(Middle Notes|Base Notes|Pros|Vote for Ingredients|$)"
    
    # Find the top notes section
    match = re.search(pattern, perfume_description, re.DOTALL | re.IGNORECASE)
    if match:
        # Extracting the matched group for top notes
        top_notes_section = match.group(1).strip()

        # Check if notes are concatenated (no spaces or commas)
        if ',' not in top_notes_section and ' ' not in top_notes_section:
            return extract_concatenated_notes(top_notes_section)
        else:
            # Splitting notes by commas or spaces
            notes_list = re.split(r',\s*|\s(?=\w)', top_notes_section)
            return [note.strip() for note in notes_list if note.strip()]
    else:
        return []
  
nltk.download('punkt')
def preprocess_reviews(reviews):
    sentences = sent_tokenize(reviews)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

    
def insert_into_edgedb(df, client):
    for index, row in df.iterrows():
        # Insert Brand
        brand_name = row['Brand']
        existing_brands = client.query("""
            SELECT Brand {
                id
            } FILTER .name = <str>$brand_name
        """, brand_name=brand_name)

        if not existing_brands:
            # Insert the brand if it doesn't exist
            client.query("""
                INSERT Brand {
                    name := <str>$brand_name
                }
            """, brand_name=brand_name)
       
        # Insert Scent Groups
        scent_groups = row['Scent group'].strip('][').split(', ')
        for scent in scent_groups:
            # Check if the scent group already exists
            existing_scent_groups = client.query("""
                SELECT ScentGroup {
                    id
                } FILTER .name = <str>$scent
            """, scent=scent)

            if not existing_scent_groups:
                # Insert the scent group if it doesn't exist
                client.query("""
                    INSERT ScentGroup {
                        name := <str>$scent
                    }
                """, scent=scent)

        # Extract and Insert Top Notes
        top_notes = extract_top_notes(row['Top Notes'])
        notes_ids = []

        for note in top_notes:
            existing_notes = client.query("""
                SELECT Notes {
                id
                } FILTER .name = <str>$note
            """, note=note)

            if existing_notes:
                note_id = existing_notes[0].id
            else:
            # Insert new note and get the Object
                new_note = client.query_single("""
                    INSERT Notes {
                        name := <str>$note
                    }
                """, note=note)
                note_id = new_note.id  # Extract the ID from the Object
            notes_ids.append(note_id)

        # Insert Perfume
        perfume_name = row['Perfume Name']
        perfume_rating = row['Perfume Rating']
        perfume_best_rating = row['Perfume Best Rating']
        perfume_rating_count = row['Perfume Rating Count']
        perfume_description = row['Perfume Description']

        existing_perfume = client.query("""
            SELECT Perfume {
                id
            } FILTER .name = <str>$perfume_name AND .owned_by.name = <str>$brand_name
        """, perfume_name=perfume_name, brand_name=brand_name)

        if not existing_perfume:
            # Insert the perfume if it doesn't exist
            new_perfume = client.query_single("""
                INSERT Perfume {
                    name := <str>$perfume_name,
                    rating := <float64>$perfume_rating,
                    best_rating := <int64>$perfume_best_rating,
                    rating_count := <int64>$perfume_rating_count,
                    description := <str>$perfume_description,
                    owned_by := (SELECT Brand FILTER .name = <str>$brand_name),
                    belongs_to := (
                        SELECT ScentGroup FILTER .name IN array_unpack(<array<str>>$scent_groups)
                    ),
                    contains := (
                        SELECT Notes FILTER .id IN array_unpack(<array<uuid>>$notes_ids)
                    )
                }
            """, perfume_name=perfume_name, perfume_rating=perfume_rating, perfume_best_rating=perfume_best_rating, 
                perfume_rating_count=perfume_rating_count, perfume_description=perfume_description, brand_name=brand_name, 
                scent_groups=scent_groups, notes_ids=notes_ids)

            perfume_id = new_perfume.id  # Extracting the ID from the new perfume object
        else:
            perfume_id = existing_perfume[0].id

        # Insert Reviews
        reviews = row['User Reviews']
        if pd.notna(reviews):
            preprocessed_reviews = preprocess_reviews(reviews)
            for review in preprocessed_reviews:
                client.query("""
                    INSERT Review {
                        content := <str>$review,
                        user_of := (SELECT Perfume FILTER .id = <uuid>$perfume_id)
                    }
                """, review=review, perfume_id=perfume_id)