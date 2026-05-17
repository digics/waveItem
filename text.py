


########################################################
# TEXT v0.1 ############################################
########################################################
#
#
"""

import  text

regex               = text.regex
match               = text.match
gsub                = text.gsub
xmatch              = text.xmatch
addbox              = text.addbox
xoffset             = text.xoffset
fixlen              = text.fixlen
csioff                = text.csioff
ln                  = text.ln
lrspctaboff         = text.lrspctaboff
lrspctabeoloff      = text.lrspctabeoloff
lspctaboff          = text.lspctaboff
rspctaboff          = text.rspctaboff
blank               = text.blank

text.totext
text.formatime
text.unformatime

"""
#
#
########################################################
########################################################
########################################################

import  _
import  re
import  sys

from    typing      import  Any, Pattern, Dict

from    ansi2html   import  Ansi2HTMLConverter





import  common

exit                = common.exit
fatal               = common.fatal
warning             = common.warning
getime              = common.getime

import  _

####################################################


REGEX: Dict[ str, Pattern ] = {}
REGEX[ "^" ] = re.compile( r"a\A" )

DEFAULT_BOX_ATTR        = ""

WIDTH_MAX               = 0
WIDTH_LOWX              = 0
GSUBQNT                 = 0

####################################################

def totext( t ):

    if isinstance( t, str ):

        return t

    return t.decode( "utf-8", errors = "replace" )


####################################################

def ansi_html( t ):

    conv = Ansi2HTMLConverter(

        inline = True,
        line_wrap = False )

    return f'<div style="white-space: pre;">{conv.convert( t )}</div>'



def zansi_html( t):

    conv = Ansi2HTMLConverter( inline = True, line_wrap = False )
    html = conv.convert( t, full = False )

    return (
        '<div style="white-space: pre; overflow-x: auto; '
        'font-family: monospace;">'
        f'{html}'
        '</div>' )



####################################################

def formatime( t ):

    h, r = divmod( int( t ), 3600 )
    m, s = divmod( r, 60 )

    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"

    return f"{m:02d}:{s:02d}"


################################################

def unformatime( t ):

    A = {}
    match( t, r"(((\d+):)?(\d+):)?(\d+(\.\d+)?)", A )
    h = m = s = 0

    if A[ "3" ] is not None:
        h = int( A[ "3" ] )

    if A[ "4" ] is not None:
        m = int( A[ "4" ] )

    s = float( A[ "5" ] )

    t = h * 3600 + m * 60 + s

    return t

####################################################

def ln( t = "" ):

    if t == "" or t is None:
        t = _.EOL

    elif t[ -1 ] != "\x0A":

        t += _.EOL
   
    return t


####################################################

def lastln( t ):

    if not t:
        return ""

    t = gsub( t, "(?s)^.*[\x0A\x0D]+" )

    return t


####################################################

def lrspctaboff( t ):

    return gsub( t, r"^[\x09\x20\xA0]+|[\x09\x20\xA0]+$" )


################################################

def lrspctabeoloff( t ):

    return gsub( t, r"^[\x09\x0A\x0D\x20\xA0]+|[\x09\x0A\x0D\x20\xA0]+$" )


################################################

def lspctaboff( t ):

    return gsub( t, r"^[\x09\x20\xA0]+" )

################################################

def rspctaboff( t ):

    return gsub( t, r"[\x09\x20\xA0]+$" )





####################################################

def csioff( t ):

    t = gsub( t, r"\x1B\[([^mfHK]*[mfHK]|[suH]|2J)" )

    return t


####################################################

def fixlen( s, n, fill = " " ):

    if not isinstance( s, str ):
        s = str( s )

    t = s
    #t = csioff( t )
    q = len( t )

    f = n - q

    if f > 0:
        s += fill * f
    elif f < 0:
        s = s[ :f ] 

    return s


################################################

