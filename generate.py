from groq import Groq
import os

#GROQ GENERATE POEM
def generate_poem(data):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f""" First imagine, you're little girl from Thailand and love to write poem, create the poem about comparing weather forcast tomorrow from these three locations:
    {data[0]['location']}: {data[0]['temperature']}°C, wind {data[0]['wind']}
    {data[1]['location']}: {data[1]['temperature']}°C, wind {data[1]['wind']}
    {data[2]['location']}: {data[2]['temperature']}°C, wind {data[2]['wind']}
    Example:
    Warm sun kisses Hua Hin’s shore,
    Bangkok hums with rain once more,
    Aalborg whispers cold and grey,
    Where would you rather stay?

    แดดอุ่นที่หัวหินพริ้มไหว
    กรุงเทพฝนพรำไม่จางหาย
    อัลบอร์กหนาวลมพัดแรง
    ที่ไหนกันนะ น่าไปแฝงกาย

    requirements:
    - describe weather through feelings and imagery ONLY, never mention actual numbers
    - the tempurature and wind can be anywhere mentioned in the sentence, no need to be at the strict order
    - English poem must feel natural and lyrical, not like a weather report
    - Thai poem should be translated beautifully and rhyme together
    - each rhyming word must be DIFFERENT, no repeating the same word twice
    - be creative and playful, surprise the reader
    - respond with PLAIN TEXT ONLY, no markdown symbols like *, **, ###
    - no dashes or separators between English and Thai
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages =[{"role": "user", "content": prompt}],
        temperature=1)

    return response.choices[0].message.content

#SAVE POEM
def save_poem(poem):
    with open("docs/poem.txt", "w", encoding="utf-8") as f:
        f.write(poem)