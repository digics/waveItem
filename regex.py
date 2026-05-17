


########################################################
# REGEX v0.1 ###########################################
########################################################














########################################################
########################################################
########################################################

import  re
from    typing      import  Pattern, Dict
from    typing      import  Any

from    common      import  *
import  text

REGEX: Dict[ str, Pattern ] = {}
REGEX[ "^" ] = re.compile( r"a\A" )


####################################################

def gsub( src, rx, rp = "" ):

    r = regex( rx )

    return re.sub( r, rp, src )


####################################################
# regex error problem

def regex( string ):

    # if string is started by 'i:' then case insensitive
    #___________________________

    if string in REGEX:

        return REGEX[ string ]

    ci = 0
    rx = gsub( string, r"^i:" )
    if rx != string:
        ci = re.IGNORECASE

    try:

        compiled = re.compile( rx, ci )

    except re.error as e:

        fatal( f'Regex compile error: "{string}" -> {e}' )

        return REGEX[ "^" ]

    REGEX[ string ] = compiled

    return compiled


####################################################

def match( string, rxp = None, target = None ):

    if target is None:
        target = {}

    if string is None:
        return None

    target.clear()

    rx = regex( rxp )

    m = rx.search( string )

    target[ "regex" ] = rxp

    if not m:
        target[ "-1" ] = string
        target[ "0" ] = ""
        target[ "+1" ] = None
        return ""

    start, end = m.span( 0 )

    target[ "-1" ] = string[ :start ]
    target[ "0" ] = string[ start:end ]
    target[ "0S" ] = start
    target[ "0L" ] = len( target[ "0" ] )
    target[ "+1" ] = string[ end: ]

    for i, g in enumerate( m.groups(), 1 ):
        target[ str( i ) ] = g

    for k, v in m.groupdict().items():
        target[ k ] = v

    if len( target[ "0" ] ):

        return target[ "0" ][ 0 ]

    return ""
  

####################################################

def xmatch( D ):

    # D[ "+1" ]       = srcstring
    # D[ "regex" ]    = regex
    #_._

    def xmatch0( D, r = None ):

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
            ii = i
            i = str( i )
            D[ i ] = t
            D[ f"{i}S" ] = s + m.start( ii )
            D[ f"{i}L" ] = len( t )

        for i, t in m.groupdict().items():
            D[ i ] = t
            D[ f"{i}S" ] = s + m.start( i )
            D[ f"{i}L" ] = len( D[ i ] )

        if len( D[ "0" ] ):

            return D[ "0" ][ 0 ]

        return ""

    #_._

    def xcoord( D, s ):

        A = {}
        r = match( D[ "+1" ][ :s ], r"[^\x0A\x0D]*$", A )

        return A[ "0L" ]

    #_._

    def xmatch_xbox_capture( D ):

        s = D[ "0S" ]

        x = xcoord( D, s + 1 ) + 1

        r =   r"^[^\x0A\x0D]*(\x0D?\x0A" \
            + r"(([\x09\x20\xA0]{" + str( x ) + r"}[^\x0A\x0D]*" \
            + r"|[\x09\x20\xA0]*)\x0D?(\x0A|$))*)?"

        rx = regex( r )
        s = D[ "+1S" ]
        m = rx.search( D[ "+1" ][ s: ] )
        if m:

            start, end = m.span( 0 )

            xb = m.group( 0 )

            xxb = gsub( xb, r"[\x20\xA0]*(\x0D?\x0A[\x20\xA0]*)*$" )
            
            end -= len( xb ) - len( xxb )

            D[ "0" ] = D[ "0" ] + xxb
            D[ "+1S" ] += end - start

            t = m.group( 0 )

            x = x + D[ "0L" ] - 1

            D[ "0L" ] = len( D[ "0" ] )

            t = " " * x + t

            text.width( t )

            x = text.WIDTH_LOWX

            t = text.xoffset( t, -x )

            if 1:
                t = re.sub( regex( r"^[\x09\x20\xA0]+" ), "", t, count = 1 )
                t = re.sub( regex( r"[\x09\x20\xA0]*(\x0D?\x0A[\x09\x20\xA0]*)*$" ), "", t, count = 1 )

            D[ "xbox" ] = t

    #_._

    r = xmatch0( D )
    if r is not None:

        if "xbox" in D:

            xmatch_xbox_capture( D )

    return r


########################################################
########################################################
########################################################


