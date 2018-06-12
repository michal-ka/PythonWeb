#from typing import TextIO, List

from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector

app = Flask(__name__)

#def log_request(req: 'flask_erquest', res: str) -> None:
    # log: TextIO   - first, file version
    # with open('vsearch.log','a') as log:
    #     print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

def log_request(req: 'flask_request', res: str) -> None:
    """Loguje szczegóły żądania sieciowego oraz wyniki."""
    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'Vasteras1',
                'database': 'vsearchlogDB', }

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _SQL = """insert into log
             (phrase, letters, ip, browser_string, results)
             values
             (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
   phrase = request.form['phrase']
   letters = request.form['letters']
   title = 'Oto Twoje wyniki:'
   results = str(search4letters(phrase, letters))
   log_request(request, results)
   return render_template('results.html',
                          the_title=title,
                          the_phrase=phrase,
                          the_letters=letters,
                          the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
   return render_template('entry.html',
                          the_title='Witamy na stronie internetowej search4letters!')

@app.route('/viewlog')
def view_the_log() -> 'html':
    """"Function to present logfile in the browser"""
    with open('vsearch.log') as log:
                        # contents = escape(log.read())
                        # return contents
        contents=[]
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
            #my version working:
            # for line in log:
            #     splitted_line: List[str]=line.split('|')
            #     contents.append(escape(splitted_line))
    titles=('Dane z formularza', 'Adres klienta', 'Agent uzytkownika', 'Wyniki')
    return render_template('viewlog.html',
                           the_title='Widok logu',
                           the_row_titles=titles,
                           the_data=contents,)

if __name__=='__main__':
    app.run(debug=True)
# if __name__ == '__main__':
#    app.run(debug=True)
