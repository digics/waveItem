



####################################################
####################################################
####################################################
#
#                                                               filepath output: trim
#                                                               towav trashfile: disable ?
#                                                               towav dont generates errors
#                                                               its ok: dup file have it's hash
#                                                               16,24,32 comes before 8-bit in reports
#                                                               remove IGNORE everywhere
#                                                               remove _VENDOR field
#                                                               multi item-files: item-file in subfolders
#                                                               qbit s uchetom gromkosti
#                                                               default import folder: current
#                                                               generate colored report: text.ansi_html
#                                                               generate colored output to item.html
#                                                               get INDEX_OFFSET
#                                                               normalize number shorten
#                                                               what with error files?
#                                                               attr off problem  
#                                                               bug:  LOOPMASTERS - PSYTRANCE INTELLIGENCE VOL.2 446 processed 447 of 24-bit
#                                                               exit by (shift)esc: exit when split group is end
#                                                               implement sample rating parameter
#                                                               inogda oracle(0) after main pass waveitem; needs to restart
#                                                               errors do not pass to staistic
#                                                               convert to wav - ischezajushuj vopros
#                                                               error files comes to list-file w/o attr
#                                                               remove TRASH folder
#                                                               remove IGNORE support
#                                                               leftrim/rightrim do not load from the vendor file
#                                                               replace filename output in status by something more useful
#                                                               enable cleanup_dup
#                                                               budet li teper gluk c indexes pri interrupted pass ????
#                                                               calc item.rating in get()
#                                                               add in qbit message - recalculated item.rating
#                                                               draw item - calc rating
#                                                               rating round to 2
#                                                               ORGANIZE SOURCE
#                                                               .price to .rating
#                                                               dev setup aurostatus == 1
#                                                               waveitem(except towav): handle only status >= 1 (not 0)
#                                                               remove splitout support
#                                                               towav: error files goes to list-file with status 0
#                                                               towav: originals is not deleted
#                                                               towav outputs wrong indexes
#                                                               towav do not shows sample rate and other metainfo )except duration
#                                                               towav slow refresh
#                                                               towav isn't conside towav error files from list
#                                                               when we deletes file - we're don't modify list about it? WE SHOULDN'T DO THAT
#                                                               problems with the non-asc file names
#                                                               split files shouldn't go to statistic: normalize, trims - but to suffix SHOULD GO
#                                                               zablokirovat split dlja split-files
#                                                               draw separator netween TOWAV and WAVITEM MAIN LOOP
#                                                               draw oracle separator
#                                                               create flag of showing vendorpack info
#                                                               eliminate .subtype
#                                                               dup: if duplicate of file is the member of the same group then dup don't go to statistic (and status???)
#                                                               store last session time in vendor file
#                                                               move TYPES to ORACLE part
#                                                               write list file early than cleanup_dup and split_group
#                                                               end output?
#                                                               def command line interface
#                                                               duplicates inside split group isn't deleted
#                                                               duplicates inside split group: reference to original changed
#                                                               add quit to iscont
#                                                               '0' index in report (qbit???): CAUSE ADPCM_MS codec
#                                                               implement number of fields in list file
#                                                               help: modify text due to new and other keys 
#                                                               read_list: away files located outside importfolder
#                                                               if we're copying list file from import-folder to it's subfolder: original list-file will not refresh
#                                                               interlist: duplicates
#                                                               cmd interface: remove keys: lib vendor temp list log
#                                                               oracle show progress
#                                                               import show progress
#                                                               change sequence of the end output
#                                                               end report: add split files (+222)
#                                                               progress_bar(): exit at esc
#                                                               implement reserving backup copy of list and vendor files
#                                                               remove "total" from all reports
#                                                               replace end report by from the vendor file
#                                                               implement that if origin or backup is missed then no msg
#                                                               io: add file operations absolut protection for writing deleting outside from import folder
#                                                               to go: replace currnumber by estimated number of files
#                                                               add 1/5 counting inside progress_bar (uchitivaja oracle)
#                                                               number of qbit 15:16 files is +1 higher than real
#                                                               DELFILE numbering
#                                                               implement groupid (if you're importing file from list - if it's split-file to not pass to statistics?)
#                                                               new numbering: 16, 16A, 16B, ...
#                                                               report: add size field
#                                                               v0.95
#                                                               status 0 items shouldn't go to .total
#                                                               total: 123        456; same for 8/16/24/32; and at the last line of qbit paragraph: sumofqbits
#                                                               report:     16                      60              ok16 (red:total)
#                                                               report: add summary of qbit : items
#
# replace warning by own's func     <-- wtf ???
# while reading vendor file Pack( name - that was been already defined cause error?
# build rule-file for oracle
# implement config-file: important vars; library type-map
# including in report values of important variables?
# dev html(js) report with file lists
# investigate split_group: strong problems with split_group - changes do niot apply to list
#
# add_ignore_path: add feature of ignore path (for blocking same sample-pack in import and vendor folders
#
# cleanup code
#
# MOD (what to do with the old modified items?)
# RESCAN
# black_octopus do not detected?
# SPLITS SPLITGROUP ???
#
# 65120  48000  24 1  0.1    -       2.0   ./Zero-G - Ethera Gold Atlantis/Samples/Legato/CLASSIC/LEG/Atlantis_Leg_Classic_GP12_-19.wav
#       +94.4%
#
# _STATUS - not needed?
#
# add samplepack session time... for each file time is summaried with the sample pack session time
#
#
####################################################
# waveItem v0.96 ###################################
####################################################
#
#
#
#
#
####################################################
####################################################
####################################################

