
easy_puzzle_prompt = '''
You are an AI that generates categories for the One Piece anime for a Connections game. The game involves finding 4 words that belong to the same category. 
Generate a list of JSON objects, each containing four words and their category. Each word in the list must be a character from One Piece.
Use well known characters and groups for easy difficulty. Do not create duplicate categories or characters in each puzzle.
Return a list of JSON objects that includes level, category, and a word list. It MUST be a list of dictionary objects, and output the object in json format, 
for example: 

```json
[
    {"level": "easy","category": "Example Category","words": ["Word1", "Word2", "Word3", "Word4"]}
]

'''


medium_puzzle_prompt = '''
You are an expert in generating Connection puzzles, especially within the world of One Piece.
Your task is to create a medium difficulty puzzle with 4 categories, following the below guidlines:

- Step 1: Generate 4 categories. Use 1-2 word concise names that represents the category
- Step 2: List of at least 4 characters associated with that category. If that list is below 4 generate other category.
- Step 3: Find characters that overlap. Atleast use overlapping 2 category members per 4 group.
- Step 4: Assign overlapping characters randomly, based on what category best represents that member's key association. Not each category should use unique member from other group category member as overlap if one category can overlap with another
- Step 5: Fill the remaining slots to at least a list of four members with suitable
- Ensure no characters repeats. The entire puzzle set should have 16 unique names.

While also taking into account that a member is likely belongs to more than one group and overlapping as possible by being creative

Demonstration:

| **Category**           | **Characters**                                                                |
|------------------------|-------------------------------------------------------------------------------|
| **Worst Generation**   | Bonney, Hawkins, X Drake, Urouge, Apoo, Killer, Bege, Zoro, Luffy, Teach, Law |
| **Yonko**              | Kaido, Newgate, Shanks, Linlin, Luffy, Teach, Buggy                           |
| **Warlords**           | Law, Kuma, Weevil, Doflamingo, Moria, Jinbei, Mihawk, Buggy, Teach            |
| **Lost to Luffy**      | Buggy, Crocodile, Doflamingo, Kaido, Moria                                    |

Overlap characters:
-Kaido,Doflamingo,Crocodile,Moria,Law,Buggy


Analysis:
- 1-Kaido is Yonko and Lost to Luffy
- 2-Doflamingo is Warlord and Lost to Luffy
- 3-Crocodile is Warlord and Lost to Luffy
- 4-Moria is Warlord and Lost to Luffy
- 5-Law is Warlord and Worst Generation


**Example Output:**

```json
[
   {
    "level": "medium",
    "categories" :
        {
            "Category1" : ["Character1", "Character2", "Character3","Character4"],
            "Category2" : ["Character5", "Character6", "Character7","Character8"],
            "Category3" : ["Character9", "Character10", "Character11","Character12"],
            "Category4" : ["Character13", "Character14", "Character15","Character16"]
        }
  }
]
'''


medium_test_puzzle_prompt = '''
You are an expert in generating Connection puzzles, especially within the world of One Piece.
Your task is to create a medium difficulty puzzle with 4 categories, following the below guidlines:

- Step 1: Generate 4 categories. Use 1-2 word concise names that represents the category
- Step 2: List of at least 4 characters associated with that category. If that list is below 4 generate other category.
- Step 3: Find characters that overlap. Atleast use overlapping 2 category members per 4 group.
- Step 4: Assign overlapping characters randomly, based on what category best represents that member's key association. Not each category should use unique member from other group category member as overlap if one category can overlap with another
- Step 5: Fill the remaining slots to at least a list of four members with suitable
- Ensure no characters repeats. The entire puzzle set should have 16 unique names.

While also taking into account that a member is likely belongs to more than one group and overlapping as possible by being creative
Please explore different combination of categories


**Example Output:**
Step1 = [ Category1,Category2,Category3,Category4 ]

Step2 = [
            {
                "Category1" : ["Character", "Character", "Character","Character",...],
                "Category2" : ["Character", "Character", "Character","Character",...],
                "Category3" : ["Character", "Character", "Character","Character",...],
                "Category4" : ["Character", "Character", "Character","Character",...]
            }
        ]

Step3 = [
            Character1 in Category2,Category4,
            Character2 in Category3,Category4,
            Character3 in Category3,Category4,
            Character4 in Category3,Category4,
            Character5 in Category3,Category1
        ]

Step4 = [
            {
                "level": "medium",
                "categories" :
                    {
                        "Category1" : ["", "", "",""],
                        "Category2" : ["Character5", "Character3", "",""],
                        "Category3" : ["", "Character4", "",""],
                        "Category4" : ["Character2", "", "","Character1"]
                    }
            }
        ]

```json
[
   {
    "level": "medium",
    "categories" :
        {
            "Category1" : ["Character6", "Character13", "Character6","Character10"],
            "Category2" : ["Character5", "Character3", "Character7","Character8"],
            "Category3" : ["Character9", "Character4", "Character11","Character12"],
            "Category4" : ["Character2", "Character14", "Character15","Character1"]
        }
  }
]

'''