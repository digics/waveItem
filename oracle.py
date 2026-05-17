import  _


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
blank               = text.blank


SETYPE              = {}
STYLE               = {}


ORACLE_ITEM         = ""


##################################################

MATCH = {}

def zmatch( t, r, D = None ):

    global  MATCH

    rr = r
    if r not in MATCH:

        # (names? or |names?        >   (\<names?\> or |\<names?\>

        r = gsub( r, r"([(|])([a-z][a-z?]*)",       r"\1\\<\2\\>" )

        print( f"REXP: {r}" )

        MATCH[ rr ] = r

    return text.match( t, MATCH[ rr ], D )



# problems of mask \< 
#




def _oracle( item, f, pn, n, D = {} ):


    #_______________________________________________
    # STYLES #######################################
    #
    #
    #_______________________________________
    # JUNGLE ###############################

    if match( pn, r"(?i)jungle" ):

        setstyle( "jungle" )

    #_______________________________________
    # TECHNO ###############################

    if match( pn, r"(?i)(tec|techno)" ):

        setstyle( "techno" )

    #_______________________________________
    # BREAK ################################

    if match( pn, r"(?i)break" ):

        setstyle( "break" )

    #_______________________________________
    # DNB ##################################

    if match( pn, r"(?i)dnb" ):

        setstyle( "dnb" )

    #_______________________________________
    # DUB ##################################

    if match( pn, r"(?i)dub" ):

        setstyle( "dub" )

    #_______________________________________
    # PSY ##################################

    if match( pn, r"(?i)psy" ):

        setstyle( "psy" )





    #_______________________________________________
    # DRUM (12) #################################### 26
    #
    #   BD      
    #   LP      
    #   OH      
    #   HH
    #   SN
    #   CL
    #   RD
    #   TM      
    #   RM      
    #   PC      
    #   CR      
    #   RV      
    #_______________________________________
    # BD ###################################

    #if not match( pn, r"(?i)kick 2 psytrance" ):

    if match( n, r"(?i)(kick|base)" ):

        setype( "BD" )



    #_______________________________________
    # LP ###################################

    a = match( pn, r"(?i)(drum).*(loop).*(drum)?" )
    b = match( n, r"(?i)(loop)" )
    
    if a or b:

        setype( "LP" )

    #_______________________________________
    # OH ###################################

    if match( pn, r"(?i)(open|op?).*hat" ):

        setype( "OH" )
    #_______________________________________
    # HH ###################################

    if match( pn, r"(?i)(hi-?|closed).*hat" ):

        setype( "HH" )
    #_______________________________________
    # SN ###################################

    if match( pn, r"(?i)(snare)" ):

        setype( "SN" )
    #_______________________________________
    # CL ###################################

    if match( pn, r"(?i)(clap)" ):

        setype( "CL" )
    #_______________________________________
    # RD ###################################

    if match( pn, r"(?i)(ride)" ):

        setype( "RD" )
    #_______________________________________
    # TM ###################################

    if match( pn, r"(?i)(\btom)" ):

        setype( "TM" )
    #_______________________________________
    # RM ###################################

    if match( pn, r"(?i)(rim|click)" ):

        setype( "RM" )
    #_______________________________________
    # PC ###################################

    if match( pn, r"(?i)(perc|shake)" ):

        setype( "PC" )
    #_______________________________________
    # CR ###################################

    if match( pn, r"(?i)(crash|cymbal)" ):

        setype( "CR" )
    #_______________________________________
    # RV ###################################

    if match( pn, r"(?i)(rev).*(crash|cymbal)" ):

        setype( "RV" )













    #_______________________________________________
    # COMMON ELECTRONIC (7) ########################
    #
    #   BS      Bass
    #   SY      Synth      
    #   LD      Lead      
    #   PL      Pluck      
    #   ARP     Arp
    #   PD      Pad
    #   AT      Atmospheric
    #_______________________________________
    # BS ###################################

    if match( pn, r"(?i)(\bbass|\bsub)" ):

        setype( "BS" )
    #_______________________________________
    # SY ###################################

    if match( pn, r"(?i)(synth)" ):

        setype( "SY" )
    #_______________________________________
    # LD ###################################

    if match( pn, r"(?i)(lead)" ):

        setype( "LD" )
    #_______________________________________
    # PL ###################################

    if match( pn, r"(?i)(pluck)" ):

        setype( "PL" )
    #_______________________________________
    # ARP ##################################

    if match( pn, "(?i)(arp)" ):

        setype( "ARP" )
    #_______________________________________
    # PD ###################################

    if match( pn, r"(?i)(pad|string)" ):

        setype( "PD" )
    #_______________________________________
    # AT ###################################

    if match( pn, r"(?i)(atm)" ):

        setype( "AT" )













    #_______________________________________________
    # SPECIAL (2) ##################################
    #
    #   VO      Voice/Vocal
    #
    #   FX      fx
    #
    #_______________________________________
    # FX ###################################

    if match( pn, r"(?i)(fx|eff)" ):

        setype( "FX" )

    #_______________________________________
    # VO ###################################

    if match( pn, r"(?i)(voice|voc|vox)" ):

        setype( "VO" )













    #_______________________________________________
    # INSTRUMENTS (5) ##############################
    #
    #   NE      Ney
    #   SE      Setar
    #   TA      Tar
    #   PI      Piano
    #   GT      Guitar
    #
    #_______________________________________
    # NEY ##################################

    if match( pn, r"(?i)(ney)" ):

        setype( "NE" )

    #_______________________________________
    # SETAR ################################

    if match( pn, r"(?i)(setar)" ):

        setype( "SE" )

    #_______________________________________
    # TAR ##################################

    if match( pn, r"(?i)(\btar)" ):

        setype( "TA" )

    #_______________________________________
    # PIANO ################################

    if match( pn, r"(?i)(piano)" ):

        setype( "PI" )
    #_______________________________________
    # GUITAR ###############################

    if match( n, r"(?i)(\bguitar)" ):

        setype( "GT" )






























