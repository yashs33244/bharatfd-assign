# backend/faq/translations.py
import googletrans

translator = googletrans.Translator()

def translate_text(text, target_language):
    """
    Translate text using Google Translate
    
    :param text: Text to translate
    :param target_language: Target language code
    :return: Translated text or original if translation fails
    """
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception:
        return text  # Fallback to original text