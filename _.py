


#__ NORM ___________________

VOL_OK_LEVEL            = 95
TARGET_PERCENT          = 98.8


#__ SPLIT __________________

MAX_SPLIT_PIECES        = 10
MIN_SPLIT_PIECE_VOL     = 20
MIN_SPLIT_PIECE_TIME    = 0.05

MIN_SILENCE_LEVEL       = -70
MIN_SILENCE_PERIOD      = 0.35


#__ TRIM ___________________

MIN_LEFTRIM_FRAMES      = 32
MIN_RIGHTRIM_FRAMES     = 32
MIN_TRIM_TIME           = 0.0001
TRIM_TRESHOLD           = -80


NORMALIZE_LEVEL_ALERT   = 50








ATTR_TOWAV              = 9
ATTR_RESCAN             = 8
ATTR_NORM               = 7
ATTR_QBIT               = 6
ATTR_SPLIT              = 5
ATTR_LEFTRIM            = 4
ATTR_RIGHTRIM           = 3
ATTR_DUP                = 2
ATTR_ORACLE             = 1
ATTR_SORT               = 0

MASK_ATTR_TOWAV         = 1 << ATTR_TOWAV
MASK_ATTR_RESCAN        = 1 << ATTR_RESCAN
MASK_ATTR_NORM          = 1 << ATTR_NORM
MASK_ATTR_QBIT          = 1 << ATTR_QBIT
MASK_ATTR_SPLIT         = 1 << ATTR_SPLIT
MASK_ATTR_LEFTRIM       = 1 << ATTR_LEFTRIM
MASK_ATTR_RIGHTRIM      = 1 << ATTR_RIGHTRIM
MASK_ATTR_DUP           = 1 << ATTR_DUP
MASK_ATTR_ORACLE        = 1 << ATTR_ORACLE
MASK_ATTR_SORT          = 1 << ATTR_SORT

DEFAULT_ATTR            = MASK_ATTR_TOWAV     | \
                          MASK_ATTR_NORM      | \
                          MASK_ATTR_QBIT      | \
                          MASK_ATTR_SPLIT     | \
                          MASK_ATTR_LEFTRIM   | \
                          MASK_ATTR_DUP       | \
                          MASK_ATTR_ORACLE    | \
                          MASK_ATTR_SORT

REGEXMAC0               = {}
HASHFILE                = {}
FILEHASH                = {}
NEWITEMS                = {}
OLDITEMS                = {}

LOGSTR                  = {}


TYPES                   = {}

VENDOR              = ""

SESSION_START           = 0
TIMECNT                 = 0



FILES = {
    "TOWAV":            0,
    "ERRORTOWAV":       0,
    "NORM":             0,
    "SPLIT":            0,
    "SPLITS":           [],
    "SPLITGROUP":       [],
    "LEFTRIM":          0,
    "RIGHTRIM":         0,
    "DUP":              0,
    "OK":               0,
    "ERROR":            0,
    "QBIT":             0,
    "PROC":             0 }

FILELIST = {
    "TOWAV":            [],
    "ERRORTOWAV":       [],
    "NORM":             [],
    "SPLIT":            [],
    "SPLITS":           [],
    "LEFTRIM":          [],
    "RIGHTRIM":         [],
    "DUP":              [],
    "OK":               [],
    "ERROR":            [],
    "QBIT":             [],
    "PROC":             [] }

NORM                    = \
SPLIT                   = \
SPLITQ                  = \
LEFTRIM                 = \
RIGHTRIM                = \
DUP                     = \
ORACLE                  = \
ERROR                   = \
TOWAV                   = None
QBIT                    = ""
QBIT_SUFFIX             = ""

MULTIMEDIA_EXT          = r"(?i)\.(mp3|flac|aac|ogg|m4a|wma|alac|aiff|opus|ape|mp4|mkv|avi|mov|webm|flv|3gp|mpeg|mpg|wmv)$"

GLOBAL_TAB_CNTR         = 0
GLOBAL_TAB_VAL          = 0

SPLITCNT                = 0


LASTITEMREPORT          = ""



QBITAUTOTEST            = ""
QBIT_AUTOTEST_REPORT    = ""
QBIT_AUTOTEST_FILE      = "_IMPORT/qbit.log"

QBIT_AUTOTEST_TOTAL = \
QBIT_AUTOTEST_FAILED  = 0



REPORTPTR               = None
USERVENDOR              = None
USERPACK                = None
ITEM_ATTR               = ""
EOL                     = "\x0D\x0A"

REGEXSTR                = ""

VENDORPACK_INFO         = 0         # if true then show vendorpack info
INTERNAL1_INFO          = 0         # if true then show internal1 info (POST-PHASE)

DUPFILE                 = {}
ZEROSTAT                = {}


LISTDUP_CNT             = 0

SAMECNT                 = 0

TOTAL                   = 0




