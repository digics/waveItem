    # ffmpeg_split should add it's name to the error msg
    # same for getwav; getwav: 2 pframeters
    # same for movfile



########################################################
# WAV v0.1 #############################################
########################################################
#
#
#
#
#
########################################################
########################################################
########################################################



import  subprocess
import  json
import  re
import  warnings
import  traceback

import  numpy       as np
import  soundfile   as sf
from    scipy.io    import  wavfile
from    math        import  gcd, log2
from    functools   import  reduce


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

from    report  import  *

####################################################

FFMPEG_BIN           = r"E:/DRIVE/CPU/DEV/BIN/FFMPEG/"
FFMPEG               = FFMPEG_BIN + "ffmpeg"

####################################################

CODEC_BIT = {

    "pcm_s8":       8,
    "pcm_u8":       8,

    "pcm_s16le":    16,
    "pcm_s16be":    16,
    "pcm_u16le":    16,
    "pcm_u16be":    16,

    "pcm_s24le":    24,
    "pcm_s24be":    24,
    "pcm_u24le":    24,
    "pcm_u24be":    24,

    "pcm_s32le":    32,
    "pcm_s32be":    32,
    "pcm_u32le":    32,
    "pcm_u32be":    32,

    "pcm_f32le":    32,
    "pcm_f32be":    32,

    "pcm_f64le":    64,
    "pcm_f64be":    64 }

CODEC_TYPE = {

    "pcm_s8":       "i8",
    "pcm_u8":       "i8",

    "pcm_s16le":    "i16",
    "pcm_s16be":    "i16",
    "pcm_u16le":    "i16",
    "pcm_u16be":    "i16",

    "pcm_s24le":    "i24",
    "pcm_s24be":    "i24",
    "pcm_u24le":    "i24",
    "pcm_u24be":    "i24",

    "pcm_s32le":    "i32",
    "pcm_s32be":    "i32",
    "pcm_u32le":    "i32",
    "pcm_u32be":    "i32",

    "pcm_f32le":    "f32",
    "pcm_f32be":    "f32",

    "pcm_f64le":    "f64",
    "pcm_f64be":    "f64" }

NUMCODEC = {

    "16":           "pcm_s16le",
    "24":           "pcm_s24le",
    "32":           "pcm_s32le" }

################################################

def ffmpeg_convert( dst, src, codec = 24 ):

    # codec examples:
    #   pcm_u8, pcm_s16le, pcm_s24le, pcm_s32le
    #   pcm_f32le, pcm_f64le
    #___________________________

    if isinstance( codec, int ):
        codec = str( codec )

    if codec in NUMCODEC:
        codec = NUMCODEC[ codec ]

    cmd = [
        FFMPEG,
        "-hide_banner",
        "-loglevel", "error",
        "-i", src,
        "-c:a", codec,
        "-y",
        dst ]

    try:
        p = subprocess.run(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            encoding = "utf-8",
            errors = "replace" )

    except Exception as e:

        return str( e )

    if p.returncode != 0:

        return p.stderr

    return ""


####################################################
# class WaveItem ###################################
####################################################

