


########################################################
# CONSOLE v0.1 #########################################
########################################################
#
#
#
########################################################
########################################################
########################################################

import  _
import  shutil

import  text

match               = text.match
gsub                = text.gsub
xmatch              = text.xmatch
addbox              = text.addbox
xoffset             = text.xoffset
fixlen              = text.fixlen
ln                  = text.ln
lrspctaboff         = text.lrspctaboff
lrspctabeoloff      = text.lrspctabeoloff
lspctaboff          = text.lspctaboff
rspctaboff          = text.rspctaboff

####################################################

WIDTH           = shutil.get_terminal_size().columns

CON_STAT_SET    = ""
CON_STAT_CLR    = ""
CON_STAT_TEXT   = ""
CON_STATON      = False

####################################################

def stat_clr():
    print( "\r" + CON_STAT_CLR + "\r", end = "" )

#___________________________

def stat_set():
    print( "\r" + CON_STAT_SET + "\r", end = "" )

#___________________________

def conl( msg = "" ):

    if CON_STATON:
        stat_clr()

    print( msg )

    _.LOGSTR[ str( len( _.LOGSTR ) ) ] = ln( msg )

    if hasattr( _, "LOG" ):

        if _.LOG != "":
            t = str( msg )

            tt = text.csioff( t )
            #tt = gsub( tt, r"(\n|\n?\r)(\n|\n?\r)+", _.EOL )

            with open( _.LOG, "a", encoding="utf-8" ) as f:
                f.write( tt )

    if CON_STATON:
        stat_set()


################################################

def con( msg ):

    print( msg, end = "" )


####################################################

def conline( msg = "", f = None ):

    if msg != "":
        msg = "_ " + msg + " "

    x = WIDTH - 4
    x = x - len( msg )

    if x > 0:
        msg = msg + "_" * x
    else:
        msg = msg[ 0:x ]

    msg = "\r " + msg + "\r"

    msg = ln() + ln( msg ) + ln()

    if f is None:

        conl( msg )

    msg += ln()

    return msg

####################################################

def conpush():

    return "\x1B" + "7"


################################################

def conpop():
    return "\x1B" + "8"


################################################

def consetxy( x, y ):
   
    return f"\x1B[{y + 1};{x + 1}H"


####################################################

def stat( msg = "" ):

    global CON_STATON, CON_STAT_SET, CON_STAT_CLR, CON_STAT_TEXT

    if msg == "":

        if CON_STATON:
            stat_clr()
            CON_STATON = False

    else:

        if msg != ".":

            CON_STAT_TEXT = msg

        msg = CON_STAT_TEXT

        if CON_STATON:
            if msg != CON_STAT_SET:
                stat_clr()

        CON_STAT_SET = msg
        CON_STAT_CLR = " " * len( msg )
        CON_STATON = True

        stat_set()


####################################################

def iscont( prompt = "Continue? (yes): " ):

    while True:
        answer = input( prompt ).strip().lower()

        t = "\r" + " " * ( WIDTH - 1 ) + "\r"
        con( t )

        # If user just pressed Enter, return default if provided
        if answer:
            if answer in ( "y", "yes" ):
                return True

        conl( "EXIT" )
        conl()

        return False


########################################################
########################################################
########################################################