def size( v ):

    if v < 1024:

        # bytes

        sx = ""

    elif v < 1024 * 1024:

        # kbytes

        v /= 1024

        sx = "KB"

    elif v < 1024 * 1024 * 1024:

        # mb

        v /= 1024 * 1024

        sx = "MB"

    else:

        # gb

        v /= 1024 * 1024 * 1024


        sx = "GB"

    v = int( v * 100 ) / 100


    r = f"{v} {sx}"

    return r


################################################

def rfixlen( s, n, fill = " " ):

    s = str( s )

    if len( s ) > n:

        return s[ :n ]

    return s.rjust( n, fill )


####################################################

def width( t ):

    global WIDTH_LOWX, WIDTH_MAX

    if not t:
        return WIDTH_MAX

    lines = t.splitlines()

    WIDTH_MAX = 0
    WIDTH_LOWX = 9999999

    for line in lines:

        l = len( line )
        if l > WIDTH_MAX:
            WIDTH_MAX = l

        m = re.search( r"[^\x09\x20\xA0]", line )
        if m:
            x = m.start()

            if WIDTH_LOWX == 0 or x < WIDTH_LOWX:
                WIDTH_LOWX = x

    return WIDTH_MAX


####################################################

def xoffset( t, s ):

    if isinstance( t, str ):

        if s == 0:
            return t

        if s < 0:

            s = -s
            t = re.sub( r"\x0A[\x09\x20\xA0]{" + f"{s}" + r"}", "\x0A", "\x0A" + t )
            t = t[1:]

        else:

            t = gsub( "\x0A" + t, r"\x0A", "\x0A" + " " * s )
           
        t = gsub( t, r"^\x0A" )
        t = gsub( t, r"[\x09\x20\xA0]+$" )

    else:

        t = ""

    return t


####################################################

def emplnoff( t ):

    t = gsub( t, r"^([\x09\x20\xA0]*\x0D?\x0A)+|(\x0D?\x0A[\x09\x20\xA0]*)+$" )
    t = gsub( t, r"(\x0D?\x0A[\x09\x20\xA0]*){2,}", _.EOL )

    return t


####################################################

def set_default_box_attr( attr ):

    global DEFAULT_BOX_ATTR

    DEFAULT_BOX_ATTR = attr

#___________________________

def addbox( title, box, tcolor = "", bcolor = None ):

    if bcolor == None:
        bcolor = DEFAULT_BOX_ATTR

    title = gsub( title, r"[\x0D\x0A]+" )

    x = len( csioff( title ) )

    title = tcolor + title

    if match( box, r"^\x00" ):
        box = box[ 1: ]
        x = 4

    box = xoffset( box, x )
    box = box[ x: ]
    box = bcolor + box

    txt = title + box
    txt = ln( txt )

    return txt


########################################################
# REGEX v0.1 ###########################################
########################################################

# regex error problem


def regex_basic( r, pfx = None, default_regex = "$_^" ):

    # r may be str/dict/list
    # if r is empty (=="") then r = default_regex
    # if pfx is not none then return str: pfx + r
    # otherwise returns compiled regex object 
    #_______________________________

    global REGEX

    if isinstance( r, dict ):
        r = "|".join( r.keys() )

    elif isinstance( r, list ):
        r = "|".join( str( i ) for i in r )

    elif not isinstance( r, str ):
        return r

    if r == "":
        r = default_regex

    if pfx is not None:
        return pfx + r

    if r in REGEX:
        return REGEX[ r ]

    try:

        c = re.compile( r )

    except re.error as e:

        e = str( e )
        fatal( f'Regex compile error: "{r}" -> {e}' )

    REGEX[ r ] = c
    return c

regex = regex_basic


####################################################

def gsub0( src, rx, rp = "" ):

    global GSUBQNT

    src, GSUBQNT = re.subn( rx, rp, src )

    return src


def gsub( src, rx, rp = "" ):

    r = regex( rx )

    return gsub0( src, r, rp )


####################################################

def blank( t ):

    return gsub( t, r"[^ te]", " " )


####################################################

