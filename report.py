








########################################################
# REPORT v0.1 ##########################################
########################################################




# status: add qbit
# dobavit v Report datu vremja reporta

# move vendors without packs down

# report base: output bit/qbit correctly sorted


        # if error == 0 then do not output
        # if split == 0 then do not output ? others???

# repalette report



from    colorama    import  init, Fore, Back, Style
init(autoreset=True)

from datetime import datetime, timezone




import  io_

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

import  _con

conl                = _con.conl
conline             = _con.conline
stat                = _con.stat
iscont              = _con.iscont

import  common

exit                = common.exit
fatal               = common.fatal
warning             = common.warning
getime              = common.getime

import  _

####################################################

REPORT_WIDTH            = 70
REPORT_WIDTH_STEP       = 4
REPORT_PARAM_WIDTH      = 20

INDEX_OFFSET            = 0

SAMPLEPACKPTR           = {}
VENDORPTR               = {}


####################################################

TITLE_STRING        = "waveItem v0.96 by digi_cs 9 May 2026"

ERROR_COLOR         = Fore.LIGHTRED_EX
RESET_COLOR         = Style.RESET_ALL

PACK_COLOR          = Fore.WHITE
NORMAL_COLOR        = Fore.WHITE 
VENDOR_COLOR        = Fore.WHITE 
REPORT_COLOR        = Fore.WHITE
HEADER_COLOR        = Fore.LIGHTWHITE_EX
BIT_COLOR           = Fore.YELLOW

TOWAV_COLOR         = Fore.CYAN
NORM_COLOR          = Fore.GREEN
SPLIT_COLOR         = Fore.CYAN
TRIM_COLOR          = Fore.GREEN
DUP_COLOR           = Fore.MAGENTA
ORACLE_COLOR        = Fore.YELLOW
SORT_COLOR          = Fore.WHITE
QBIT_COLOR          = Fore.LIGHTRED_EX



#SHORT_COLOR
#ZERO_COLOR


OUTPUT_COL1         = 7
OUTPUT_COL2         = 15
OUTPUT_COL3         = 22

EXITING             = ""

####################################################

def title():

    return TITLE_STRING


####################################################

def help():

    return """
Usage:

  waveitem [options]

Options:

  --import <folder>     set import folder                                   default: <current folder>

  --attr <number>       set operation flags:                                default: 0b101110111 (0x177)

                            D9 == 1: TOWAV                                  default: 1
                            D8 == 1: RESCAN                                 default: 0
                            D7 == 1: NORM                                   default: 1
                            D6 == 1: QBIT                                   default: 1
                            D5 == 1: SPLIT                                  default: 1
                            D4 == 1: LEFTRIM                                default: 1
                            D3 == 1: RIGHTRIM                               default: 0
                            D2 == 1: DUP                                    default: 1
                            D1 == 1: ORACLE                                 default: 1
                            D0 == 1: SORT                                   default: 1

  --towav    -towav         enable / disable non-wav-files conversion       default: ask user
  --norm     -norm          enable / disable normalize op                   default: 1
  --qbit     -qbit          enable / disable qbit op                        default: 1
  --split    -split         enable / disable split op                       default: 1
  --leftrim  -leftrim       enable / disable leftrim op                     default: 1
  --rightrim -rightrim      enable / disable rightrim op                    default: 0
  --dup      -dup           enable / disable check duplicates               default: 1
  --oracle   -oracle        enable / disable oracle op                      default: 1
  --sort     -sort          enable / disable quality sample sort            default: 1

  --yes      -yes           answer: yes / no
  --no       -no            answer: no / yes 

Other:

  --help                show this help and exit
  --version             show version information and exit"""












####################################################
#
# waveItem v0.7 by digi_cs 18 Mar 2026
#
#    IMPORT  C:/WAV2/_IMPORT/
#    VENDOR  C:/WAV2/_IMPORT/vendor
#    TEMP    C:/WAV2/_IMPORT/_TEMP/
#    LIST    C:/WAV2/_IMPORT/item
#    LOG     C:/WAV2/_IMPORT/wav.log
#
#    OPS:    TOWAV
#            RESCAN
#            NORMALIZE
#            QBIT
#            SPLIT
#            LEFTRIM
#            RIGHTRIM
#            DUP
#            ORACLE
#            SORT
#
####################################################

