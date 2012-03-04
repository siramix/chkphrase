import requests as http
from BeautifulSoup import BeautifulSoup as soup
from chkphrase.models import User, Category, PreCategory, Genre, Difficulty, Pack, Phrase
import chkphrase.database as db
from sqlalchemy.exc import IntegrityError

if __name__ == '__main__':
    page_base = 'http://www.enchantedlearning.com'
    main_page = http.get(page_base + '/wordlist/')
    html = soup(main_page.text)
    word_lists = [tag.attrMap['href'] for tag in html.findAll('a', {'href': True}) if tag.attrMap['href'].endswith('.shtml') and tag.attrMap['href'].startswith('/wordlist')]
    count = 0
    dups = 0
    for cur_url in word_lists:
        precategory = cur_url.split('/')[2].split('.')[0]
        print precategory
        db_precategory = PreCategory(precategory)
        db.db_session.add(db_precategory)
        try:
            db.db_session.commit()
        except IntegrityError:
            db.db_session.rollback()
            query = db.db_session.query(PreCategory).filter(PreCategory.name==precategory)
            db_precategory = query[0]
            print 'Duplicate PreCategory'
        list_page = http.get(page_base + cur_url)
        list_html = soup(list_page.text)
        cur_list = [word.strip() for word in list_html.findAll(text=True) if len(word) > 1 and word.startswith("\n")]
        for word in cur_list:
            cur_phrase = Phrase(word, page_base)
            cur_phrase.pre_category_id = db_precategory.id
            db.db_session.add(cur_phrase)
            try:
                db.db_session.commit()
            except IntegrityError:
                db.db_session.rollback()
                dups += 1
                print 'Duplicate!'
        cur_len = len(cur_list)
        count += cur_len
        print cur_len
    print "Total: ", count
    print "Duplicates: ", dups

