from openai import OpenAI
import base64
from PIL import Image
import pytesseract
import cv2
import json
from dotenv import load_dotenv, find_dotenv
import ast
load_dotenv(find_dotenv(), override=True)
class imageInterpretor():
    def __init__(self):
        self.client = OpenAI()
        self.vision_model = 'gpt-4-vision-preview'
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    def get_used_language(self, image_path):
        base64_image = self.encode_image(image_path)
        response = self.client.chat.completions.create(
        model=self.vision_model,
        messages=[
            {"role": "user","content": [
                {"type": "text", "text": "Just print the name of the language that is predominantly used in the doc, If there's no text then print 'none'. Also if there is headlines in the given image assign 'true' else if there's only a statement or paragrapgh then assign 'false' in the 'headline_tag' field. In the 'headline' field assign the found headline text as it in the given language that is found in the image. Use this template provide a json response '{'language':'english','headline_tag':'false', 'headline':'content'}' and don't generate anything else."},
                {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
                ]
                }
                ],max_tokens=200)
        output = ast.literal_eval(str(response.choices[0].message.content).lower())
        print("lll", output, "kkkk")
        if "hindi" in output["language"] or "हिंदी" in output["language"]:
            output["language"] = "hindi"
            output["tess_lang"] = "hin"
            return output
        elif "arabic"  in output["language"] or "عربي"  in output["language"]:
            output["language"] = "arabic"
            output["tess_lang"] = "ara"
            return output
        elif "telugu"  in output["language"] or "తెలుగు"  in output["language"]:
            output["language"] = "telugu"
            output["tess_lang"] = "tel"
            return output
        elif "malayalam"  in output["language"] or "മലയാളം"  in output["language"]:
            output["language"] = "malayalam"
            output["tess_lang"] = "mal"
            return output
        elif "tamil"  in output["language"] or "தமிழ்"  in output["language"]:
            output["language"] = "tamil"
            output["tess_lang"] = "tam"
            return output
        elif "gujarati"  in output["language"] or "ગુજરાતી"  in output["language"]:
            output["language"] = "gujarati"
            output["tess_lang"] = "guj"
            return output
        elif "english" in output["language"]:
            output["language"] = "english"
            output["tess_lang"] = "eng"
            return output
        else:
            return "none"
    def get_text(self, image_path):
        identified_langauge = self.get_used_language(image_path=image_path)
        if identified_langauge!="none":
            text = pytesseract.image_to_string(Image.open(image_path), lang=identified_langauge["tess_lang"])
            return text,identified_langauge
        else:
            return "none",identified_langauge
    def translate(self, image_path):
        input_text = self.get_text(image_path=image_path)
        if input_text[0]!="none":
            language_obj = input_text[1]
            transcript = input_text[0]
            output = {}
            if language_obj["headline_tag"]=="false":
                response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": f"You are a helpful interperator who can translate {language_obj['language'].capitalize()} transcription in English. Any terms that can't be understood or not known, simply transliterate them."},
                    {"role": "user", "content": f"'{transcript}'.Interpret the transcript to english elaborately."}
                ]
                )
                output_response = response.choices[0].message.content
                output["headline_tag"] = "false"
                output['headline'] = 'none'
                output['description'] = output_response
                summary_response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant who can summarize context."},
                    {"role": "user", "content":  f"'{output_response}'. Summarize the give passage not more than in 10 or within 10 lines based on it's size."}
                ]
                )
                output["summary"] = summary_response.choices[0].message.content

            elif language_obj["headline_tag"].lower()=="true":
                response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": f"You are a helpful interperator who can translate {language_obj['language'].capitalize()} transcription in English. Any terms that can't be understood or not known, simply transliterate them"},
                    {"role": "user", "content": f"'{transcript}'.Interpret the transcript to english elaborately."}
                ]
                )
                output_response = response.choices[0].message.content
                response_ = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": f"You are a helpful interperator who can translate {language_obj['language'].capitalize()} transcription in English. Any terms that can't be understood or not known, simply transliterate them"},
                    {"role": "user", "content": f"'{transcript}'.Translate headline given in the transcript to english, just generate the headline and nothing else, headlines are conceived based on the first two sentences from the given transcript. Make the headline short. Shouldn't be more than 10 words"}
                ]
                )
                headline_response = response_.choices[0].message.content
                output["headline_tag"] = 'true'
                output['headline'] = headline_response.replace('\\"', '').replace('""', '"')
                output['description'] = output_response
                summary_response = self.client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant who can summarize context."},
                    {"role": "user", "content":  f"'{output_response}'. Summarize the give passage not more than in 10 or within 10 lines based on it's size."}
                ]
                )
                output["summary"] = summary_response.choices[0].message.content
            return output
        else:
            return "none"
        
#img_inter = imageInterpretor
#value = img_inter.translate()
#print(value)