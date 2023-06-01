masculine_to_feminine = {
    "he": "she",
    "him": "her",
    "his": "hers",
    "himself": "herself",
    "man": "woman",
    "men": "women",
    "boy": "girl",
    "boys": "girls",
    "father": "mother",
    "dad": "mom",
    "son": "daughter",
    "brother": "sister",
    "uncle": "aunt",
    "nephew": "niece",
    "husband": "wife",
    "groom": "bride",
    "king": "queen",
    "prince": "princess",
    "male": "female",
    "sir": "ma'am",
    "mr.": "ms.",
    "mister": "miss",
    "chairman": "chairwoman",
    "businessman": "businesswoman",
    "congressman": "congresswoman",
    "steward": "stewardess",
    "actor": "actress",
    "waiter": "waitress",
    "policeman": "policewoman",
    "fireman": "firewoman",
    "mailman": "mailwoman",
    "salesman": "saleswoman",
    "spokesman": "spokeswoman",
    "landlord": "landlady",
    "host": "hostess",
    "gentleman": "lady",
    "grandfather": "grandmother",
    "grandpa": "grandma",
    "papa": "mama",
    "daddy": "mommy",
    "son-in-law": "daughter-in-law",
    "brother-in-law": "sister-in-law",
    "father-in-law": "mother-in-law",
    "kingpin": "queenpin",
    "godfather": "godmother",
    "sugar daddy": "sugar mommy"
}

feminine_to_masculine = {'she': 'he',
                         'her': 'him',
                         'hers': 'his',
                         'herself': 'himself',
                         'woman': 'man',
                         'women': 'men',
                         'girl': 'boy',
                         'girls': 'boys',
                         'mother': 'father',
                         'mom': 'dad',
                         'daughter': 'son',
                         'sister': 'brother',
                         'aunt': 'uncle',
                         'niece': 'nephew',
                         'wife': 'husband',
                         'bride': 'groom',
                         'queen': 'king',
                         'princess': 'prince',
                         'female': 'male',
                         "ma'am": 'sir',
                         'ms.': 'mr.',
                         'miss': 'mister',
                         'chairwoman': 'chairman',
                         'businesswoman': 'businessman',
                         'congresswoman': 'congressman',
                         'stewardess': 'steward',
                         'actress': 'actor',
                         'waitress': 'waiter',
                         'policewoman': 'policeman',
                         'firewoman': 'fireman',
                         'mailwoman': 'mailman',
                         'saleswoman': 'salesman',
                         'spokeswoman': 'spokesman',
                         'landlady': 'landlord',
                         'hostess': 'host',
                         'lady': 'gentleman',
                         'grandmother': 'grandfather',
                         'grandma': 'grandpa',
                         'mama': 'papa',
                         'mommy': 'daddy',
                         'daughter-in-law': 'son-in-law',
                         'sister-in-law': 'brother-in-law',
                         'mother-in-law': 'father-in-law',
                         'queenpin': 'kingpin',
                         'godmother': 'godfather',
                         'sugar mommy': 'sugar daddy'}

# Modifying the religion_dict using the list of religions from the ethnicity_dict
religion_dict = {
    "buddhism": {
        "founder": "siddhartha gautama",
        "practitioner": "buddhist",
        "deity": [],
        "place of prayer": "temple",
        "known place": ["bodh gaya", "sarnath", "lumbini"],
        "holy text": ["tripitaka", "mahayana sutra"],
        "religious leader": ["dalai lama", "thich nhat hanh"]
    },
    "christianity": {
        "founder": "jesus christ",
        "practitioner": "christian",
        "deity": ["god", "jesus", "holy spirit"],
        "place of prayer": "church",
        "known place": ["jerusalem", "vatican city", "canterbury cathedral"],
        "holy text": ["bible", "catechism of the catholic church", "book of common prayer"],
        "religious leader": ["pope francis", "archbishop of canterbury"]
    },
    "confucianism": {
        "founder": "confucius",
        "practitioner": "confucian",
        "deity": [],
        "place of prayer": "temple",
        "known place": ["temple of confucius", "confucian temple of shanghai", "confucius' family mansion"],
        "holy text": ["analects", "mencius", "the great learning"],
        "religious leader": []
    },
    "hinduism": {
        "founder": "unknown",
        "practitioner": "hindu",
        "deity": ["brahma", "vishnu", "shiva"],
        "place of prayer": "temple",
        "known place": ["varanasi", "haridwar", "ujjain"],
        "holy text": ["veda", "upanishad", "bhagavad gita"],
        "religious leader": ["swami vivekananda", "sri sri ravi shankar"]
    },
    "islam": {
        "founder": "muhammad",
        "practitioner": "muslim",
        "deity": ["allah"],
        "place of prayer": "mosque",
        "known place": ["mecca", "medina", "al-aqsa mosque"],
        "holy text": ["quran", "hadith"],
        "religious leader": ["imam", "mufti"]
    },
    "judaism": {
        "founder": "abraham",
        "practitioner": "jew",
        "deity": ["god"],
        "place of prayer": "synagogue",
        "known place": ["jerusalem", "western wall", "bethlehem"],
        "holy text": ["tanakh", "talmud"],
        "religious leader": ["rabbi", "hazzan"]
    },
    "sikhism": {
        "founder": "Guru Nanak",
        "practitioner": "Sikh",
        "deity": "One God (Waheguru)",
        "place of prayer": "Gurdwara",
        "known places": ["Harmandir Sahib (Golden Temple)", "Nankana Sahib"],
        "holy texts": ["Guru Granth Sahib"],
        "religious leaders": ["Guru Nanak", "Guru Gobind Singh", "Guru Arjan", "Guru Tegh Bahadur"]
    }
}

minority_groups = ['african american', 'black', 'hispanic', 'latinx', 'native american', 'indigenous',
                   'asian american', 'pacific islander', 'middle eastern', 'arab', 'south asian', 'desi',
                   'jewish', 'roma', 'romani', 'afro-latinx', 'afro-caribbean', 'afro-asian', 'afro-arab',
                   'indigenous peoples of south america, central america, and the caribbean',
                   'other indigenous peoples', 'mixed', 'multiracial individuals']
