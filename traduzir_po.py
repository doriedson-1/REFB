# Traduz arquivos .po automaticamente
import polib
import time
import random
from deep_translator import GoogleTranslator

def translate_po_file(po_filepath, target_lang='en'):
    po = polib.pofile(po_filepath)
    # Define origem automática e destino desejado
    translator = GoogleTranslator(source='auto', target=target_lang)
    
    print(f"Traduzindo: {po_filepath}")
    
    for entry in po:
        # Traduz apenas se estiver vazio
        if not entry.msgstr and entry.msgid:
            try:
                # O deep_translator lida melhor com strings longas e erros
                translation = translator.translate(entry.msgid)
                entry.msgstr = translation
                time.sleep(random.uniform(1,4)) # pausa
                print(f"✅ {entry.msgid} -> {entry.msgstr}")
            except Exception as e:
                print(f"❌ Erro em '{entry.msgid}': {e}")
                time.sleep(10)

    po.save()
    print("\nProcesso finalizado! Não esqueça de rodar 'pybabel compile'.")

# Ajuste o caminho conforme sua estrutura
translate_po_file('locales/en/LC_MESSAGES/messages.po', 'en')