class WaveItem:

    def __init__( self ):

        self.index          = 0
        self.filepath       = ""
        self.size           = 0
        self.groupid        = ""
        self.rate           = 0
        self.type           = ""
        self.channels       = 0
        self.time           = 0.0
        self.peak           = 0
        self.vol            = 0
        self.prevol         = 0

        self.bit            = 0
 
        self.hash           = ""
        self.silences       = []


        self.libtype        = ""
        self.libname        = ""
        self.libstatus      = ""

        self.history        = ""

        self.rating          = 0

        self.qbit           = self.bit

        self.importflag     = ""

    ####################################

    def copy( srcitem, dstitem ):

        dstitem.index       = srcitem.index
        dstitem.filepath    = srcitem.filepath
        dstitem.size        = srcitem.size
        dstitem.groupid     = srcitem.groupid
        dstitem.rate        = srcitem.rate
        dstitem.type        = srcitem.type
        dstitem.channels    = srcitem.channels
        dstitem.time        = srcitem.time
        dstitem.peak        = srcitem.peak
        dstitem.vol         = srcitem.vol
        dstitem.prevol      = srcitem.prevol
        dstitem.bit         = srcitem.bit

        dstitem.hash        = srcitem.hash
        dstitem.silences    = srcitem.silences
        dstitem.libtype     = srcitem.libtype
        dstitem.libstatus   = srcitem.libstatus
        dstitem.libname     = srcitem.libname
        dstitem.history     = srcitem.history
        dstitem.rating      = srcitem.rating
        dstitem.qbit        = srcitem.qbit

        dstitem.importflag  = srcitem.importflag


    ####################################

    @classmethod
    def get( cls, path ):

        def get_0( item, path ):

            cmd = [
                FFMPEG,
                "-hide_banner",
                "-i", path,
                "-af", f"astats,silencedetect=noise={_.MIN_SILENCE_LEVEL}dB:d={_.MIN_SILENCE_PERIOD},volumedetect",
                "-f", "null",
                "-" ]

            try:
                p = subprocess.run(
                    cmd,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    text = True,
                    encoding = "utf-8",
                    errors = "replace" )

            except Exception as e:

                return item, str( e )

            if p.returncode != 0:

                return item, p.stderr

            D = {}
            silence_start = None

            line = ( p.stdout or "" ) + ( p.stderr or "" )

            if match( line, r"Stream #\d+:\d+[^:]*:\s*Audio:\s*([^ ,]+)[^,]*,\s*(\d+)\s*Hz,\s*([^,]+)", D ):

                item.codec              = D[ "1" ].strip()
                item.rate               = int( D[ "2" ] )
                ch                      = D[ "3" ].lower()

                if "mono" in ch:
                    item.channels       = 1
                elif "stereo" in ch:
                    item.channels       = 2
                else:
                    try:
                        item.channels = int( ch )
                    except:
                        item.channels   = 0

                codec = item.codec.lower()

                if codec not in CODEC_BIT:

                    dst = _.TEMP + "convert.wav"
                    err = ffmpeg_convert( dst, path, 24 )
                    if err:

                        return item, err

                    err = io_.movfile( path, dst )
                    if err:

                        return item, err

                    return get_0( item, path )

                item.bit = CODEC_BIT[ codec ]
                item.qbit = item.bit
                item.type = CODEC_TYPE[ codec ]

            if match( line, r"Duration:\s*(\d+):(\d+):([0-9.]+)", D ):

                h = int( D[ "1" ] )
                m = int( D[ "2" ] )
                s = float( D[ "3"] )
                item.time       = h * 3600 + m * 60 + s

            if match( line, r"max_volume:\s*([+\-]?[0-9.]+)", D ):

                item.peak       = float( D[ "1" ] )
                item.vol        = db_percent( item.peak )

            if match( line, r"mean_volume:\s*([+\-]?[0-9.]+)", D ):

                item.rms        = float( D[ "1" ] )

            if match( line, r"(?s)^.*n_samples:\s*(\d+)", D ):

                item.samples    = int( D[ "1" ] )

                if item.channels:
                    item.frames = int(item.samples / item.channels)
                else:
                    item.frames = 0

            while line != "":

                if match( line, r"silence_start:\s*([0-9.]+)", D ):

                    line = D[ "+1" ]
                    silence_start = float( D[ "1" ] )
                    if match( line, r"silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)", D ):

                        line = D[ "+1" ]
                        s = silence_start
                        e = float( D[ "1" ] )
                        d = float( D[ "2" ] )
                        item.silences.append( ( s, e, d ) )

                else:

                    break

            return item, ""

        #_______________________

        path = io_.filepath( path )

        item = cls()

        item.filepath       = path
        item.size, err      = io_.sizefile( path )
        item.time           = None
        item.silences       = []
        item.peak           = None
        item.rms            = None
        item.codec          = None
        item.vol            = 0
        item.samples        = 0
        item.frames         = 0
        item.begintrim      = 0
        item.endtrim        = 0
        item.changevol      = None
        item.channels       = 0

        item.hash        = ""

        item.libtype        = ""
        item.libname        = ""
        item.libstatus      = ""

        return get_0( item, path )




    








 