def tabx( t, ts = 6 ):

    def tabx0( t, ts, x ):

        A = {}
        if match( t, r"\x09+", A ):

            l = A[ "-1" ]
            x += len( l )

            w = A[ "0L" ] - 1
            m = ts * w

            w = len( ts )

            w = ( int( ( x + w ) / w ) * w ) - x
            
            m = ts[ 0:w ] + m

            x += len( m )
            t = l + m + tabx0( A[ "+1" ], ts, x )

        t = l + m + r

        return t

    #___________________________

    if ts > 0:

        ts = "\x20" + "\x20" * ( ts - 1 )

        lines = t.splitlines()

        t = ""

        for line in lines:

            t += ln( tabx0( line, ts, 0 ) )

    return t


####################################################

def match( t, rxp = None, D = None ):

    if D is None:
        D = {}

    if t is None:
        return None

    D.clear()

    rx = regex( rxp )

    m = rx.search( t )

    D[ "regex" ] = rxp

    if not m:
        D[ "-1" ]   = t
        D[ "0" ]    = ""
        D[ "+1" ]   = None
        return ""

    s, e = m.span( 0 )

    D[ "-1" ]       = t[ :s ]
    D[ "0" ]        = t[ s:e ]
    D[ "0S" ]       = s
    D[ "0L" ]       = len( D[ "0" ] )
    D[ "+1" ]       = t[ e: ]

    for i, v in enumerate( m.groups(), 1 ):
        D[ str( i ) ] = v

    for i, v in m.groupdict().items():
        if v is not None:
            D[ i ] = v

    if len( D[ "0" ] ):
        return D[ "0" ][ 0 ]

    return ""
  

####################################################



def rdacc( D, i = None ):

    if i is None:

        return rdacc( D, -9 )

    it = str( i )

    t = D.get( i, "" )
    if t is None:
        t = ""

    if i > -2:

        return D.get( "-1" )

    t += rdacc( D, i + 1 )

    D[ it ] = ""

    return t




def suidx( D, i, t ):

    if i + "<" in D:
        t = lspctaboff( t )

    if i + ">" in D:
        t = rspctaboff( t )

    if i + "<>" in D:
        t = lrspctaboff( t )

    if i + "~" in D:

        r = D[ i + "~" ]


        S[ "+1" ] = D[ "+1" ]
        S[ "+1S" ] = D[ "+1S" ]
        S[ "regex" ] = D[ i + "~" ]

        xmatch( S )

        D[ i + "~" ] = rdacc( S )

        D[ "+1" ] = S[ "+1" ]
        D[ "+1S" ] = S[ "+1S" ]


    if i + "^" in D:

        c = D[ i + "^" ]
        t = globals()[ c ]( D, t )

    if i + "@" in D:

        t = globals()[ D[ i + "@" ] ]( D, t )

    t = D.get( i + "<", "" ) + t + D.get( i + ">", "" )

    if i + "_" in D:

        t = blank( t )

    return t


















def wracc( D, i, t ):

    if i > 1:

        fatal( f"wracc( D, bad accumulator: {i} )" )

    if i == 0:

        l = D[ "+1"][ :D[ "0S" ] ]
        r = D[ "+1"][ D[ "0S" ] + D[ "0L" ]: ]
        D[ "+1" ] = l + t + r

    elif i == -1:

        l = D[ "+1"][ :D[ "-1S" ] ]
        r = D[ "+1"][ D[ "+1S" ]: ]
        D[ "+1" ] = l + t + r

    else:

        it = str( i )

        s = D.get( it, "" )
        s += str( rdacc( D, i + 1 ) )
        s += t
        D[ it ] = s