def begin():

    def _params():

        i = _.IMPORT
        l = _.LIST
        v = _.VENDOR

        t = ln() + RESET_COLOR      + \
            ln( f"IMPORT  {i}" )    + \
            ln( f"ITEM    {l}" )    + \
            ln( f"VENDOR  {v}" )    + \
            ln()

        return t

    #___________________________

    def _attr():

        t = ""

        attr = _.ATTR

        if attr & _.MASK_ATTR_TOWAV:
            t += ln(                 "TOWAV" )

        if attr & _.MASK_ATTR_RESCAN:
            t += ln(                 "RESCAN" )

        if attr & _.MASK_ATTR_NORM:
            t += ln( NORM_COLOR +    "NORM" )

        if attr & _.MASK_ATTR_QBIT:
            t += ln( QBIT_COLOR +    "QBIT" )

        if attr & _.MASK_ATTR_SPLIT:
            t += ln( SPLIT_COLOR +   "SPLIT" )

        if attr & _.MASK_ATTR_LEFTRIM:
            t += ln( TRIM_COLOR +    "LEFTRIM" )

        if attr & _.MASK_ATTR_RIGHTRIM:
            t += ln( TRIM_COLOR +    "RIGHTRIM" )

        if attr & _.MASK_ATTR_DUP:
            t += ln( DUP_COLOR +     "DUP" )

        if attr & _.MASK_ATTR_ORACLE:
            t += ln( ORACLE_COLOR +  "ORACLE" )

        if attr & _.MASK_ATTR_SORT:
            t += ln( SORT_COLOR +    "SORT" )

        if not match( text.csioff( t ), r"[^\x00-\x20\x7F]" ):
            t = "-"

        t = addbox( "OPS:    ", t, RESET_COLOR, "" )

        return t

    #___________________________

    t = _params()

    t += _attr()

    t = xoffset( t, 4 )

    return t

################################################

def result_file_towav():

    if _.TOWAV == "":
        return ""

    t = addbox( "TOWAV  ", _.TOWAV, TOWAV_COLOR )

    t = ln( t ) + ln()

    t = xoffset( t, 7 )

    return t


################################################


















####################################################
#
# 12345  192000 24 2  0.393  65%  filepath
#
#        +25.5%
#        SPLIT  8     error: jkhkjhgg mkj nnnmn hghg
#                     asda a a s asdsdas
#
# 12345  192000 24 2  0.393  65%  filepath
#
#        +25 %
#        -100000      -100000
#
# 12345  192000 24 2  0.393  65%  filepath
#
#        +25 %
#        LEFTRIM      error: jkhkjhgg mkj nnnmn hghg
#                     asda a a s asdsdas
#
# 12345  192000 24 2  0.393  65%  filepath
#
#        +25 %
#        -100000      error: jkhkjhgg mkj nnnmn hghg
#                     asda a a s asdsdas
#
####################################################

def time_period( t ):

    px = "-" if t < 0 else ""

    t = abs( t )

    if t < 0.001:

        t *= 1000000
        sx = "us"

    elif t < 1:

        t *= 1000
        sx = "ms"

    else:

        sx = "sec"

    t = int( t * 100 ) / 100

    t = f"{px}{t} {sx}"

    return t


########################################

_.FORCEXIT = 0

def report_item( item ):

    t = item.time
    if t is None or t == 0:
        t = "-"
    else:
        t = round_time( t )

    v = item.vol
    if v is None or v == 0:
        v = "-"
    else:
        v = f"{round_percent( v )}%"

    sr = item.rate
    if sr is None or sr == 0:
         sr = "-"

    b = item.bit
    if b is None or b == 0:
         b = "-"

    c = item.channels
    if c is None or c == 0:
         c = "-"

    r = item.rating
    if r == 0:
        r = "-"

    i = item.index

    #if _.GLOBAL_TAB_CNTR > 0:
    #
    #if i > 203:
    #    _.FORCEXIT = 1


    i = fixlen( f"{i}", 7 )
    sr = fixlen( f"{sr}", 7 )
    b = fixlen( f"{b}", 3 )
    c = fixlen( f"{c}", 3 )
    t = fixlen( f"{t}", 7 )
    v = fixlen( f"{v}", 8 )
    r = fixlen( f"{r}", 6 )
    f = trim_filepath( item.filepath )

    t = i + sr + b + c + t + v + r + f

    t = ln( t )

    _.LASTITEMREPORT = t

    return t