import  os
os.environ[ "PYGAME_HIDE_SUPPORT_PROMPT" ] = "1"

import  sys
import  argparse

import  pygame

import  shutil
import  string
import  subprocess

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

import  con

#conl                = con.conl
conline             = con.conline
stat                = con.stat

import  common

exit                = common.exit
fatal               = common.fatal
warning             = common.warning
getime              = common.getime

import  _
import  oracle
from    wav     import  *
import  report

vendor_match = report.vendor_match


################################################


_PATH                   = 0
_HASH                   = 1
_HISTORY                = 2
_STATUS                 = 3
_TYPE                   = 4
_NAME                   = 5
_SOURCE                 = 6
_RATE                   = 7
_GROUPID                = 8

ATTROFF                 = 0

text.set_default_box_attr( report.ERROR_COLOR )

BLINK_PERIOD            = 0.125
LISTFILE_FIELDS         = 16
ALIEN_MARK              = "?"

SYSTEM_FOLDERNAME       = "_/"
TEMP_FOLDERNAME         = "_TEMP/"
ITEM_FILENAME           = "item"
VENDOR_FILENAME         = "vendor"
LOG_FILENAME            = "log"


PROGRESSBAR_THEME = {
    "READ":         1,
    "IMPORT":       2,
    "GET FILES":    3,
    "WRITE":        4 }







####################################################
# COMMON ###########################################
####################################################

PROGRESS_BAR_ON = 0

def conl( t = "" ):

    global PROGRESS_BAR_ON

    if PROGRESS_BAR_ON:

        progress_bar( "off" )

        con.conl( t )

        progress_bar( "on" )

    else:

        con.conl( t )


############################################

def zonl( t = "" ):

    if _.VENDORPACK_INFO:

        return conl( t )


################################################

def quit():

    conl()
    conl( "QUIT" )

    exit()


################################################

import msvcrt
import time

def iscont( text = "CONTINUE ?" ):

    def draw( text ):

        stat( text )

    #_______________

    def clear( text ):

        stat()
        #print( "\r" + " " * len( text ) + "\r", end = "", flush = True )

    #_______________

    progress_bar()

    text += " (YNQ)"

    visible = True
    last = getime()

    while True:

        if msvcrt.kbhit():

            ch = msvcrt.getch()

            ch = ch.upper()

            if ch == b'\r' or ch == b'Y':

                clear( text )
                return "yes"

            if ch == b'\x1b' or ch == b'N':

                clear( text )
                return "no"

            if ch == b' ' or ch == b'Q':

                clear( text )
                return "quit"

        now = getime()

        if now - last >= BLINK_PERIOD:

            last = now
            visible = not visible

            if visible:

                draw( text )

            else:

                clear( text )

        time.sleep( 0.01 )



################################################

def getkey():

    ch = msvcrt.getwch()

    return ch


################################################

PROGRESS_BAR_TEXT = ""

def progress_bar( t = "", i = 0, q = 0, m = 0 ):

    def clear():

        global  PROGRESS_BAR_ON

        PROGRESS_BAR_ON         = 0

        print( report.RESET_COLOR +
               '\r' +
               ' ' * ( con.WIDTH - 1 ) + '\r',
               end = "",
               flush = True )

    #___________________

    def draw( t = None, a = None, b = None, s = None ):

        global  PROGRESS_BAR_ON, PROGRESS_BAR_TEXT

        PROGRESS_BAR_ON         = 1

        if t is not None:

            t = report.RESET_COLOR +            \
                '\r' +                          \
                ' ' + t + ' ' +                 \
                '\033[47;94m' + ' ' * a +       \
                '\033[104;97m' + ' ' * b +      \
                '\033[0m' + s + '\r'

            PROGRESS_BAR_TEXT = t

        print( PROGRESS_BAR_TEXT, end = '', flush = True )
    #___________________

    def percent( i, q ):

        if q == 0:

            return 100

        return int( i / q * 100 )
    #___________________

    global PROGRESSBAR_THEME

    if t != "":

        if t == "off":

            return clear()

        if t == "on":

            return draw()

        A = PROGRESSBAR_THEME
        if t in A:

            c = A[ t ]
            t = f"{c}/{len( A )} {t}"

        else:

            fatal( f"progressbar: undefined theme: {t}'" )



    if not m:

        if msvcrt.kbhit():

            ch = msvcrt.getch()

            if ch == b'\x1b':

                clear()
                exit()

    if t == "":

        clear()
        PROGRESS_BAR_THEME = ""

        return False

    pc = percent( i, q )
    pc = max( 0, min( 100, int( pc ) ) )

    cw = con.WIDTH - 7 - len( t )
    w = max( 1, cw )

    a = round( w * pc / 100 )
    b = w - a

    s = f'{pc:3d}% '

    draw( t, a, b, s )

    return False



################################################

def getdirs( p ):

    R, err = io_.getdirs( p )
    if err:
        return R, err

    for f in list( R.keys() ):
        if f.startswith( "_" ):
            del R[ f ]

    return R, ""


################################################

def html_report( hf, t ):

    D = {}
    tt, err = io_.rdfile( hf )
    if err:

        tt = ""

    else:

        tt = text.totext( tt )

        if match( tt,  r"<pre [^e]*(`eol)", D ):

            tt = D[ "+1" ]

            if match( tt, r"</pre>", D ):

                tt = D[ "-1" ]

    t = text.ansi_html( t )
    if match( t, r"<pre [^e]*(`eol)", D ):

        t = D[ "-1" ] + D[ "0" ] + tt + D[ "+1" ]

    io_.wrfile( hf, t )