####################################################

_.ITEM_ATTR = ""

def regop( group = "", v = "", file = None ):

    if file is None:
        file = _.SRCFILE
    #_______________

    if group == "":

        a = _.ITEM_ATTR
        _.ITEM_ATTR = ""

        return a

    #_______________

    if not isinstance( v, str ):

        if isinstance( v, float ):

            v = round( v, 4 )

        v = str( v )

    hg = group.upper()

    if hg not in _.FILELIST:

        _.FILELIST[ hg ] = []

    _.FILELIST[ hg ].append( file )

    if ":" in group:

        _.FILES[ "QBIT" ] += 1

    else:

        if hg in _.FILES:

            _.FILES[ hg ] += 1



            

    _.ITEM_ATTR += group + "|" + v + "|"

    return

    pp = get_file_pack( file )

    A = {}
    if match( group, r"^((`bit	\d\d+?)|(`qbit	\d\d?:\d\d?))$", A ):

        if "bit" in A:

            pp.bits[ group ] = pp.bits.get( group, 0 ) + 1

        else:

            pp.qbit[ group ] = pp.qbit.get( group, 0 ) + 1

    elif hasattr( pp, group ):

        setattr( pp, group, getattr( pp, group ) + 1 )

    else:

        print( traceback.print_stack() )
        fatal( f"regop( {group}: unknown group, , {file} )" )


################################################

def db_percent( db ):

    r = ( 10 ** ( db / 20 ) ) * 100
    r = int( r * 10 ) / 10

    return r

################################################

def xonl( t = "" ):

    if _.INTERNAL1_INFO:

        return conl( t )




























####################################################
# TOWAV ############################################
####################################################

CODEC_CONVERT = {
    "pcm_s16be": "pcm_s16le",
    "pcm_s24be": "pcm_s24le",
    "pcm_s32be": "pcm_s32le",
    "pcm_u16be": "pcm_u16le",
    "pcm_u24be": "pcm_u24le",
    "pcm_u32be": "pcm_u32le",
    "pcm_f32be": "pcm_f32le",
    "pcm_f64be": "pcm_f64le",
    }

def ffmpeg_towav( f, c ):

    f = io_.filepath( f )

    if not io_.isfile( f ):
        return f"file not found: {f}"

    df = io_.fpathnam( f ) + ".wav"

    cmd = [FFMPEG, "-y", "-i", f, "-map_metadata", "0", "-vn"]

    if c in CODEC_CONVERT:

        cmd += [ "-c:a", CODEC_CONVERT[c] ]

    cmd.append( df )

    try:

        p = subprocess.run(
                cmd,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text = True,
                encoding = "utf-8",
                errors = "replace",
                check = False )

    except Exception as e:

        err = str( e )
        return err

    if p.returncode != 0:

        err = p.stderr.strip()
        return err

    io_.delfile( f )
    return ""


################################################

def towav_item( items, idx, item, f, olditems ):

    f = io_.filepath( f )

    _.SRCFILE = f

    while True:

        ix = item.index

        status_towav( f, items, idx )

        item, err = WaveItem.get( f )
        item.index = ix

        if err:
            _.TOWAV = err
            item = WaveItem()
            item.filepath = f
            item.index = ix
            break

        c = item.codec
        if c is None:
            c = ""

        err = ffmpeg_towav( f, c )
        if err:
            _.TOWAV = err

        break

    if _.TOWAV != "":

        ptr = WaveItem()
        ptr.filepath = f
        ptr.libstatus = 0
        ptr.hash = "0" * 128
        ptr.index = ix

        olditems.append( ptr )

        _.FILES[ "ERRORTOWAV" ] += 1

    t = report_item( item )
    t = RESET_COLOR + t
    conl( t )
    conl( result_file_towav() )

    return True



