################################################

def round_time( v ):

    v = int( v * 100 ) / 100
    return v


####################################################

def item_result():

    ################################

    def item_norm():

        x = OUTPUT_COL2
        v = _.NORM

        if v is None:
            return ""

        if isinstance( v, str ):

            txt = addbox( "NORM     ", v, NORM_COLOR )

        else:

            v = round_percent( v )
            c = NORM_COLOR
            if v > _.NORMALIZE_LEVEL_ALERT:
                c = ERROR_COLOR

            txt = ln( c + f"+{v}%" )

        return txt


    ################################

    def item_qbit():

        txt = ""

        v = _.QBIT

        if v != "":

            txt = addbox( "QBIT     ", fixlen( v, 19 ) + str( _.QBIT_SUFFIX ), QBIT_COLOR )

        return txt


    ################################

    def item_split():

        x = OUTPUT_COL3
        v = _.SPLIT
        t = _.SPLITQ

        if t is None:
            return ""

        r = SPLIT_COLOR
        if isinstance( t, str ):

            r = ERROR_COLOR if t.startswith( "ERROR" ) else SPLIT_COLOR

            if t != "":

                t = fixlen( t, 12 )

            if v is not None:

                if not isinstance( v, str ):

                    v = str( v )

                t = addbox( t, v, "", "" )

        elif t is not None:

            t = str( t )

        t = addbox( "SPLIT    ", t, "", r )
        t = SPLIT_COLOR + t

        return t


    ################################

    def item_trim():

        x = OUTPUT_COL2

        l = _.LEFTRIM
        r = _.RIGHTRIM

        txt = ""

        if l is not None:

            if isinstance( l, str ):

                txt = "LEFTRIM  "
                txt = addbox( txt, l, TRIM_COLOR ) 

                return txt

            else:

                txt = time_period( l )
                txt = fixlen( txt, x )

        if r is not None:

            if isinstance( r, str ):

                txt = addbox( txt, r, TRIM_COLOR )

            else:

                txt += time_period( r )

        if match( text.csioff( txt ), r"[^\x09\x20\xA0]" ):
            return ln( TRIM_COLOR + txt )

        return ""


    ################################

    def item_dup():

        v = _.DUP

        txt = ""

        if v is not None:

            txt = addbox( "DUPWITH  ", v, DUP_COLOR, "" )

        return txt

    ################################

    def item_error():

        v = _.ERROR

        if v is None:

            return ""

        v = addbox( "ERROR   ", v, ERROR_COLOR )

        return v

    ################################

    t =  item_norm()
    #t += "!"
    t += item_qbit()
    #t += "!"
    t += item_split()
    #t += "@"
    t += item_trim()
    #t += "#"
    t += item_dup()
    #t += "$"
    t += item_error()
    #t += "^"

    x = OUTPUT_COL1
    t = xoffset( t, x )

    _.LASTITEMREPORT = _.LASTITEMREPORT + t

    return t




























































################################################
#
# STATUS SUFFIX:
#
#  STCR2_HRH_158_Vocal_Phrase_Cataclysm_DRY_Fmin ...     0  0  0/0  0  0  1/7942  47:38  0%  00:00
#
#                    N   S     LT/RT    D  E  C  T    P    EST   TIME
#
#                   100  23  -600/-100  8  3  1/1792  0%  47:38  00:00 
#                  9999  9999  -100000/-100000  9999  9999  9999/9999  99%  01:59:59  01:59:59
#
################################################

def estimated_time( time, idx, total ):

    if idx <= 0:
        return 0

    peritem = time / idx
    r = total - idx

    return peritem * r


#___________________________________