################################################

import msvcrt
import ctypes

user32 = ctypes.windll.user32

VK_SHIFT = 0x10

def check_esc():
    if not msvcrt.kbhit():
        return ""

    ch = msvcrt.getch()

    if ch == b'\x1b':  # ESC
        shift_pressed = user32.GetAsyncKeyState(VK_SHIFT) & 0x8000

        if shift_pressed:
            return "SHIFT+ESC"
        else:
            return "ESC"

    return ""


################################################

def attroff( f, p = False ):

    global ATTROFF

    if not ATTROFF or p:

        io_.attroff( f )

        if not p:

            ATTROFF = True


################################################

def dumpa( A ):

    t = ""
    for i in A:

        v = A[ i ]
        t += ln( f"[ {i} ] = {v}'" )

    return t


################################################


def exp_filename( path, base = None ):

    if path.startswith( "./" ):

        if base is None:

            base = _.IMPORT

        path = base + path[ 2: ]

    return path


















####################################################
# INIT #############################################
####################################################

def waveItem_init( args ):

    global PROGRESSBAR_THEME

    _.EOL = "\x0A"

    s = sys.platform
    if s.startswith( "win" ):

        _.OSTYPE     = "win"
        _.EOL        = "\x0D\x0A"

    elif s == "darwin":

        _.OSTYPE     = "mac"

    elif s.startswith( "linux" ):

        _.OSTYPE = "lnx"

    else:
        fatal( f"unknown os-type: {s}" )

    #_______________________

    _.ATTR = _.DEFAULT_ATTR if args.ATTR is None else int( args.ATTR )

    pos = args.towav + args.rescan + args.norm + args.qbit + args.split + \
          args.leftrim + args.rightrim + args.dup + args.oracle + args.sort

    neg = args._towav + args._rescan + args._norm + args._qbit + args._split + \
          args._leftrim + args._rightrim + args._dup + args._oracle + args._sort

    neg = ~neg

    _.ATTR |= pos
    _.ATTR &= neg

    #_______________________

    def init_folder( val, defval ):

        if not val:
            val = defval

        val = io_.filepath( val + "/" )

        return val

    #_______________________

    def init_pygame():

        pygame.init()

    #_______________________

    _.IMPORT            = init_folder( args.IMPORT, os.getcwd() )

    if not io_.isdir( _.IMPORT ):

        fatal( f"import folder not found: {_.IMPORT}" )

    _.SYSTEM            = _.IMPORT + SYSTEM_FOLDERNAME

    _.BACKUP            = _.SYSTEM
    _.TEMP              = _.SYSTEM + TEMP_FOLDERNAME

    _.LIST              = _.IMPORT + ITEM_FILENAME
    _.VENDOR            = _.IMPORT + VENDOR_FILENAME
    _.LOG               = _.IMPORT + LOG_FILENAME

    io_.add_absprotpath( _.IMPORT )

    io_.defdir( _.SYSTEM )

    #_______________

    if _.ATTR & _.MASK_ATTR_ORACLE:

        PROGRESSBAR_THEME[ "ORACLE" ]   = 4
        PROGRESSBAR_THEME[ "WRITE" ]    = 5

    #_______________

    debug_args( args )

    waveitem_checkbackup()

    if args.help:

        conl( report.help() )
        exit()

    if args.version:

        exit()

    #___________________

    io_.defdir( _.TEMP )

    init_pygame()

    conl( report.begin() )


################################################

def debug_args( args ):

    part = "norm"

    if args.small:
        part = "small"

    if args.normal:
        part = "norm"

    if args.full:
        part = "full"

    if args.real:
        part = "real"

    base = "c:/WAVLIB/"

    dst = _.IMPORT

    p = f"{base}{part}/"

    if args.ca:

        src = f"{p}a/"

        if True:

            attroff( dst, 1 )

            err = io_.clonedir( dst, src )
            if err:
                conl( f"CLONE ERROR: {err}" )
                exit()

    elif args.cb:

        src = f"{p}b/"

        r = iscont( f"copy {src} to import folder {dst} ? " )
        if r == "yes":

            err = io_.copydir( dst, src )
            if err:
                conl( f"COPY ERROR: {err}" )
                exit()

        elif r == "quit":

            quit()





####################################################
# VENDOR FILE ######################################
####################################################