####################################################
# NORM #############################################
####################################################

def normalize( item ):

    # returns:
    #
    #       None        in case if there is no normalize operation performed
    #       ""          in case if normalize operation performed
    #       "str"       in case if error raising while normalize operation performed
    #
    #___________________________
    
    _.NORM = None

    if not _.ATTR & _.MASK_ATTR_NORM:
        return item, None

    if not hasattr( item, "vol" ):
        _.NORM = "#1: can't get volume percent"
        return item, 1

    if item.vol >= _.VOL_OK_LEVEL:
        return item, None

    if not hasattr( item, "peak" ):
        _.NORM = "#2: can't get peak level"
        return item, 1

    vol = -item.peak
    vol -= 0.1

    t = f"volume={vol}dB"

    newitem, err = ffmpeg_trimnorm( item, "_norm", t )
    if err:
        _.NORM = err
        return item, 1

    if not hasattr( newitem, "vol" ):
        _.NORM = "#3: can't get volume percent"
        return item, 1

    p = newitem.vol - item.vol
    newitem.prevol = item.vol

    _.NORM = p
    regop( "norm", p )

    return newitem, ""

#_______________________________

def ffmpeg_trimnorm( item, opname, str ):

    dstfile = _.TEMP + opname + ".wav"

    cmd = [
        FFMPEG,
        "-y",
        "-i", item.filepath,
        "-af" , str,
        "-f", "wav",
        "-c:a", item.codec,
        dstfile
        ]

    try:

        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text = True,
            encoding = "utf-8",
            errors = "replace" )

    except Exception as err:

        err = str( err )
        return item, err

    if p.returncode != 0:

        err = p.stderr
        return item, err

    newitem, err = WaveItem.get( dstfile )
    if err:

        return item, err

    return newitem, ""































####################################################
# QBIT #############################################
####################################################

def qbit( item, vol ):

    def qbit_getbitdepth( data, declared ):

        dtype_bits = data.dtype.itemsize * 8

        if np.issubdtype( data.dtype, np.floating ):
            flat = np.round( data.flatten() * (2 ** (declared - 1)) ).astype( np.int64 )
        else:
            flat = data.flatten().astype( np.int64 )

        if dtype_bits > declared:
            flat = flat >> ( dtype_bits - declared )

        unique = np.unique( flat )

        if len( unique ) < 2:
            return declared

        min_diff = int( np.min( np.diff( unique ) ) )

        if min_diff <= 0:
            return declared

        # count leading zeros from bit (declared-1) down
        # real = number of leading zeros + 1
        leading_zeros = 0
        for bit in range( declared - 1, -1, -1 ):
            if min_diff & ( 1 << bit ):
                break
            leading_zeros += 1

        real = leading_zeros + 1

        if real < 1 or real >= declared:
            return declared

        return real

    #_______________________

    _.QBIT = _.QBIT_SUFFIX = ""

    if not _.ATTR & _.MASK_ATTR_QBIT:
        return

    if _.GLOBAL_TAB_CNTR > 0:
        return

    f = item.filepath
    bit = item.bit

    try:

        with warnings.catch_warnings():

            warnings.simplefilter( "ignore" )
            rate, data = wavfile.read( f )

        r = qbit_getbitdepth( data, bit )
        
        if r < bit:

            ppr = 0
            cm = 50

            while cm != 0 and vol <= cm:
                ppr += 1
                cm /= 2

            r += ppr
            if r < bit:

                item.qbit = r
                _.QBIT = f"{r}:{bit}"

                item.rating = calc_item_price( item )
                _.QBIT_SUFFIX       = item.rating

                regop( _.QBIT, r )

    except Exception as e:

        conl( f"QBITERR: {str(e)}'" )

        _.QBIT = str( e )