def status_suffix( items, idx ):

    n   = _.FILES[ "NORM" ]
    s   = _.FILES[ "SPLIT" ]
    sq  = _.SPLITCNT
    lt  = _.FILES[ "LEFTRIM" ]
    rt  = _.FILES[ "RIGHTRIM" ]
    d   = _.FILES[ "DUP" ]
    e   = _.FILES[ "ERROR" ]
    q   = _.FILES[ "QBIT" ]

    t = " "                          + \
        f"{NORM_COLOR}{n}  "         + \
        f"{SPLIT_COLOR}{s} (+{sq})  " + \
        f"{QBIT_COLOR}{q}  "         + \
        f"{TRIM_COLOR}{lt}/{rt}  "   + \
        f"{DUP_COLOR}{d}  "          + \
        f"{ERROR_COLOR}{e}  "

        
    t += status_suffix_main( items, idx )

    return t




####################################################

def status_suffix_main( items, idx ):

    item = items[ idx ]

    t = f"{RESET_COLOR}"

    q = _.TOTAL

    i = item.index
    ni = int( gsub( str( i ), r"[A-Z]+" ) )

    t += f"{i}/{q}  "

    p = percent( ni, q )
    t += f"{p}%  "

    l = getime() - _.STARTIME

    e = estimated_time( l, idx, q )
    e = text.formatime( e )
    
    l = text.formatime( l )
    t += f"{e}  {l} "

    return t

#___________________________________

def status_path( f, w ):

    f = io_.filename( f )

    l = len( f )
    if l < w:

        f = f + " " * ( w - l )

    elif l > w:

        f = f[ -w: ]

    return f

#___________________________________

def status_extra( f, x ):

    if EXITING:

        t = EXITING

    else:

        #    t = status_path( f, x )
        t = ""

    t = fixlen( t, x )

    return t

#_______________________________________

def status( items, idx ):

    item = items[ idx ]

    t = status_suffix( items, idx )

    x = _con.WIDTH
    x = x - len( text.csioff( t ) )

    s = status_extra( item.filepath, x )

    t = s + t

    stat( t )










##########################################


def status_suffix_towav( items, idx ):

    e = _.FILES[ "ERRORTOWAV" ]

    t = " " + f"{ERROR_COLOR}{e}  "

    t += status_suffix_main( items, idx )

    return t


#___________________________________


def status_towav( f, items, i ):

    t = status_suffix_towav( items, i )

    x = _con.WIDTH
    x -= len( text.csioff( t ) )

    s = "TOWAV: "
    x -= len( s )

    s = TOWAV_COLOR + s + RESET_COLOR + status_path( f, x )
    t = s + t

    stat( t )

    return t
















































####################################################

def draw_header( n, w = None, rt = "" ):

    if w is None:
        w = REPORT_WIDTH
    #___________________

    if n != "":
        n += ": "

    if rt != "":
        rt = " " + rt

    n += "#" * ( w - len( n ) )

    n = HEADER_COLOR + ln( "_" * w + rt ) + ln( n ) + ln()

    return n

#_______________________________________

def print_years( pw, bd, ed ):

    if bd != 0:

        bd = year_epoch( bd )
        ed = year_epoch( ed )
        bd = f"{bd}" if bd == ed else f"{bd}-{ed}"

        return ln( fixlen( "YEARS", pw ) + bd ) + ln()

    return ""









################################################

def round_percent( v ):

    v = int( v * 10 ) / 10

    iv = int( v )

    if v == iv:

        return iv

    return v


#_______________________________________

def percent( v, q ):

    if q == 0:

            return 100

    pr = v / q * 100

    pr = round_percent( pr )

    return pr

#_______________________________________

def year_epoch( epoch ):

    return datetime.fromtimestamp( int( epoch ), tz = timezone.utc ).year

#_______________________________________

def epoch_year( year ):

    return datetime( int( year ), 1, 1, tzinfo=timezone.utc).timestamp()

#_______________________________________

def trim_filepath( p, f = None ):

    if f is None:
        f = _.IMPORT

    if f != "":

        if p.startswith( f ):

            p = "./" + p[ len( f ): ]

    return p

#_______________________________________

def untrim_filepath( p, f = None ):

    if f is None:
        f = _.IMPORT

    if f != "":

        if p.startswith( "./" ):

            p = f + p[ 2: ]

    return io_.filepath( p )

#_______________________________________

def minmax( d, bd, ed ):

    if bd == 0 or d < bd:
        bd = d

    if ed == 0 or d > ed:
        ed = d

    return bd, ed


####################################################