def read_vendor( vf = None ):

    def import_folder_in( f ):

        D, err = getdirs( f )
        if err:
            fatal( f"import_dirin( {f}: {err} )" )

        Z = {}
        for n in list( D.keys() ):

            if n in D:

                #conl( f"import folder: {n} at {D[ n ]}'" )


                vp, fl = vendor_match( n )
                if fl == 2:

                    zonl( f"vendor folder found: {n}'" )

                    if vp not in Z:
                        Z[ vp ] = {}

                    #F = io_.getfiles( D[ n ], r"(?i)\.wav$", 1 )
                    #if len( F ):
                    #
                    #   Z[ vp ][ D[ n ] ] = "_"

                    E, err = getdirs( D[ n ] )
                    if err:
                        fatal( f"import_folder_in( {f}: {D[ n ]}: {err}" )

                    del D[ n ]

                    for vn in E:

                        if vn in D:
                            add_ignore_path( D[ vn ] )
                            del D[ vn ]

                        zonl( f"vendor's {n} sample pack: {vn} found" )

                        Z[ vp ][ E[ vn ] ] = vn

        for n in D:
            
            report.def_pack( n, D[ n ] )

        conl()

        return Z

    #_______________________

    def reassign_packs( rp = None ):

        if rp is None:
            rp = _.REPORTPTR

        for vp in rp.vendors:

            zonl( f"reassign: check vendor: {vp.name}" )

            for pp in list( vp.packs.keys() ):

                zonl( f"reassign: check pack: {pp.name}" )

                n = pp.name

                nvp, f = vendor_match( n )
             
                if nvp != vp:

                    zonl( f"reassigning pack to new vendor from {vp.name} to {nvp.name}'" )

                    del vp.packs[ pp ]

                    nvp.packs[ pp ] = 1
                
                    pp.vendor = nvp

    #_______________________

    def get_start_param( t ):

        A = {}        
        if match( t, r"DATE		+(`date	[^ ]+)		+(`time	[^ ]+)		+(`session	[^ ]+)", A ):

            s = A[ "session" ]
            s = text.unformatime( s )
            _.TIMECNT = s

        t = gsub( t, r"(?s)PACKS.*$" )
        t = gsub( t, r"(?s)^.*(PROC)", r"\1" )

        lines = t.splitlines()

        for line in lines:

            if match( line, r"(`name	[0-9:A-Z]+)[ ]+(`val	[^e]*)$", A  ):

                n = A[ "name" ]
                v = A[ "val" ]

                n = n.upper()

                match( v, r"(`val	[0-9]+)([(/+ ]*(`val2	[0-9]+))?", A )                    

                v = int( A[ "val" ] )
                v2 = 0
                if "val2" in A:
                    v2 = int( A[ "val2" ] )

                if n == "SPLIT":

                    _.FILES[ n ]            = v
                    _.SPLITCNT              = v2

                elif n == "TRIM":

                    _.FILES[ "LEFTRIM" ]   = v
                    _.FILES[ "RIGHTRIM" ]   = v2

                elif ":" in n:
                    _.FILES[ "QBIT" ] += v

                else:
                    _.FILES[ n ] = v

        report.INDEX_OFFSET = _.FILES[ "PROC" ]

    #_______________________

    if vf is None:
        vf = _.VENDOR

    t, err = io_.rdfile( vf )
    if err:

        t = ""

    t = text.totext( t )

    get_start_param( t )

    rp = report.Report()

    _.REPORTPTR = rp

    vp = report.Vendor( "_" )
    pp = report.Pack( "_" )

    pp.vendor = vp
    vp.packs[ pp ] = 1
    rp.vendors[ vp ] = 1

    _.USERPACK = pp
    _.USERVENDOR = vp 

    rp.load( t )

    #_______________________

    VP = import_folder_in( _.IMPORT )

    reassign_packs( rp )

    for vp in VP:

        for path in VP[ vp ]:

            report.def_pack( VP[ vp ][ path ], path, vp )

    zonl()


################################################

def write_vendor( vf = None, rp = None ):

    if vf is None:

        vf = _.VENDOR

    if rp is None:

        rp = _.REPORTPTR

    t = rp.report()

    tt = text.csioff( t )
    err = io_.wrfile( vf, tt )
    if err:
        conl( f"write_vendor( {vf}: write vendor-file error: {err}" )

    tt = text.ansi_html( t )
    hf = vf + ".html"
    err = io_.wrfile( hf, tt )
    if err:
        conl( f"write_vendor( {hf}: write html vendor-file error: {err}" )


####################################################
# LIST FILE ########################################
####################################################

def read_list( path, importflag ):

    zonl( f"reading item-file: {path}" )
    zonl()

    files = []
    FF = {}

    if path is None:
        return files, ""

    txt, err = io_.rdfile( path )
    if err:
        txt = ""

    txt = text.totext( txt )

    #___________________

    A = {}
    if match( txt, r"^\x09(`dir	[^e]+)", A ):
        pi = A[ "dir" ]
        txt = A[ "+1" ]
    else:
        pi = ""
    #___________________

    lines = txt.splitlines()

    pp = io_.fpath( path )
    ppp = io_.FPATH( pp )

    i = 0
    c = 1
    cq = len( lines )
    ch = int( cq / 200 )

    for line in lines:

        i += 1
        c -= 1
        if c == 0:

            c = ch

            progress_bar( "READ", i, cq )

        line = line.rstrip( "\n" )
        F = line.split( "\t" )

        p = F[ _PATH ]

        if p != "":

            p = exp_filename( p, pp if pi == "" else pi )
            p = io_.filepath( p )

            ff = io_.FILEPATH( p )

            #conl( f"zho: {ff}          {ppp}" )


            if not ff.startswith( ppp ):

                # if file is outside from item-file's folder then its will be skipped

                conl( f"away file: {p}" )
                continue


            if ff in FF:

                _.LISTDUP_CNT += 1
                conl( f"LIST FILE DUPLICATE({_.LISTDUP_CNT}): {p}" )

                continue

            FF[ ff ] = 1

            file = list( F )

            file[ _PATH ] = p
            file[ _SOURCE ] = importflag

            if len( file ) < LISTFILE_FIELDS:
                file.extend( [ "" ] * ( LISTFILE_FIELDS - len( file ) ) )

            files.append( file )

    progress_bar()

    return files, ""


################################################

