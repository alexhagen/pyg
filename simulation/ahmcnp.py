''' mcnp input decks can be programmed in an object oriented
way to narrow the scope possible and thus to keep better
agreement of parameters between problems '''

class mcnp(object):
    cells = {};
    currcell = 1;
    surfaces = {};
    currsurf = 1;
    materials = {};
    currmatl = 1;
    msgblock = '';
    titlecard = '';
    cellcards = '';
    surfacecards = '';
    datacards = '';
    inputstr = '';
    filename = '';
    def __init__(self):
        # initialize here!
        pass;
    def __del__(self):
        # destroy here!
        pass;
    def add_message(self,msg):
        # write a message block creator
        pass;
    def add_surface(self):
        # write a generalized surface addition function
        pass;
    def compileinp(self,_filename):
        # write one with a new filename
        self.filename = _filename;
        pass;
    def compileinp(self):
        # now compile with the built in file name