############################################

def calc_item_price( item ):

    def bit_depth_factor( b ):

        return round( 2 ** ( b / 8 - 2 ), 3 )

    #___________________________

    def sample_rate_factor( sr ):

        return sr / 48000

    #___________________________

    def status_factor( s ):

        return s + 1

    #_______________________

    bd = bit_depth_factor( item.qbit )
    sr = sample_rate_factor( item.rate )

    r = bd * sr

    r = round( r, 2 )

    return r



























####################################################
# SPLIT ############################################
####################################################

def get_groupid():

    t = int( getime() * 100 )
    t = str( t )

    return t

#___________________________

def split( item, item0, items, idx ):

    # returns:
    #
    #       None        in case if there is no split operation performed
    #       ""          in case if split operation performed
    #       "str"       in case if error raising while split operation performed
    #
    #_______________________

    _.SPLIT = _.SPLITQ = None

    if not _.ATTR & _.MASK_ATTR_SPLIT:
        return None

    if _.GLOBAL_TAB_CNTR > 0:
        return

    #___________________

    ix = item0.index

    pieces = calc_cuts( item0 )

    if not pieces:
        return None

    l = len( pieces )

    if l < 2:
        return None

    q = _.MAX_SPLIT_PIECES
    if l > q:

        _.SPLIT = f"TOO MUCH PIECES: {l} (MAX {q})"
        _.SPLITQ = "CANCEL"

        return None

    _.SPLIT = _.SPLITQ = l

    #_______________________

    g = _.GROUPID
    _.GROUPID = get_groupid()

    newitems = []
    base = io_.fpathnam( item0.filepath )
    outpaths, err = ffmpeg_split( item, item.filepath, pieces, base )
    if err:

        _.SPLIT = err
        _.SPLITQ = "ERROR(1)"
        return 1

    #_______________________

    for outpath in outpaths:

        newitem, err = WaveItem.get( outpath[ 1 ] )
        if err:

            _.SPLIT = err
            _.SPLITQ = "ERROR(2)"

            _.GROUPID = g

            return 1

        if newitem.vol < _.MIN_SPLIT_PIECE_VOL:

            _.SPLIT = f"PIECE VOL IS TOO LOW: {newitem.vol}%"
            _.SPLITQ = "CANCEL"

            _.GROUPID = g

            return None

        #if newitem.time < MIN_SPLIT_PIECE_TIME:

        #    _.SPLIT = f"PIECE TIME IS TOO SHORT: { rountime?newitem.time}"
        #    _.SPLITQ = "CANCEL"
        #    return None

    #_______________________

    err = io_.movfile( outpaths )
    if err:

        _.SPLIT = err
        _.SPLITQ = "ERROR(3)"
        return 1

    #_______________________


    c = 0
    for outpath in outpaths:

        newitem, err = WaveItem.get( outpath[ 0 ] )
        
        newitem.groupid     = str( 0 - int( _.GROUPID ) )

        newitem.index       = ix + chr( 65 + c )
        c += 1

        if err:

            _.SPLIT = err
            _.SPLITQ = "ERROR(4)"
            return 1

        newitems.append( newitem )

    #_______________________

    i = idx + 1

    items[ i:i ] = newitems

    regop( "split", _.SPLITQ )

    _.FILES[ "SPLITS" ].append( item )
    _.FILES[ "SPLITS" ].extend( newitems )

    _.FILES["SPLITGROUP"].append( list( newitems ) )

    _.GLOBAL_TAB_VAL = len( newitems )

    return ""

#_______________________________

