


########################################################
# IO v0.1 ##############################################
########################################################
#
#
#
#
#
########################################################
########################################################
########################################################

import  os
import  shutil
import  hashlib
import  subprocess
import  ctypes
from    pathlib import  Path
from    typing  import  List

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


UPPER_FILEPATH      = 1


####################################################

ABSOLUTE_PROTECTION = {}

def add_absprotpath( path ):

    global  ABSOLUTE_PROTECTION

    f = FPATH( path )

    ABSOLUTE_PROTECTION[ f ] = 1

################################################

def absolute_protection( path ):

    global  ABSOLUTE_PROTECTION

    f = FILEPATH( path )

    for p in ABSOLUTE_PROTECTION:

        if f.startswith( p ):

            return ""

    return f"ABSOLUTE PROTECTION ERROR: {path}"


####################################################

def todata( t ):

    if isinstance( t, str ):
        return t.encode( "utf-8" )

    if isinstance( t, bytes ):
        return t

    tp = type( t )
    fatal( f"todata( {tp} noy supported" )


####################################################

def getfiles( source, rxp, lv = 0 ):

    # returns list of items that are each is file
    # each item have 8 fields; the field 0 is filepath
    # files or folders starting by '_' are ignored
    #___________________________

    err = ""
    files = []

    try:

        source = fpath( source )

        if lv == 1:

            F = {}
            for name in os.scandir( source ):

                if name.is_file():

                    name = name.path
                    if match( name, rxp ):
                        
                        f = filepath( name )
                        F[ name ] = 1

            return F

        if not os.path.isdir( source ):

            return files, f"not a directory: {source}"

        for root, dirs, filez in os.walk( source ):

            dirs[ : ] = [ d for d in dirs if not d.startswith( "_" ) ]

            for name in filez:

                if name.startswith( "_" ):

                    continue

                if match( name, rxp ):

                    full = root + "/" + name
                    item = [ full, "", "", "", "", "", "", "" ]
                    files.append( item )

    except Exception as e:

        err = str( e )

    return files, err


####################################################

def rdfile( path ):

    try:
        p = Path( path )
        return p.read_bytes(), ""

    except Exception as e:

        return "", e


################################################

def wrfile( path, data ):

    err = absolute_protection( path )
    if err:
        return err

    data = todata( data )

    try:
        p = Path( path )
        p.parent.mkdir( parents = True, exist_ok = True )
        p.write_bytes( data )
        return ""

    except Exception as e:
        return str( e )

################################################

def movfile( dst, src = None ):

    if isinstance( dst, list ):

        # movfile( list )

        lst = dst

        for dst, src in lst:

            err = movfile( dst, src )
            if err:

                return err

        return ""

    #conl( f"MOVFILE {dst} < {src}'" )

    # movfile( dstfile, srcfile )

    if src is None:

        return f"movfile( {dst}, source not specified )"

    err = absolute_protection( dst )
    if err:
        return err

    try:

        src = Path( src )
        dst = Path( dst )

        if not src.exists() or not src.is_file():
            return "NF"

        dst.parent.mkdir( parents = True, exist_ok = True )
        shutil.move( str( src ), str( dst ) )

        return ""

    except Exception as e:

        return f"movfile( {dst}, {src} )" + str( e )


################################################

def renfile( path, newpath ):

    err = absolute_protection( newpath )
    if err:
        return err

    try:
        path = filepath( path )

        if not path:
            return "invalid filepath"

        if not newpath:
            return "invalid new name"

        dirpath = os.path.dirname( path )
        newpath = os.path.join( dirpath, newpath )

        os.replace( path, newpath )
        return ""

    except Exception as e:
        return str( e )


################################################

def copyfile( dst, src ):

    try:
        if not os.path.isfile( src ):
            return False

        dstdir = os.path.dirname( dst )
        if dstdir and not os.path.exists( dstdir ):

            os.makedirs( dstdir, exist_ok = True )

        shutil.copy( src, dst )
        return ""

    except Exception as e:
      
        return str( e )


################################################

def delfile( path ):

    err = absolute_protection( path )
    if err:
        return err

    try:

        if os.path.isfile( path ):

            os.remove( path )
            return None

        else:

            return "File not found"

    except Exception as e:

        return str( e )


################################################

def sizefile( path ):

    # returns:
    #
    #       size, err
    #___________________________

    try:

        return os.path.getsize( path ), ""

    except Exception as e:

        return 0, str( e )


################################################

def isfile( path ):

    p = Path( path )
    return os.path.isfile( path )


################################################

def hashfile( path ):

    path = filepath( path )

    try:

        if not os.path.isfile( path ):

            return ""

        file = filename( path )

        chunk_size = 1024 * 1024
        hobj = hashlib.blake2b()

        with open( path, "rb" ) as f:

            while True:

                chunk = f.read( chunk_size )

                if not chunk:

                    break

                hobj.update( chunk )

        h = hobj.hexdigest()

        return h, ""

    except Exception as e:

        stat()
        err = f"get hash error: {path} ({e})"

        return "", err


####################################################

def defdir( path ):

    Path( path ).mkdir( parents = True, exist_ok = True )


################################################

