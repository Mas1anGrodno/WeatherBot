from deep_translator import GoogleTranslator

translated = GoogleTranslator(source="en", target="ru").translate("keep it up, you are awesome")

print(translated)