def write_list( path, items ):

    lines = []

    i = 0
    c = 1
    ch = 400
    cq = len( items )
    ch = int( cq / 200 )

    for item in items:

        i += 1
        c -= 1
        if c == 0:

            c = ch

            progress_bar( "WRITE", i, cq, 1 )

        f = item.filepath

        if f == "":
            continue

        t = write_list_item( item )
        lines.append( t )

    txt = ln( f"\x09{_.IMPORT}" ) + _.EOL.join( lines )

    data = io_.todata( txt )

    r = io_.wrfile( path, data )

    progress_bar()

    return r

#___________________________

def write_list_item( item, F = None ):

    if F is None:
        F = [""] * LISTFILE_FIELDS

    p = item.filepath
    F[ _PATH ]      = io_.filepath( p, _.IMPORT )
    F[ _GROUPID ]   = item.groupid
    F[ _HASH ]      = item.hash
    F[ _STATUS ]    = str( item.libstatus )
    F[ _HISTORY ]   = item.history
    F[ _SOURCE ]    = str( item.importflag )
    F[ _RATE ]      = str( item.rating )

    tp = item.libtype

    F[ _TYPE ]      = tp
    F[ _NAME ]      = item.libname

    return "\t".join( F )


####################################################
# ITEMS ############################################
####################################################

def unfold_items( path, new, old ):

    # returns:
    #
    #   newitems, olditems = unfold_items( "path"
    #___________________

    def unfold_list( f, items, c = 0 ):

        fp = io_.FPATH( f )

        for item in items[:]:

            ff = io_.FILEPATH( item.filepath )

            if ff.startswith( fp ):

                if ff in _.OLDITEMS:

                    ptr = _.OLDITEMS[ ff ]

                    #pp = get_file_pack( ptr )
                    #pp.total -= 1
                    #pp.count( ptr.history, -1 )

                c += 1

                if ff in _.OLDITEMS:
                    del _.OLDITEMS[ ff ] 
                elif ff in _.NEWITEMS:
                    del _.NEWITEMS[ ff ] 
                else:
                    conl( f"BEZHOZ: {ff}" )



                zonl( f"UNFOLD FILE: {item.filepath}" )

                items.remove( item )

        return items, c
    #_______________

    path = io_.fpath( path )

    old, co = unfold_list( path, old )
    new, cn = unfold_list( path, new )

    return new, old














################################################

def import_list( path, newitems, olditems, importflag = "" ):

    if importflag == "":

        progress_bar()

    zonl( f"importing item-file: {path} ..." )
    zonl()

    files, err = read_list( path, importflag )
    if err == "":

        if importflag != "":

            newitems, olditems = unfold_items( path, newitems, olditems )

        i = 0
        c = 1
        cq = len( files )
        ch = int( cq / 200 )

        for F in files:

            i += 1
            c -= 1
            if c == 0:

                c = ch

                progress_bar( "IMPORT", i, cq )

            f = io_.filepath( F[ _PATH ] )
            ff = io_.FILEPATH( f )

            item = WaveItem()
            item.filepath       = f

            #_______________

            s = F[ _STATUS ]
            s = 1 if s == "" else int( s )
            if s == 0:

                if item.importflag != "":

                    continue

                _.ZEROSTAT[ ff ] = 1

            item.libstatus = s

            #_______________

            item.rating         = float( F[ _RATE ] )
            item.history        = F[ _HISTORY ]
            item.libtype        = F[ _TYPE ]
            item.libname        = F[ _NAME ]
            item.importflag     = F[ _SOURCE ]
            item.groupid        = F[ _GROUPID ]

            h = F[ _HASH ]

            if h == "":

                if item.importflag == "":

                    newitems.append( item )
                    _.NEWITEMS[ ff ] = item

                continue
            #___________

            if _.ATTR & _.MASK_ATTR_RESCAN:

                hr = io_.hashfile( f )

                if h != hr:
                    h = hr
                    conl( f"LIST FILE MODIFIED: {f}" )

            #___________

            item.hash = h

            if ff in _.OLDITEMS:

                _.SAMECNT += 1
                conl( f"SAME ({_.SAMECNT}): {f}'" )
                continue

            _.OLDITEMS[ ff ] = item

            _.FILEHASH[ ff ] = h
            _.HASHFILE[ h ] = f

            olditems.append( item )

    progress_bar()

    return newitems, olditems

#_______________________

GETFILES_CNT            = 0

def getfiles( f, newitems, olditems, importflag = "" ):

    global GETFILES_CNT

    f = io_.filepath( f ) + "/"

    cq = len( olditems ) + len( newitems )

    if importflag == "":

        GETFILES_CNT = 0

    else:

        progress_bar( "GET FILES", GETFILES_CNT, cq )
        lf = f + ITEM_FILENAME
        if io_.isfile( lf ):

            newitems, olditems = import_list( lf, newitems, olditems, ALIEN_MARK )

            if importflag:

                return newitems, olditems

    folder = os.path.abspath( f )

    folders = []
    local_files = []

    for item in os.scandir( folder ):
        name = item.name
        if name.startswith( "_" ):

            continue

        if item.is_dir():
            folders.append( str( item.path ) )
        elif item.is_file():
            local_files.append( str( item.path ) )

    for f in folders:

        newitems, olditems = getfiles( f, newitems, olditems, ALIEN_MARK )

    for f in local_files:

        f = io_.filepath( f )

        n = io_.filename( f )
        if match( n, r"(?i)\.wav$" ):

            GETFILES_CNT += 1

            ff = io_.FILEPATH( f )

            if ff in _.OLDITEMS:

                continue

            if ff in _.NEWITEMS:

                continue

            _.NEWITEMS[ ff ] = 1

            item = WaveItem()
            item.filepath = f

            newitems.append( item )

    return newitems, olditems











