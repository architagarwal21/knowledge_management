
def search_items(query, client):
    # This is a complex query that attempts to match the search query to various fields
    # across the Perfume type and its related types (Brand, ScentGroup, Notes, Review).
    result = client.query('''
        SELECT Perfume {
            name,
            rating,
            best_rating,
            rating_count,
            description,
            owned_by: {
                name
            },
            belongs_to: {
                name
            },
            contains: {
                name
            },
            has_review: {
                content
            }
        } FILTER 
            .name ILIKE <str>$query OR
            .description ILIKE <str>$query OR
            .owned_by.name ILIKE <str>$query OR
            EXISTS(.belongs_to FILTER .name ILIKE <str>$query) OR
            EXISTS(.contains FILTER .name ILIKE <str>$query) OR
            EXISTS(.has_review FILTER .content ILIKE <str>$query);
    ''', query=f'%{query}%')
    return result