################################################
#
# FINAL REPORT:
#        
#        PROC            100             30477
#        
#        OK              100             30477
#        ERROR           0               0
#        
#        DUP             5               1802
#        
#        NORM            40              12273
#        SPLIT           2               670 (+2220)
#        TRIM            20 / 0          6358 / 0
################################################

def end():

    h = conline( "REPORT", 1 )

    t = _.REPORT

    t = gsub( t, r"(?s)(___+[^_]*)___.*", r"\1" )
    t = gsub( t, r"(?s)(^[^#]*###+[e]+)(.*)", r"\2" )

    t = xoffset( t, 4 )

    t = h + t

    return t

















class ReportBase:

    FIELDS = ( ( "size",                "GB",    1, NORMAL_COLOR ),
               ( "total",               ".",     1, NORMAL_COLOR ),
               ( "proc",                "%",     1, NORMAL_COLOR ),
               ( "ok",                  "%",     0, NORMAL_COLOR ),
               ( "error",               "%",     1, ERROR_COLOR  ),
               ( "dup",                 "%",     1, DUP_COLOR    ),
               ( "norm",                "%",     0, NORM_COLOR   ),
               ( "split",               "%()",   0, SPLIT_COLOR  ),
               ( "trim",                "%/%",   1, TRIM_COLOR   ),
               ( r"[0-9]+",             "%",     1, BIT_COLOR    ),
               ( r"[0-9]+:[0-9]+",      "%%",    1, QBIT_COLOR   ) )

    #___________________________

    def load( p, t ):

        return t

    #___________________________

    def __init__( p, t = "" ):

        p.total     = 0
        p.size      = 0
        p.proc      = 0
        p.ok        = 0
        p.error     = 0
        p.dup       = 0
        p.norm      = 0
        p.split     = 0
        p.splitcnt  = 0
        p.leftrim   = 0
        p.rightrim  = 0
        p.bits      = {}
        p.qbit      = {}

        if t != "":

            p.load( t )

    #___________________________

    def _apply( p, r, sign ):

        p.total     += sign * r.total
        p.size      += r.size
        p.proc      += sign * r.proc
        p.ok        += sign * r.ok
        p.error     += sign * r.error
        p.dup       += sign * r.dup
        p.norm      += sign * r.norm
        p.split     += sign * r.split
        p.splitcnt  += sign * r.splitcnt
        p.leftrim   += sign * r.leftrim
        p.rightrim  += sign * r.rightrim

        for k, v in r.bits.items():
            p.bits[ k ] = p.bits.get( k, 0 ) + sign * v

        for k, v in r.qbit.items():
            p.qbit[ k ] = p.qbit.get( k, 0 ) + sign * v

    #___________________________

    def __iadd__( p, r ):

        p._apply( r, 1 )
        return p

    #___________________________

    def __isub__( p, r ):

        p._apply( r, -1 )
        return p

    #___________________________

    def report( p, w, pw ):

        st = REPORT_WIDTH_STEP

        if w is None:
            w = REPORT_WIDTH - st * 4

        if pw is None:
            pw = REPORT_PARAM_WIDTH - st * 2

        pw2 = pw + st * 4
        #_______________

        A = {}
        F = p.FIELDS
        q = p.total
        tb2 = 9
        t = ""
        for n, op, f, c in F:

            nh = n.upper()

            if n == nh:

                break

            if op == "GB":

                a = getattr( p, n )
                a = text.size( a )
                b = ""

            elif op == "%/%":

                l = "lef" + n
                r = "righ" + n

                a = b = ""
                    
                l = getattr( p, l )
                a = str( percent( l, q ) )
                b = str( l )

                r = getattr( p, r )
                a += f" / {str( percent( r, q ) )}"
                b += f" / {str( r )}"

            else:

                b = getattr( p, n )

                if op == "%()":

                    a = str( percent( b, q ) )

                    if b != 0:

                        n += "cnt"
                        if hasattr( p, n ):

                            r = getattr( p, n )
                            b = fixlen( f"{b}", tb2 ) + f"+{r}"
        
                elif hasattr( p, n ):

                    if op == ".":

                        a = "%"
                        z = p.splitcnt + b
                        b = fixlen( f"{b}", tb2 ) + SPLIT_COLOR + f"{z}"

                    else:
                        a = str( percent( b, q ) )

                else:

                    fatal( f"unknown field: {n}" )

            a = fixlen( a, pw2 - pw ) + str( b )
            a = fixlen( nh, pw ) + a

            t += ln( f"{c}{a}" )
            t += ln() * f

            if q == 0:

                break
        #_______________

        s = ""
        if q != 0:

            cb = BIT_COLOR
            cq = QBIT_COLOR

            for n, b in sorted( p.bits.items(), key = lambda x: int( x[ 0 ] ) ):
            
                tt = ""
                qq = 0

                for qn, bb in sorted( p.qbit.items(), key = lambda x: int( x[ 0 ].split( ":" )[ 0 ] ) ):

                    if qn.endswith( ":" + n ):

                        qq += bb

                        a = str( percent( bb, q ) )
   
                        a = fixlen( "  " + qn, pw ) + fixlen( a, pw2 - pw ) + fixlen( bb, tb2 )

                        tt += ln( f"{cq}{a}" )

                za = str( percent( b, q ) )
                zb = fixlen( b - qq, tb2 )

                if qq > 0:

                    zb += cq + str( b )

                za = fixlen( za, pw2 - pw ) + str( zb )
                za = fixlen( n, pw ) + za

                s += ln( f"{cb}{za}" ) + ln()

                
                if tt != "":

                    tt = gsub( tt, r"[e]+$" )

                    tt += ln( str( qq ) )

                    s += tt + ln()
        #_______________

        t = t + s

        return t


