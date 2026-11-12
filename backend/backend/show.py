from database import get_all_faqs
for f in get_all_faqs():
    if f['category'] == 'Faculty':
        print(f['question'], "=>", f['answer'])