def xmatch( D, r = None, T = None ):

    if isinstance( D, str ):

        T = {}
        T[ "+1" ] = D
        T[ "regex" ] = r

        return xmatch( T )

    # D[ "+1" ]       = srcstring
    # D[ "regex" ]    = regex
    #___________________________

    def xmatch_pre( D ):

        if "-1" in D:

            D[ "-1" ] = suidx( D, "-1", D[ "-1" ] )

        i = D.get( "", "" )
        if i == "":
            i = -2
        else:
            i = int( i )

        if "0" in D:
            t = suidx( D, "0", D[ "0" ] )
        else:
            t = ""

        wracc( D, i, t )

     #___________________________           

    def xmatch0( D, r = None ):

        xmatch_pre( D )

        for i in list( D ):
            if i not in ( "+1", "+1S", "regex", "-2", "-3", "-4", "-5" ):
                del D[ i ]

        if "+1" not in D or D[ "+1" ] is None:
            D[ "+1S" ] = -1
        elif "+1S" not in D:
            D[ "+1S" ] = 0

        s = D[ "+1S" ]
        if s == -1:
            return None

        if s > len( D[ "+1" ] ):
            D[ "+1S" ] = -1
            return None



        if r is None:
            r = D[ "regex" ]

        rx = regex( r )
        m = rx.search( D[ "+1" ][ s: ] )

        D[ "-1S" ] = s

        if not m:
            D[ "-1" ] = D[ "+1" ][ s: ]
            D[ "-1L" ] = len( D[ "-1" ] )
            D[ "0" ] = ""
            D[ "0S" ] = len( D[ "+1" ] )
            D[ "0L" ] = 0
            D[ "+1S" ] = -1
            return ""

        start, end = m.span(0)

        D[ "-1" ] = D[ "+1" ][ s:s + start ]
        D[ "-1L" ] = len( D[ "-1" ] )

        D[ "0" ] = m.group( 0 )
        D[ "0S" ] = s + start
        D[ "0L" ] = len( D[ "0" ] )

        D[ "+1S"] = s + end

        for i, t in enumerate( m.groups(), 1 ):
            if t is not None:
                ii = i
                i = str( i )
                D[ i ] = t
                D[ f"{i}S" ] = s + m.start( ii )
                D[ f"{i}L" ] = len( t )

        for i, t in m.groupdict().items():
            if t is not None:
                D[ i ] = t
                D[ f"{i}S" ] = s + m.start( i )
                D[ f"{i}L" ] = len( D[ i ] )

        if len( D[ "0" ] ):

            return D[ "0" ][ 0 ]

        return ""

    #___________________________

    def xcoord( D, s ):

        A = {}
        r = match( D[ "+1" ][ :s ], r"[^e]*$", A )

        return A[ "0L" ]

    #___________________________

    def xmatch_xbox_capture( D ):

        s = D[ "xboxS" ]
        
        x = xcoord( D, s + 1 )

        #print( f"X: {x}" )
        #print( D[ "+1" ][ s: ] )

        r =   r"^[^e]*((`eol)" \
            + r"(([ t]{" + str( x ) + r"}[^e]*" \
            + r"|[ t]*)((`eol)|$))*)?"

        rx = regex( r )

        s = D[ "+1S" ]
        m = rx.search( D[ "+1" ][ s: ] )
        if m:

            start, end = m.span( 0 )

            xb = m.group( 0 )

            xxb = gsub( xb, r"[ ]*((`eol)[ t]*)*$" )
            
            end -= len( xb ) - len( xxb )

            D[ "0" ] = D[ "0" ] + xxb
            D[ "+1S" ] += end - start

            t = m.group( 0 )

            x = x + D[ "0L" ] - 1

            D[ "0L" ] = len( D[ "0" ] )

            t = " " * x + t

            width( t )

            x = WIDTH_LOWX

            t = xoffset( t, -x )

            if 1:
                t = re.sub( regex( r"^[\x09\x20\xA0]+" ), "", t, count = 1 )
                t = re.sub( regex( r"[\x09\x20\xA0]*(\x0D?\x0A[\x09\x20\xA0]*)*$" ), "", t, count = 1 )

            D[ "xbox" ] = t

    #___________________________

    r = xmatch0( D )

    if r is not None:

        if "xbox" in D:

            xmatch_xbox_capture( D )

    return r