####################################################
# ORACLE ###########################################
####################################################

def _oracle( items ):

    q = len( items )
    q -= len( _.ZEROSTAT )

    if q > 0:

        i = 0
        c = 1
        cq = len( items )
        ch = int( cq / 200 )

        for item in items:

            i += 1
            c -= 1
            if c == 0:

                c = ch
                progress_bar( "ORACLE", i, cq )

            _oracle_item( item )

        progress_bar()

        conline( f"ORACLE ({q})" )
        conl( oracle.report() )
        conl()

    stat()
        
#___________________________

def _oracle_item( item ):

    f = item.filepath
    n = io_.filenam( f )
    p = trim_filepath( io_.fpath( f ) )

    pp = get_file_pack( f )
    r = r"(?i)" + report.toregex( pp.name )

    #conl( f"FROM: {p}'" )

    pn = p + n

    pnc = gsub( p, r )

    #conl( f"TO:   {p}'" )

    oracle.oracle( item, f, pn, pnc, n )

    return 





 





####################################################
# TOWAV ############################################
####################################################

def towav( args, olditems ):

    # returns:
    #
    #   ""      in case if towav op completed
    #   true in case if towav op is breaked
    #___________________________

    if not _.ATTR & _.MASK_ATTR_TOWAV:
        return None

    files, err = io_.getfiles( _.IMPORT, _.MULTIMEDIA_EXT )
    if err:
        fatal( f"TOWAV  import folder access err: {err}" )
        return 
        
    if not files:
        return

    _.FILES[ "TOWAV" ] = files

    #_______________


    items = []
    c = 0
    for F in _.FILES[ "TOWAV" ]:

        c += 1

        f = F[ _PATH ]
        ff = io_.FILEPATH( f )

        if ff in _.ZEROSTAT:

            continue

        ptr             = WaveItem()
        ptr.index       = c
        ptr.filepath    = f

        items.append( ptr )

    #_______________

    q = len( items )

    if q == 0:
        return

    _.TOTAL = q

    attroff( _.IMPORT )

    f = args.answer
    if f is None:

        f = iscont( f"CONVERT NON.WAV-FILES ({q}) ?" )
        if f == "quit":

            quit()

        f = True if f == "yes" else False

    if not f:
        return
 
    conline( f"toWAV ({q})" )

    #_____________________

    _.STARTIME = getime()

    idx = 0
    r = ""

    while True:

        key = check_esc()
        if key == "ESC":
            r = key
            break

        _.TOWAV = ""

        if idx >= q:

            break

        item = items[ idx ]

        f = item.filepath

        #ff = io_.FILEPATH( f )
        #if ff not in _.ZEROSTAT:

        towav_item( items, idx, item, f, olditems )

        idx += 1

    stat()

    return r





DEBUG_POINT             = 0
DEBUG_POINT_CNT         = 0

def debug_point( t ):

    global DEBUG_POINT, DEBUG_POINT_CNT

    if not isinstance( t, str ):

        t = str( t )

    tm = DEBUG_POINT
    DEBUG_POINT = getime()

    tm = DEBUG_POINT - tm

    c = DEBUG_POINT_CNT

    DEBUG_POINT_CNT += 1

    conl( f"{t} : DBG POINT({c}): {tm}" )
















####################################################
# WAVITEM ##########################################
####################################################





def waveItem( args ):

    def count_lists( new, old ):

        def count_list( items, b = None ):

            if items is None:

                return

            for item in items:

                f = item.filepath
                g = item.groupid
                g = 0 if g == "" else int( g )
                h = item.history
                s = item.libstatus

                if s == 0:

                    continue

                pp = get_file_pack( f )

                if g < 0:

                    pp.splitcnt += 1

                else:

                    pp.total += 1
                    pp.count( h )

            return items

        #_______________

        old = count_list( old )
        new = count_list( new )

        return new, old

    #_______________________

    _.SESSION_START = getime()

    read_vendor()

    idx = 0
    wf = True

    a = report.INDEX_OFFSET
    report.INDEX_OFFSET = 0

    #___________________

    newitems, olditems = import_list( _.LIST, [], [] )

    r = towav( args, olditems )
    if r:
        return

    report.INDEX_OFFSET = a

    progress_bar()

    newitems, olditems = getfiles( _.IMPORT, newitems, olditems )
    newitems, olditems = count_lists( newitems, olditems )

    progress_bar()

    #___________________

    _.STARTIME = getime()

    r = _.MASK_ATTR_NORM + _.MASK_ATTR_SPLIT + _.MASK_ATTR_LEFTRIM + _.MASK_ATTR_RIGHTRIM + _.MASK_ATTR_DUP
    if _.ATTR & r:

        _.LOGSTR.clear()

        if len( newitems ):

            conline( "waveItem" )

            attroff( _.IMPORT )

            #___________

            c = report.INDEX_OFFSET
            for ptr in newitems:

                c += 1
                ptr.index = str( c )

            _.TOTAL = c

            #___________

            while True:

                r = waveItem_item( newitems, idx )
                if r is None:
                    break

                key = check_esc()
                if key == "ESC" or _.FORCEXIT:

                    report.EXITING = "EXITING (SAVE) ..."

                elif key == "SHIFT+ESC":

                    report.EXITING = "EXITING (NO SAVE) ..."
                    wf = False

                if report.EXITING and _.GLOBAL_TAB_CNTR == 0:
                    break

                idx += 1

    #___________________

    stat()

    t = ""
    q = len( _.LOGSTR )
    if q:

        i = 0
        t = ""
        while i < q:

            t += _.LOGSTR[ str( i ) ]
            i += 1


    _.LOGREPORT = t

    olditems += newitems

    if wf:

        if _.ATTR & _.MASK_ATTR_ORACLE:

            _oracle( olditems )

        if _.ATTR & _.MASK_ATTR_SORT:

            wf = wf

        #___________________

        err = write_list( _.LIST, olditems )
        if err:

            err = f"write list error: {err}"
            conl( err )

        err = write_vendor()
        if err:

            err = f"write vendor error: {err}"
            conl( err )

        #___________________

        cleanup_dup()
        #split_group( newitems )

        #_______________________

        err = waveitem_post()
        if err:

            err = f"waveitem_post error: {err}"
            conl( err )

    t = report.end()

    conl( t )