def oracle( item, f, pn, pnc, n ):

    # pn is the filepath to item (trimmed by import folder path)
    #   sample-pack's folder name is deleted from pn
    # 
    #___________________________

    global SETYPE, ORACLE_ITEM

    ORACLE_ITEM = item

    SETYPE.clear()
    STYLE.clear()


    _oracle( item, f, pn, n )

    tp = setype()
    if tp == "":

        tp = "_"

    #print( f"TYPE: {tp}    FILE: {item.filepath}" )
    #print()

    # oracle status

    apply_type( item, tp )

    item.libtype = tp




def apply_type( item, tp ):

    T = _.TYPES

    L = tp.split( "|" )

    f = item.filepath

    for i in L:

        #print( f"!!!: {t}" )

        if i not in T:
            T[ i ] = {}

        T[ i ][ f ] = 1







##################################################


def setype( tp = "", item = None ):

    global SETYPE

    if item is None:
        item = ORACLE_ITEM

    if tp != "":

        SETYPE[ tp ] = item
        return

    tp = "|".join( sorted( SETYPE ) )

    if tp != "":

        st = setstyle()

        if st != "":

            tp += " " + st

    return tp




def setstyle( st = "" ):

    global STYLE

    if st != "":

        st = st.upper()

        STYLE[ st ] = 1
        return

    t = "|".join( sorted( STYLE ) )

    STYLE.clear()

    return t










########################################################

def report():

    def files( L ):

        t = ""
        for l in L:

            t += ln( l )

        return t

    #___________________

    T = _.TYPES
    t = ""
    c = 1
    for i in sorted( T.keys() ):

        t += ln( fixlen( str( c ), 6 ) + fixlen( i, 12 ) + str( len( T[ i ] ) ) )
        c += 1

    t = xoffset( t, 4 )

    return t





















































####################################################
# ORACLE ###########################################
####################################################


def gos( L, pn ):

    for p in L:

        r = p.go( pn )
        if r != "":
            return r

    return ""

class   Typer:

    def __init__( p, tp ):

        p.type  = tp
        p.mac   = []

    #_______________________

    def go( p, pn ):

        r = gos( p.mac, pn )
        if r != "":
            return r

        return p.type


class   Matcher:

    def __init__( p, rxp, nt ):

        p.regex = rxp
        p.notf  = nt
        p.mac   = []

    #_______________________

    def go( p, pn ):

        r = p.regex
        f = p.notf

        if match( pn, r ):

            if not f:

                return gos( p.mac, pn )

        elif not f:

            return gos( p.mac, pn )

        




def pathrule( f ):

    p = io_.FPATH( f )

    if p not in PATHRULE:

        t, err = io_.rdfile( f )
        if err:
            return err

        t = text.totext( t )

        r = r"(`xbox	\x0A)		*"                      + \
            r"(((`not	!?)(`op	~)		*(`rxp	[^e]*))"    + \
            r"|(\x0A		*(`type	[0-9A-Z_a-z]+)))"

        D = {}
        D[ "+1" ] = t
        D[ "regex" ] = r

        L, t = get_mask_type( D )

        PATHRULE[ p ] = L 

    return PATHRULE[ p ]



def get_mask_type( D ):

    L = []
    while True:

        r = xmatch( D )

        if r is None:
            break
        
        if r == "":
            continue

        if "op" in D:

            p = Matcher( D[ "rxp" ], D[ "not" ] )

        if "type" in D:

            p = Typer( D[ "type" ] )

        L.append( p )

        P = {}
        P[ "+1" ] = D[ "xbox" ]
        P[ "regex" ] = D[ "regex" ]

        p.mac, t = get_mask_type( P )

        D[ "0" ] = ""

    t = text.rdacc()

    return L, t