####################################################

PACK_PATH           = {}

def add_pack_path( path, pp ):

    global PACK_PATH

    if path is not None:

        path = io_.FILEPATH( path )

        PACK_PATH[ path ] = pp

#___________________________________________

def get_file_pack( ft ):

    # returns sample pack name
    #_______________________

    global PACK_PATH


    fp = io_.FILEPATH( ft )

    ff = ""
    pp = _.USERPACK
    for f, p in PACK_PATH.items():

        if fp.startswith( f ) and len( f ) > len( ff ):

            pp = p
            ff = f

    #if match( ft, r"currupt" ):

    #    conl( f">>>>>>>>>>>>>>>>>>>>>>> CURRUPT: {pp.name}" )

    return pp


############################################

def vendor_match( n, rp = None ):

    # return vendor_ptr, flag
    #
    #   flag:
    #
    #       == 0 no match           _.USERVENDORPTR
    #       == 1 match partially    
    #       == 2 match total
    #___________________

    if rp is None:
        rp = _.REPORTPTR

    #conl( f"vendor match: {n}" )

    A = {}
    for vp in rp.vendors:

        r = vp.regex[ "" ]

        if match( n, r, A ):

            if A[ "0L" ] == len( n ):

                return vp, 2

            elif "" in vp.nregex:

                if match( n, vp.nregex[ "" ] ):

                    continue

            return vp, 1

    return _.USERVENDOR, 0

#___________________________________________

def def_pack( name, path, vp = None ):

    if vp is None:

        vp, f = vendor_match( name )

    f = path
    if f is None:
        f = ""
    else:
        f = "    <    " + f

    zonl( f"DEF PACK ({vp.name}): {name}{f}" )

    pp = Pack( name )

    if path is not None:
        pp.path = path

    if vp is not None:

        if hasattr( pp, "vendor" ):

            pvp = pp.vendor
        
            if pvp != vp:

                if pp in pvp.packs:

                    del pvp.packs[ pp ]
    
        pp.vendor = vp

        vp.packs[ pp ] = 1

    add_pack_path( path, pp )

    return pp

#___________________________________________