def ffmpeg_split( item, path, cuts, base ):

    out_paths = []
    tmp = _.TEMP + "do_split"

    for idx, (a, b) in enumerate(cuts):

        suffix = chr(65 + idx)
        tmp_path = f"{tmp}.{suffix}.wav"
        out_path = f"{base}.{suffix}.wav"

        out_paths.append((out_path, tmp_path))

        a = float(f"{a:.6f}")
        b = float(f"{b:.6f}")

        cmd = [
            FFMPEG,
            "-y",
            "-i", path,
            "-ss", str(a),
            "-to", str(b),
            "-c:a", item.codec,
            tmp_path
        ]

        try:

            p = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text = True,
                encoding = "utf-8",
                errors = "replace" )

        except Exception as e:

            err = str( e )
            return [], err

        if p.returncode != 0:

            err = p.stderr
            return [], err

    return out_paths, ""

#_______________________________

def calc_cuts( item ):

    def merge_short_segments( segments, total, min_len ):

        if not segments:
            return []

        def seg_len( s ):
            return s[ 1 ] - s[ 0 ]

        segments = list( segments )
        n = len( segments )

        long_idxs = [ i for i, s in enumerate( segments ) if seg_len( s ) >= min_len]

        if not long_idxs:
            return [ ( 0, total ) ]

        blocks = { li: [ segments[ li ][ 0 ], segments[ li ][ 1 ] ] for li in long_idxs }

        for i, seg in enumerate( segments ):
            if i in blocks:
                continue

            s_start, s_end = seg

            nearest_li = None
            nearest_dist = float( "inf" )

            for li in long_idxs:

                l_start, l_end = segments[ li ]
                dist = min( abs( s_start - l_end ), abs( s_end - l_start ) )

                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_li = li

            blocks[ nearest_li ][ 0 ] = min( blocks[ nearest_li ][ 0 ], s_start )
            blocks[ nearest_li ][ 1 ] = max( blocks[ nearest_li ][ 1 ], s_end )

        result = list( blocks.values() )
        result.sort( key=lambda x: x[ 0 ] )

        return [ tuple( x ) for x in result ]

    #_______________________

    if not item.silences:
        return []

    total_time = item.time

    # full silence detection
    if len( item.silences ) == 1:

        s, e, d = item.silences[ 0 ]

        if s <= 0.01 or e >= total_time - 0.01:

            return None

    f = item.filepath
    cuts = []

    for s, e, d in item.silences:

        if s <= 0.01:
            continue

        if e >= total_time - 0.01:
            continue

        cuts.append( ( s, e ) )

    if not cuts:
        return []

    pieces = []
    last_end = 0.0

    for s, e in cuts:
        if s > last_end:
            pieces.append( ( last_end, s ) )
        last_end = e

    if last_end < total_time:
        pieces.append( ( last_end, total_time ) )

    pieces = merge_short_segments( pieces, item.time, _.MIN_SPLIT_PIECE_TIME )

    return pieces


################################################

def split_group( items ):

    def split_group_del( f ):

        r = io_.delfile( f )

        xonl( f"DELFILE:     {f}" )

        return r

    #_______________________

    def split_group_ren( sf, df, items ):

        r = io_.renfile( sf, df )

        xonl( f"RENAME FILE: {sf} > {df}" )

        if r:
            return r

        for it in items:

            if it.filepath == sf:
                it.filepath = df
                break

        return r

    #_______________________

    xonl( NORMAL_COLOR )
    xonl( "POST-SPLIT: BEGIN" )
    xonl()

    for group in _.FILES[ "SPLITGROUP" ]:

        alive = []

        for item in group:

            f = io_.filepath( item.filepath )

            if not io_.isfile( f ):
                continue

            alive.append( item )

        if not alive:
            continue

        base = io_.filepath( alive[ 0 ].filepath )

        i = base.rfind(".")
        if i >= 0:
            base = base[:i]

        i = base.rfind(".")
        if i >= 0:
            base = base[:i]

        for idx, item in enumerate(alive):

            f = io_.filepath( item.filepath )

            c = chr( ord( "A" ) + idx )
            nf = io_.filepath( base + "." + c + ".wav")

            if f == nf:
                continue

            if io_.isfile( nf ):
                split_group_del( nf )

            err = split_group_ren( f, nf, items )
            if err:
                xonl(f"split rename error: {err}")
                continue

            item.filepath = nf

    xonl()
    xonl( "POST-SPLIT: END" )













