################################################

def waveItem_item( items, idx ):

    def waveItem_item_box( t, p = None, err = None ):

        if err:
            c = report.ERROR_COLOR
        else:
            c = report.RESET_COLOR

        if _.GLOBAL_TAB_CNTR > 0:

            if p:
                _.GLOBAL_TAB_CNTR -= 1

            t = xoffset( t, 3 )

            if not err:
                c = report.SPLIT_COLOR

        t = c + t

        return t

    #_______________________

    if idx >= len( items ):
        return None

    item = items[ idx ]

    f = item.filepath
    am = item.importflag
    ix = item.index

    sz, err = io_.sizefile( f )

    _.GROUPID = item.groupid

    st = item.libstatus
    if isinstance( st, str ):
        if st == "":
            st = 1
    else:
        st = int( st )

    _.SRCFILE   = f
    _.NORM = _.SPLIT = _.SPLITQ = _.LEFTRIM = _.RIGHTRIM = _.DUP = _.ORACLE = _.ERROR = None
    _.QBIT = err = ""

    while True:

        item, err = WaveItem.get( f )

        item.rating = calc_item_price( item )
        item.index = ix

        t = report.report_item( item )
        t = waveItem_item_box( t, None, err )
        conl( t )

        vol = item.vol        
        item0 = item

        if err:
            err = f"WaveItem.get1: {err}"
            break

        regop( str( item.bit ) )

        report.status( items, idx )

        item, err = normalize( item )
        if err:
            err = f"NORM: {err}"
            break

        err = qbit( item, vol )
        if err:
            err = f"QBIT: {err}"
            break

        item0.qbit = item.qbit

        err = split( item, item0, items, idx )
        if err:
            err = f"SPLIT: {err}"
            break

        if err is None:

            item, err = leftrim( item )
            if err:
                err = f"LEFTRIM: {err}"
                break

            item, err = rightrim( item )
            if err:
                err = f"RIGHTRIM: {err}"
                break

        #___________________

        if item0.filepath != item.filepath:

            err = io_.movfile( item0.filepath, item.filepath )
            if err:
                err = f"MOVFILE: {err}"
                break

        item, err = WaveItem.get( item0.filepath )
        if err:
            err = f"WaveItem.get2: {err}"
            break

        item.qbit = item0.qbit
        item.rating = calc_item_price( item )

        break

    #___________________

    # ????if not err??????

    item.importflag     = am
    item.size           = sz
    item.index          = ix

    item.groupid        = _.GROUPID

    _.GROUPID = 0

    item.hash, e = io_.hashfile( item.filepath )
    if e:

        if not err:

            err = f"gethash: {e}"

    else:

        r = dup( item )
        if r is not None:

            if r == 0:

                _.FILEHASH[ item.filepath ]   = item.hash
                _.HASHFILE[ item.hash ]       = item.filepath

            elif r == 1:

                regop( "dup" )

    items[ idx ] = item

    item.libstatus = st

    if err:

        regop( "error" )

        _.ERROR = err

    else:

        regop( "ok" )
        regop( "size", sz )

    regop( "proc" )

    item.history = regop()

    pp = get_file_pack( f )

    if _.GLOBAL_TAB_CNTR > 0:
        pp.splitcnt += 1
        _.SPLITCNT += 1
    else:
        pp.count( item.history )

    t = report.item_result()
    t = waveItem_item_box( t, 1 )
    conl( t )

    #_ QBIT AUTOTEST _______

    if _.QBITAUTOTEST:
        qbit_autotest_report( _.LASTITEMREPORT )

    #_______________________

    if _.GLOBAL_TAB_VAL:

        _.GLOBAL_TAB_CNTR = _.GLOBAL_TAB_VAL
        _.GLOBAL_TAB_VAL = 0

    return 1


################################################

def waveitem_checkbackup():

    def check_backupfiles( fr, fb, n, f ):

        t, err = io_.rdfile( fr )
        if err:

            return None

        t0, err = io_.rdfile( fb )
        if err:

            return None

        if t != t0:

            # file is corrupted

            r = iscont( f"{n} FILE CORRUPTED. REPAIR ?" )
            if r == "quit":

                quit()

            if r == "yes":

                err = io_.copyfile( _.LIST, _.BACKUP + f )
                if err:

                    err = f"{err}"

    #___________________

    f = _.LIST
    f0 = _.BACKUP + ITEM_FILENAME

    r = check_backupfiles( f, f0, "ITEM", ITEM_FILENAME )

    #_______________

    v = _.VENDOR
    v0 = _.BACKUP + VENDOR_FILENAME

    r = check_backupfiles( v, v0, "VENDOR", VENDOR_FILENAME )