class Pack( ReportBase ):

    def __new__( cls, name = "", t = "" ):

        global SAMPLEPACKPTR

        name = name.upper()

        if name in SAMPLEPACKPTR:
            pp  = SAMPLEPACKPTR[ name ]

        else:
            pp = super().__new__( cls )

            SAMPLEPACKPTR[ name ] = pp
            pp.name = name
            pp.initf = 1

        return pp

    #___________________________

    def load( pp, t ):

        A = {}
        if match( t, r"<PATH		+([^e]*)", A ):

            p = untrim_filepath( rspctaboff( A[ "1" ] ) )
            pp.path = p
            t = A[ "-1" ] + A[ "+1" ]

        if match( t, r"<YEAR		+([^e]*)", A ):

            pp.date      = epoch_year( int( rspctaboff( A[ "1" ] ) ) )
            t = A[ "-1" ] + A[ "+1" ]

        return super().load( t )

    #___________________________

    def __init__( pp, name = "", t = "", vp = None ):

        if pp.initf:
            super().__init__()
            pp.initf = 0

        if vp is not None:

            pp.vendor   = vp

        if t != "":

            pp.load( t )

    #___________________________

    def report( pp, w = None, pw = None ):

        st = REPORT_WIDTH_STEP

        if w is None:
            w = REPORT_WIDTH - st * 4

        if pw is None:
            pw = REPORT_PARAM_WIDTH - st * 2
        #_______________

        s = super().report( w, pw )

        vp = pp.vendor
        v = vp.name
        t = ln( fixlen( "VENDOR"   , pw ) + v )
        t += ln()

        if hasattr( pp, "date" ):
            t += ln( fixlen( "YEAR"     , pw ) + str( year_epoch( pp.date ) ) )
            t += ln()

        if hasattr( pp, "path" ):
            t += ln( fixlen( "PATH"     , pw ) + trim_filepath( pp.path ) )
            t += ln()        
        #_______________

        t = s + PACK_COLOR + t
        t = xoffset( t, st )
        t = draw_header( pp.name, w, "SAMPLE-PACK" ) + t

        return t

    #___________________________

    def count( pp, t, st = None ):

        if st is None:
            st = 1

        A = t.split( "|" )

        i = 0
        q = len( A )

        while i < q:

            n = A[ i ]
            i += 1

            if n != "":

                if match( n, r"^\d\d?|^\d\d?:\d\d?" ):

                    if ":" in n:

                        pp.qbit[ n ] = pp.qbit.get( n, 0 ) + st

                    else:

                        pp.bits[ n ] = pp.bits.get( n, 0 ) + st

                elif hasattr( pp, n ):

                    if _.GLOBAL_TAB_CNTR > 0:

                        if n in ( "norm", "leftrim", "rightrim" ):

                            i += 1
                            continue

                    if n == "size":

                        setattr( pp, n, getattr( pp, n ) + int( A[ i ] ) )

                        i += 1
                        continue

                    setattr( pp, n, getattr( pp, n ) + st )

                    #if n == "split":

                    #    n += "cnt"
                    #    v = int( A[ i ] )

                    #    if hasattr( pp, n ):

                    #        setattr( pp, n, getattr( pp, n ) + v * st )

                else:

                    fatal( f"regop( {n}: unknown group )" )

            i += 1




####################################################

def _get_regex( R ):

    t = ""
    for r in R:
        if r != "":
            if t != "":
                t += "|"
            t += r

    R[ "" ] = "(?i)" + t

#_______________________________________

def toregex( r ):

    #return r 

    r = gsub( r, r"([.(){}\[\]+])", r"\\\1" )

    return r 

#_______________________________________

def zonl( t = "" ):

    if _.VENDORPACK_INFO:

        return conl( t )

#_______________________________________