####################################################
# LEFTRIM ##########################################
####################################################

def leftrim( item ):

    _.LEFTRIM = None

    newitem, err, len = _trim( item, _.MASK_ATTR_LEFTRIM, "leftrim" )
    if err:
        _.LEFTRIM = err
        return item, 1

    l = item.frames - newitem.frames

    if l < _.MIN_LEFTRIM_FRAMES:
        return item, None

    l = l / item.rate

    _.LEFTRIM = -l

    regop( "leftrim", _.LEFTRIM )

    return newitem, ""

#_______________________________

def _trim( item, mask, opname, rv = "" ):

    if not _.ATTR & mask:
        return item, "", 0

    minlen = _.MIN_TRIM_TIME
    tresh = _.TRIM_TRESHOLD
    t = rv + f"silenceremove=start_periods=1:start_silence=0:start_duration={minlen:.6f}:start_threshold={tresh}dB,adelay=1S:all=1," + rv
    t = t.rstrip(",")

    newitem, err = ffmpeg_trimnorm( item, opname, t )
    if err:

        return item, err, 0

    l = newitem.frames - item.frames 

    return newitem, "", l


####################################################
# RIGHTRIM #########################################
####################################################

def rightrim( item ):

    _.RIGHTRIM = None

    newitem, err, len = _trim( item, _.MASK_ATTR_RIGHTRIM, "rightrim", "areverse," )
    if err:
        _.RIGHTRIM = err
        return item, 1

    l = item.frames - newitem.frames

    if l < _.MIN_RIGHTRIM_FRAMES:
        return item, None

    l = l / item.rate

    _.RIGHTRIM = -l

    regop( "rightrim", _.RIGHTRIM )

    return newitem, ""
































####################################################
# DUP ##############################################
####################################################



def isamegroup( a, b ):

    a = io_.FPATHNAM( a )[ :-1 ]
    b = io_.FPATHNAM( b )[ :-1 ]

    r = 0
    if a == b:
        r = 1

    return r














def dup( item ):

    # returns:
    #
    #   None    - in case if no dup operation performed
    #   0       - in case dup ok (no matches)
    #   1       - in case if duplicate found
    #   -1      - in case if duplicate found (same group)
    #___________________________

    _.DUP = None 

    if not _.ATTR & _.MASK_ATTR_DUP:
        return None

    h = item.hash
    f = item.filepath

    if h == "":
        fatal( "nihuja se!" )

    if h in _.HASHFILE:

        df = _.HASHFILE[ h ]

        if df != f:

            _.DUP = trim_filepath( df )
            add_dupfile( f )

            if isamegroup( f, df ):

                pp = get_file_pack( f )
                pp.splitcnt -= 1
                _.SPLITCNT -= 1


                item.filepath = ""

                return -1

            return 1

    else:

        _.HASHFILE[ h ] = f

    return 0

################################################

def add_dupfile( f ):

    f = io_.filepath( f )

    _.DUPFILE[ f ] = 1

################################################


CLEANUP_DUPCNT          = 0

def cleanup_dup():

    def cleanup_dup_del( f, c ):

        r = io_.delfile( f )

        xonl( f"DELFILE({c}):     {f}" )

        return r

    #_______________________

    global CLEANUP_DUPCNT

    xonl()
    xonl( "POST-DUP: BEGIN:" )
    xonl()

    for f in list( _.DUPFILE ):

        CLEANUP_DUPCNT += 1

        if io_.isfile( f ):
            cleanup_dup_del( f, CLEANUP_DUPCNT )

        del _.DUPFILE[ f ]

    xonl()
    xonl( "POST-DUP: END" )
    xonl()