def clonedir( dst, src ):

    stat( f"cloning folder {src} to {dst}" )

    try:
        src = os.path.abspath( src )
        dst = os.path.abspath( dst )

        if not os.path.isdir( src ):
            return f"source is not a directory: {src}"

        if os.path.exists( dst ):
            if not os.path.isdir( dst ):
                return f"destination exists and is not a directory: {dst}"

            # remove contents of dst, but keep the directory
            for name in os.listdir( dst ):
                path = os.path.join( dst, name )
                if os.path.isdir( path ) and not os.path.islink( path ):
                    shutil.rmtree( path )
                else:
                    os.remove( path )
        else:
            os.makedirs( dst, exist_ok = True )

        # copy contents of src into dst
        for name in os.listdir( src ):
            s = os.path.join( src, name )
            d = os.path.join( dst, name )
            if os.path.isdir( s ):
                shutil.copytree( s, d )
            else:
                shutil.copy2( s, d )

        stat()
        return ""

    except Exception as e:
        stat()
        return str(e)


################################################

def copydir( dst, src ):

    stat( f"copy folder {src} to {dst} ..." )

    try:
        src = os.path.abspath( src )
        dst = os.path.abspath( dst )

        if not os.path.isdir( src ):
            return f"source is not a directory: {src}"

        os.makedirs( dst, exist_ok = True )

        for root, dirs, files in os.walk( src ):
            rel = os.path.relpath( root, src )
            dst_root = dst if rel == "." else os.path.join( dst, rel )

            os.makedirs( dst_root, exist_ok = True )

            for d in dirs:
                os.makedirs( os.path.join( dst_root, d ), exist_ok = True )

            for f in files:
                s = os.path.join( root, f )
                d = os.path.join( dst_root, f )
                shutil.copy2( s, d )

        stat()
        return ""

    except Exception as e:
        stat()

        return str( e )


################################################

def isdir( path ):

    p = Path( path )
    return p.exists() and p.is_dir()


################################################

def getdirs( p ):

    R = {}
    p = fpath( p )

    try:
        
        for e in os.scandir( p ):

            if e.is_dir():

                R[ e.name ] = e.path + "/"

    except Exception as err:

        return R, str( err )

    return R, ""


####################################################

FILE_ATTRIBUTE_READONLY         = 0x00000001
INVALID_FILE_ATTRIBUTES         = 0xFFFFFFFF

kernel32 = ctypes.WinDLL( "kernel32", use_last_error = True )

GetFileAttributesW              = kernel32.GetFileAttributesW
GetFileAttributesW.argtypes     = [ ctypes.c_wchar_p ]
GetFileAttributesW.restype      = ctypes.c_uint32

SetFileAttributesW              = kernel32.SetFileAttributesW
SetFileAttributesW.argtypes     = [ ctypes.c_wchar_p, ctypes.c_uint32 ]
SetFileAttributesW.restype      = ctypes.c_int

def attroff( path: str ) -> list[ tuple[ str, str ] ]:

    stat( f"removing attributes: {path}" )

    root = Path( path )
    errors: list[ tuple[ str, str ] ] = []

    if not root.exists():

        raise FileNotFoundError(f"Path not found: {root}")

    def clear_readonly( target: Path ) -> None:

        p = str( target )
        attrs = GetFileAttributesW( p )

        if attrs == INVALID_FILE_ATTRIBUTES:

            err = ctypes.get_last_error()
            errors.append( ( p, f"GetFileAttributesW failed: {err}" ) )
            return

        if attrs & FILE_ATTRIBUTE_READONLY:

            new_attrs = attrs & ~FILE_ATTRIBUTE_READONLY
            if not SetFileAttributesW( p, new_attrs ):

                err = ctypes.get_last_error()
                errors.append( ( p, f"SetFileAttributesW failed: {err}" ) )

    # Process all nested files and folders

    for item in root.rglob( "*" ):

        clear_readonly( item )

    # Process the root folder itself
    clear_readonly( root )

    stat()

    return errors


####################################################

def filepath( path = None, base = None ):

    if path is None:
        return None

    path = str( path )

    t = os.path.abspath( path )

    if path.endswith( "/" ):

        t = t + "/"  

    t = gsub( t, r"[\\/]+", "/" )

    if base is not None:

        t = gsub( t, "(?i)^" + base, "./" )

    return t

#_______________________________________

def FILEPATH( f, base = None ):

    f = filepath( f, base )

    if UPPER_FILEPATH:
        f = f.upper()

    return f


################################################

def filename( path ):
   
    path = os.path.abspath( path )
    path = gsub( path, r"^([^\\/]+[\\/])+" )

    return path

#_______________________________________

def FILENAME( path ):

    f = filename( path )

    if UPPER_FILEPATH:
        f = f.upper()

    return f


################################################

def filenam( path ):

    path = filename( path )
    path = gsub( path, r"\.[^\\/.]*$" )

    return path

#_______________________________________

def FILENAM( path ):

    f = filenam( path )

    if UPPER_FILEPATH:
        f = f.upper()

    return f

################################################

def fext( path ):

    path = filename( path )

    A = {}
    match( path, r"(\.[^\.]*)?$", A )

    path = A[ "1" ]

    return path


################################################

def fpathnam( path ):

    path = os.path.abspath( path )
    path = gsub( path, r"\.[^\\/.]*$" )
    path = gsub( path, r"[\\/]+", "/" )

    return path

#_______________________________________

def FPATHNAM( path ):

    f = fpathnam( path )

    if UPPER_FILEPATH:
        f = f.upper()

    return f


################################################

def fpath( f, base = None ):

    f = filepath( f, base )

    f = gsub( f, r"[^\\/]+$" )
    f = gsub( f, r"[\\/]+", "/" )
    
    return f


############################################

def FPATH( f, base = None ):

    f = fpath( f, base )

    if UPPER_FILEPATH:
        f = f.upper()

    return f


########################################################
########################################################
########################################################


