#!python
# -*- coding: utf-8 -*-

import sys
import qi
import wikipedia

class WikiService:
    """Implements a qiMessaging interface for the Wikipedia Python module"""

    def __init__(self, session):
        # we need a pointer to the session to call other services later
        self.session = session
        self.name = "Wikipedia"
        self.lang = None
        self.ttsToWikiLang = {
            'English': 'en',
            'Japanese': 'jp'
        }
        self.ttsToDialogLang = {
            'English': 'enu',
            'Japanese': 'jpj'
        }

    def search(self, pattern):
        """Sets the dynamic concept and return a sentence to be said"""
        try:
            self._setLanguage()
        except RuntimeError:
            return 'error'
        search = wikipedia.search(pattern)
        if len(search) == 0:
            return 'no results'
        try:
            self.session.service('ALDialog').setConcept('WikiSearchResults',
                self.ttsToDialogLang[self.lang], search[:3], _async=True)
        except RuntimeError:
            return 'error'
        enum = ' or '.join(search[:3])
        sc = set(['.','-','?'])
        enum = ''.join([c if c not in sc else ' ' for c in enum])
        ans = 'do you want to know more about ' + enum
        qi.logInfo('wikipedia.service', ans)
        return ans

    def get_summary(self, reference):
        """Gets the summary of a page given its official name
           It is advised to first run a search and use one of the titles
           returned by the search.
        """
        try:
            self._setLanguage()
        except RuntimeError:
            return 'error'
        qi.logInfo('wikipedia.service', 
                   'Looking for summary for the word' + reference.strip('" '))
        return wikipedia.summary(reference.strip('" '))

    def _setLanguage(self):
        """sets the language according to the current robot language"""
        self.lang = self.session.service('ALTextToSpeech').getLanguage()
        # you should try catch for unsupported languages here
        wikipedia.set_lang(self.ttsToWikiLang[self.lang])


def register_service(session):
    """Registers the service to make it available to everyone"""
    myService = WikiService(session)
    return session.registerService(myService.name, myService)

def main():
    app = qi.Application(sys.argv)
    app.start()
    session = app.session
    register_service(session)
    app.run()


if __name__ == "__main__":
    main()