####################################################
# QBIT #############################################
####################################################

def generate_bitdepth_samples( path, B, scale = False ):

    RATE    = 44100
    SAMPLES = 44100   # one cycle

    # sine wave normalized -1.0 ... +1.0
    t    = np.arange( SAMPLES )
    sine = np.sin( 2 * np.pi * t / SAMPLES )

    for A in range( 2, B + 1 ):

        levels  = 2 ** A
        max_A   = levels // 2 - 1     # max signed value for A bits
        min_A   = -( levels // 2 )    # min signed value for A bits

        # quantize sine to A-bit signed integers
        quantized = np.round( sine * max_A ).astype( np.int64 )
        quantized = np.clip( quantized, min_A, max_A )

        max_B = 2 ** ( B - 1 ) - 1   # max signed value for B bits

        if scale:
            if max_A == 0:
                upsampled = quantized.astype( np.int64 )
            else:
                upsampled = np.round( quantized * max_B / max_A ).astype( np.int64 )
        else:
            # shift method: value << (B - A)
            upsampled = ( quantized << ( B - A ) ).astype( np.int64 )

        method   = "S" if scale else ""
        if A == B:
            filename = f"{path}_{A}{method}.wav"
        else:
            filename = f"{path}_{A}_{B}{method}.wav"

        if B == 8:
            # soundfile doesn't support uint8 - use scipy
            out = ( upsampled + 128 ).astype( np.uint8 )
            wavfile.write( filename, RATE, out )

        elif B == 16:
            out = upsampled.astype( np.int16 )
            sf.write( filename, out, RATE, subtype = "PCM_16" )

        elif B == 24:
            out = ( upsampled << 8 ).astype( np.int32 )
            sf.write( filename, out, RATE, subtype = "PCM_24" )

        elif B == 32:
            out = upsampled.astype( np.int32 )
            sf.write( filename, out, RATE, subtype = "PCM_32" )

        print( f"written: {filename}" )


def generate_qbit_files( path ):

    path = r"C:\WAVLIB\small\a\SINE\sine"

    generate_bitdepth_samples( path, 8 )
    generate_bitdepth_samples( path, 8, 1 )

    generate_bitdepth_samples( path, 16 )
    generate_bitdepth_samples( path, 16, 1 )

    generate_bitdepth_samples( path, 24 )
    generate_bitdepth_samples( path, 24, 1 )

    generate_bitdepth_samples( path, 32 )
    generate_bitdepth_samples( path, 32, 1 )











################################################

# v4 was best











def qbit_autotest_item( path, bit, r ):
 
    _.QBITAUTOTEST = None

    A = {}

    if match( path, r"/SINE/[^\x0D\x0A_]*_(\d+)(_(\d+))?S?\.wav", A ):

        _.QBIT_AUTOTEST_TOTAL += 1

        a = int( A[ "1" ] )
        if "3" in A and A[ "3" ] != None:

            b = int( A[ "3" ] )

            if r == a and bit == b:
                return

        elif r == a:
            return

        _.QBITAUTOTEST = 1
        _.QBIT_AUTOTEST_FAILED += 1

        _.QBIT += " (!)"



def qbit_autotest_report( t ):

    _.QBIT_AUTOTEST_REPORT += t + ln()


def qbit_autotest_final():

    if _.QBIT_AUTOTEST_REPORT != "":

        f = _.QBIT_AUTOTEST_FILE

        t = _.QBIT_AUTOTEST_REPORT
        t = text.csioff( t )

        tc = _.QBIT_AUTOTEST_TOTAL
        fc = _.QBIT_AUTOTEST_FAILED

        s = ln()
        s += ln( f"QBIT TEST TOTAL:  {tc}" )
        s += ln( f"QBIT TEST FAILED: {fc}" )
        s += ln()

        t += s
    
        t = io_.todata( t )
        io_.wrfile( f, t )