class Vendor( ReportBase ):

    def __new__( cls, vendor = "", t = "" ):

        global VENDORPTR

        vendor = vendor.upper()

        if vendor in VENDORPTR:

            vp = VENDORPTR[ vendor ]

        else:

            vp = super().__new__( cls )
            VENDORPTR[ vendor ] = vp

            zonl( f"defining vendor {vendor}'" )

            vp.name = vendor
            vp.initf = 1

        return vp

    #___________________________

    def load( vp, t ):

        def addpack( vp, pp ):

            vp.packs[ pp ] = 1

            pp.vendor = vp

        #_______________

        D = {}
        D[ "+1" ] = "\x0A" + t
        D[ "regex" ] = r"\x0A		*((`xbox	(`pack	[^e:]*):[ te])|(`flag	!)?~		*(`rxp	[^ te]*))"

        lt = ""
        while True:

            r = xmatch( D )
            lt += D[ "-1" ]

            if r == "":
                break

            if "rxp" in D:

                r = D[ "rxp" ]
                if r == "":
                    continue

                r = lrspctaboff( r )
                #r = toregex( r )

                if "flag" in D and D[ "flag" ] == "!":

                    vp.nregex[ r ] = 1
                    _get_regex( vp.nregex )

                else:

                    vp.regex[ r ] = 1
                    _get_regex( vp.regex )

            else:

                pn = D[ "pack" ]
                pt = D[ "xbox" ]

                pp = Pack( pn, pt )
                
                if hasattr( pp, "path" ):
                    s = pp.path
                else:
                    s = None
                    
                def_pack( pp.name, s, vp )

        return lt

    #___________________________

    def __init__( vp, vendor = "", t = "" ):

        if vp.initf:

            super().__init__()



            vendor = vendor.upper()

            vp.nregex   = {}

            vp.regex    = {}
            
            r = vendor
            #r = toregex( r )
            vp.regex[ r ] = 1
            _get_regex( vp.regex )

            vp.packs    = {}

            if t != "":

                vp.load( t )

    #___________________________

    def report( vp, w, pw ):

        st = REPORT_WIDTH_STEP

        if w is None:
            w = REPORT_WIDTH - st * 2

        if pw is None:
            pw = REPORT_PARAM_WIDTH - st
        #_______________

        ReportBase.__init__( vp )

        s = ""
        bd = ed = 0
        for pp in vp.packs:

            pp.vendor = vp

            s += pp.report( w - st * 2 , pw - st )
            vp += pp

            if hasattr( pp, "date" ):

                bd, ed = minmax( pp.date, bd, ed )

        #_______________

        t = ""
        for r in vp.regex:
            r = r.upper()
            if r != "" and r != vp.name:
                t += ln( f"~{r}" )
        if t != "":
            t += ln()

        nt = ""
        for r in vp.nregex:
            if r != "":
                nt += ln( f"!~{r}" )
        if nt != "":
            nt += ln()

        t += nt

        #_______________

        t += super().report( w, pw ) + VENDOR_COLOR
        t += print_years( pw, bd, ed )
        t += ln( fixlen( "PACKS", pw ) + f"{len( vp.packs )}" )
        t += ln()
        t += s
        t = xoffset( t, st )
        t = draw_header( vp.name, w, "VENDOR" ) + t

        return t


####################################################

class Report( ReportBase ):

    def load( rp, t ):

        V = {}
        D = {}
        D[ "+1" ] = "\x0A" + t
        D[ "regex" ] = r"\x0A		*(`xbox	(`vendor	[^e:]*):[ te])"

        lt = ""
        while True:

            r = xmatch( D )
            lt += D[ "-1" ]
            if r == "":
                break

            v = D[ "vendor" ]

            if v not in V:
                V[ v ] = ""

            V[ v ] += D[ "xbox" ]

        for v in V:

            vp = Vendor( v, V[ v ] )
            rp.vendors[ vp ] = 1

        return lt

    #___________________________

    def __init__( rp, t = "" ):

        _.REPORTPTR = rp

        super().__init__()

        rp.packs        = 0
        rp.vendors      = {}

        if t != "":

            rp.load( t )
        
    #___________________________

    def report( rp, w = None, pw = None ):

        if w is None:
            w = REPORT_WIDTH

        if pw is None:
            pw = REPORT_PARAM_WIDTH
        #_______________

        st = REPORT_WIDTH_STEP

        ReportBase.__init__( rp )

        s = ""
        pk = bd = ed = 0
        for vp in rp.vendors:

            s += vp.report( w - st * 2, pw - st )
            rp += vp
            pk += len( vp.packs )

            for pp in vp.packs:

                if hasattr( pp, "date" ):

                    bd, ed = minmax( pp.date, bd, ed )

        rp.packs = pk

        tm = int( getime() )

        tt = tm - _.SESSION_START
        tt += _.TIMECNT
        tt = text.formatime( tt )

        tm = str( datetime.fromtimestamp( tm ) ) + " " * 6 + tt
        t = ln( fixlen( "DATE", pw ) + tm )
        t += ln()
        t += super().report( w, pw ) + REPORT_COLOR

        t += ln( fixlen( "PACKS", pw ) + f"{rp.packs}" )
        t += ln()
        t += print_years( pw, bd, ed )
        t += ln( fixlen( "VENDORS", pw ) + f"{len( rp.vendors )}" )
        t += ln()
        t += s
        #t = xoffset( t, st )
        t = draw_header( "", w ) + t

        _.REPORT = t

        return t




























































########################################################
########################################################
########################################################


