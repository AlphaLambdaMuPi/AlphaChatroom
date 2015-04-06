import re

class Regex:
    def __init__(self):
        self.init_forbidden_char()
        self.init_emoticon_regex()
        self.init_latex_regex()
        self.init_url_regex()
        #self.init_youtube_regex()

    def init_forbidden_char(self):
        self.forbid = {
                '^': r'\^',
                '$': r'\$',
            }

    def sub_forbidden_char(self, s):
        for x in self.forbid:
            s = s.replace(x, self.forbid[x])
        return s

    def init_emoticon_regex(self):
        self.emoregexs = []
        with open('data/emoticon.map', 'r') as f:
            for line in f:
                emos, x, y = line.split()
                emos = self.sub_forbidden_char(emos)
                print(emos)
                self.emoregexs.append(
                    (re.compile(emos), r'<img src=Image://emoticon/{}-{}>'.format(x, y))
                )
        self.emoregexs.append(
            (re.compile(r'\\\(\(emoticon:(\d+)-(\d+)\)\)'), r'<img src=Image://emoticon/\1-\2>')
        )

    def init_latex_regex(self):
        self.latexregex = (
            re.compile('\$([^$]+)\$'),
            r'<img src="http://latex.codecogs.com/png.latex?\1"/>',
        )

    #def 

    def init_url_regex(self):
        self.urlregex = (
            re.compile('(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'),
            r'<a href="\1">\1</a>',
        )


    def sub(self, s):
        for reg in self.emoregexs:
            s = reg[0].sub(reg[1], s)

        s = self.urlregex[0].sub(self.urlregex[1], s)
        s = self.latexregex[0].sub(self.latexregex[1], s)

        return s


R = Regex()

def do_sub(s):
    s = R.sub(s)
    return s