def patsplit( t, r, A, B ):

    A = []
    B = []

    le = 0
    for m in re.finditer( t, s ):

        s, e = m.span()

        B.append( s[ le:s ] )
        A.append( m.group() )

        le = e

    B.append( s[ le: ] )

    return A, B

#_______________________________________


def retab( A, B, a, q, b ):

    return ""





########################################################
########################################################
########################################################


####################################################

REGEX_BREATHE       = {}

REGEXSTR            = ""

regex_breathe_      = regex


#_______________________________________

def addregexmac0( r, rp ):

    _.REGEXMAC0[ r ] = rp



def regex_breathe( t ):

    global  REGEX

    t = str( t )
    r = t
    if t not in REGEX:

        # \t\t              >   [\x09\x20\xA0]
        # <white_field>     >   tab
        # [^ te             >   [^\x09\x0A\x0D\x20\xA0
        # [^e               >   [^\x0A\x0D
        # [e                >   [\x0A\x0D
        # [^ t              >   [^\x09\x20\xA0
        # [ t               >   [\x09\x20\xA0
        # [^<space>         >   [^\x20\xA0
        # [<space>          >   [\x20\xA0
        # (`name<tab>       >   (?P<name>
        # (`int             >   ([0-9]+
        # (`fract           >   ([0-9]+(\.[9-0]+)?
        # (`eol             >   (\x0D?\x0A
        # ^<                >   \<

        #for r in _.REGEXMAC0:

            #rp = _.REGEXMAC0[ r ]

            #print( f"IN: {t}" )
            #print( f"REGEX: {r}" )
            #print( f"REPL: {rp}" )

            #t = gsub0( t, r, rp )

            #print( f"OUT: {t}" )
            #print()

        t = gsub0( r, r"\x09\x09([^\x09]|$)",   "\xB7\\1" )

        t = gsub0( t, r"[\x20\xA0]*[\x09\x0A\x0D][\x09\x0A\x0D\x20\xA0]*", "\x09" )

        #t = gsub0( t, r"\(`styles",             r"(`style	(jungle|tec(hno)?|hardcore|dnb|break)" )

        t = gsub0( t, r"\(`int",                r"([0-9]+" )
        t = gsub0( t, r"\(`float",              r"([0-9]+(\\.[0-9]+)?" )
        t = gsub0( t, r"\(`eol",                r"(\\x0D?\\x0A" )

        t = gsub0( t, r"\(\x60([^\x09\x0A\x0D]*)\x09", r"(?P<\1>" )
        t = gsub0( t, r"[\x20\xA0]*[\x09\x0A\x0D][\x09\x0A\x0D\x20\xA0]*", "\x09" )

        t = gsub0( t, r"\[\^ te",               r"[^\\x09\\x0A\\x0D\\x20\\xA0" )
        t = gsub0( t, r"\[\^e",                 r"[^\\x0A\\x0D" )
        t = gsub0( t, r"\[e",                   r"[\\x0A\\x0D" )
        t = gsub0( t, r"\[\^ t",                r"[^\\x09\\x20\\xA0" )
        t = gsub0( t, r"\[ te",                 r"[\\x09\\x0A\\x0D\\x20\\xA0" )
        t = gsub0( t, r"\[ t",                  r"[\\x09\\x20\\xA0" )
        t = gsub0( t, r"\[\^ ",                 r"[^\\x20\\xA0" )
        t = gsub0( t, r"\[ ",                   r"[\\x20\\xA0" )




        #t = gsub0( t, r"^<",                    r"\\x0A[\\x09\\x20\\xA0]*"  )
        t = gsub0( t, r"\xB7",                  r"[\\x09\\x20\\xA0]" )





        REGEX[ r ] = regex_breathe_( t )

    _.REGEXSTR = REGEX[ r ]

    return REGEX[ r ]

#_______________________________________

regex               = regex_breathe

########################################################
########################################################
########################################################