################################################

def waveitem_post():

    err = io_.copyfile( _.BACKUP + ITEM_FILENAME, _.LIST )
    if err:

        err = f"copy backup list error: {err}"
        return err

    err = io_.copyfile( _.BACKUP + VENDOR_FILENAME, _.VENDOR )
    if err:

        err = f"write backup vendor error: {err}"
        return err

    t = _.LOGREPORT

    hf = _.LIST + ".html"
    html_report( hf, t )






def draw_list( lst, L ):

    t = ln( lst + ":" ) + ln()

    for f in L:

        t += ln( "    " + f )

    t += ln()

    return t



def draw_dbg():

    _.FILELIST[ "NORM" ].append( "huj" )

    t = ""
    for l in _.FILELIST:

        t += draw_list( l, _.FILELIST[ l ] )

    conl( t )





















####################################################
# MAIN #############################################
####################################################

def main():

    #generate_qbit_files( r"C:\WAVLIB\small\a\SINE\sine" )
    #exit()

    parser = argparse.ArgumentParser( add_help = False )

    parser.add_argument( "--help",      action = "store_true" )
    parser.add_argument( "--version",   action = "store_true" )

    parser.add_argument( "--import",    dest = "IMPORT" )

    parser.add_argument( "--attr",      dest = "ATTR",      type = int )

    parser.add_argument( "--rescan",    dest = "rescan",    action = "store_const", const = _.MASK_ATTR_RESCAN )
    parser.add_argument( "-rescan",     dest = "_rescan",   action = "store_const", const = _.MASK_ATTR_RESCAN )

    parser.add_argument( "--towav",     dest = "towav",     action = "store_const", const = _.MASK_ATTR_TOWAV )
    parser.add_argument( "-towav",      dest = "_towav",    action = "store_const", const = _.MASK_ATTR_TOWAV )

    parser.add_argument( "--norm",      dest = "norm",      action = "store_const", const = _.MASK_ATTR_NORM)
    parser.add_argument( "-norm",       dest = "_norm",     action = "store_const", const = _.MASK_ATTR_NORM )

    parser.add_argument( "--qbit",      dest = "qbit",      action = "store_const", const = _.MASK_ATTR_QBIT  )
    parser.add_argument( "-qbit",       dest = "_qbit",     action = "store_const", const = _.MASK_ATTR_QBIT  )

    parser.add_argument( "--split",     dest = "split",     action = "store_const", const = _.MASK_ATTR_SPLIT )
    parser.add_argument( "-split",      dest = "_split",    action = "store_const", const = _.MASK_ATTR_SPLIT )

    parser.add_argument( "--leftrim",   dest = "leftrim",   action = "store_const", const = _.MASK_ATTR_LEFTRIM )
    parser.add_argument( "-leftrim",    dest = "_leftrim",  action = "store_const", const = _.MASK_ATTR_LEFTRIM )

    parser.add_argument( "--rightrim",  dest = "rightrim",  action = "store_const", const = _.MASK_ATTR_RIGHTRIM )
    parser.add_argument( "-rightrim",   dest = "_rightrim", action = "store_const", const = _.MASK_ATTR_RIGHTRIM )

    parser.add_argument( "--dup",       dest = "dup",       action = "store_const", const = _.MASK_ATTR_DUP )
    parser.add_argument( "-dup",        dest = "_dup",      action = "store_const", const = _.MASK_ATTR_DUP )

    parser.add_argument( "--oracle",    dest = "oracle",    action = "store_const", const = _.MASK_ATTR_ORACLE )
    parser.add_argument( "-oracle",     dest = "_oracle",   action = "store_const", const = _.MASK_ATTR_ORACLE )

    parser.add_argument( "--sort",      dest = "sort",      action = "store_const", const = _.MASK_ATTR_SORT )
    parser.add_argument( "-sort",       dest = "_sort",     action = "store_const", const = _.MASK_ATTR_SORT )

    parser.set_defaults(

        towav       = 0,
        rescan      = 0,
        norm        = 0,
        qbit        = 0,
        split       = 0,
        leftrim     = 0,
        rightrim    = 0,
        dup         = 0,
        oracle      = 0,
        sort        = 0,

        _towav      = 0,
        _rescan     = 0,
        _norm       = 0,
        _qbit       = 0,
        _split      = 0,
        _leftrim    = 0,
        _rightrim   = 0,
        _dup        = 0,
        _oracle     = 0,
        _sort       = 0 )

    parser.add_argument( "--yes",       dest = "answer",    action = "store_const", const = True )
    parser.add_argument( "-yes",        dest = "answer",    action = "store_const", const = False )
    parser.add_argument( "--no",        dest = "answer",    action = "store_const", const = False )
    parser.add_argument( "-no",         dest = "answer",    action = "store_const", const = True )

    #_ DEBUG _______

    parser.add_argument( "--ca",        action = "store_true" )
    parser.add_argument( "--cb",        action = "store_true" )
    parser.add_argument( "--real",      action = "store_true" )
    parser.add_argument( "--small",     action = "store_true" )
    parser.add_argument( "--normal",    action = "store_true" )
    parser.add_argument( "--full",      action = "store_true" )

    #_______________________

    args = parser.parse_args()

    conl( report.title() )

    waveItem_init( args )

    waveItem( args )

    draw_dbg()


####################################################
####################################################
####################################################

if __name__ == "__main__":
    main()




















