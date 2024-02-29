from utilities import Player


# Play.py
STIMULATE_STPES = 100
PRINT_BOARD = False
GUI_ON = False

COLS = "ABCDEFGHJKLMNOPQRST"
STONE_TO_CHAR = {
    None: " . ",
    Player.black: " B ",
    Player.white: " W ",
}

WIDTH = 9
HEIGHT = 9

PASS_STONE = (-1, -1)
SURRENDER_STONE = (-10, -10)

# Constants for the display
BOARD_SIZE = (800, 800)  # Size of the board in pixels
BOARD_COLOR = (248, 196, 113)  # Color of the board
LINE_COLOR = (0, 0, 0)  # Color of the lines
STONE_RADIUS = int(BOARD_SIZE[0] / WIDTH / 2 * 0.7)  # Radius of the stones
BOARD_MARGIN = 100  # Margin around the board
GRID_SIZE = (BOARD_SIZE[0] - 2 * BOARD_MARGIN) / (WIDTH - 1), (
    BOARD_SIZE[1] - 2 * BOARD_MARGIN
) / (HEIGHT - 1)
LINE_WIDTH = 2  # Width of the board lines
FONT_SIZE = 30
FONT_COLOR = (0, 0, 0)


HASH_CODE = {
    ((-1, -1), Player.black): 0000000000000000000,
    ((-10, -10), Player.black): 1111111111111111111,
    ((-1, -1), Player.white): 2222222222222222222,
    ((-10, -10), Player.white): 3333333333333333333,
    ((0, 0), None): 7349794984634908158,
    ((0, 0), Player.black): 2577484128315197955,
    ((0, 0), Player.white): 2988129388360669189,
    ((0, 1), None): 7251182020906809862,
    ((0, 1), Player.black): 8382500506112718343,
    ((0, 1), Player.white): 2553043670731189257,
    ((0, 2), None): 3818790000598916618,
    ((0, 2), Player.black): 5000905371307676680,
    ((0, 2), Player.white): 2891931831814004238,
    ((0, 3), None): 2977299961627648527,
    ((0, 3), Player.black): 4012362483232672784,
    ((0, 3), Player.white): 5252297799859909646,
    ((0, 4), None): 3270751732854960147,
    ((0, 4), Player.black): 7728183601883506707,
    ((0, 4), Player.white): 5989899997778481687,
    ((0, 5), None): 4272423801382648345,
    ((0, 5), Player.black): 4970411597144725026,
    ((0, 5), Player.white): 589008149238762535,
    ((0, 6), None): 8870893546506640421,
    ((0, 6), Player.black): 4906293754246000166,
    ((0, 6), Player.white): 5213502344741460007,
    ((0, 7), None): 4163977029663087146,
    ((0, 7), Player.black): 9065202374915728422,
    ((0, 7), Player.white): 4414979630482021420,
    ((0, 8), None): 4386773227894073898,
    ((0, 8), Player.black): 5785377379849441837,
    ((0, 8), Player.white): 4187542720822536750,
    ((1, 0), None): 8870999803119110702,
    ((1, 0), Player.black): 577320512464655404,
    ((1, 0), Player.white): 1442626321311929908,
    ((1, 1), None): 8955592660968312883,
    ((1, 1), Player.black): 2346760968947277879,
    ((1, 1), Player.white): 967324053145457722,
    ((1, 2), None): 1374316109835900478,
    ((1, 2), Player.black): 5312345775751868478,
    ((1, 2), Player.white): 6306506777601312319,
    ((1, 3), None): 5137876029885099582,
    ((1, 3), Player.black): 991491890192603201,
    ((1, 3), Player.white): 202221648649567814,
    ((1, 4), None): 773746097844463689,
    ((1, 4), Player.black): 4115835414843298890,
    ((1, 4), Player.white): 7880066349844563018,
    ((1, 5), None): 3353132111561198157,
    ((1, 5), Player.black): 5968073062215335501,
    ((1, 5), Player.white): 1272002410105515087,
    ((1, 6), None): 7620147826752139342,
    ((1, 6), Player.black): 9127705806915490383,
    ((1, 6), Player.white): 8082426592410315859,
    ((1, 7), None): 2025625959053490263,
    ((1, 7), Player.black): 6206391228106699350,
    ((1, 7), Player.white): 7539626170347050582,
    ((1, 8), None): 432917307978506843,
    ((1, 8), Player.black): 8968480827255514204,
    ((1, 8), Player.white): 5807263234736119390,
    ((2, 0), None): 7872944445682646621,
    ((2, 0), Player.black): 3914004713124204641,
    ((2, 0), Player.white): 1438463295971430500,
    ((2, 1), None): 5250614460783010914,
    ((2, 1), Player.black): 2407587285132118629,
    ((2, 1), Player.white): 3880254134778175594,
    ((2, 2), None): 2245374355024073323,
    ((2, 2), Player.black): 1037713127918448750,
    ((2, 2), Player.white): 2951697498591242866,
    ((2, 3), None): 2714147714519316087,
    ((2, 3), Player.black): 7509209316595741305,
    ((2, 3), Player.white): 1422386638658864252,
    ((2, 4), None): 489579615302256765,
    ((2, 4), Player.black): 9136515925026270844,
    ((2, 4), Player.white): 8009119032349373564,
    ((2, 5), None): 5754199423687265919,
    ((2, 5), Player.black): 5641190221839433856,
    ((2, 5), Player.white): 2025983216884014213,
    ((2, 6), None): 5867153004674408076,
    ((2, 6), Player.black): 6761232361498173582,
    ((2, 6), Player.white): 5221203497240445583,
    ((2, 7), None): 4772811254238867086,
    ((2, 7), Player.black): 1219262801637203602,
    ((2, 7), Player.white): 5950013889033568398,
    ((2, 8), None): 2179446164046721682,
    ((2, 8), Player.black): 953845264737607832,
    ((2, 8), Player.white): 7589288831053119640,
    ((3, 0), None): 5695616831511120025,
    ((3, 0), Player.black): 4453610098394458778,
    ((3, 0), Player.white): 4420465248351159963,
    ((3, 1), None): 5355089975978203289,
    ((3, 1), Player.black): 7540579742945561753,
    ((3, 1), Player.white): 1931758981057197218,
    ((3, 2), None): 2319417831048855715,
    ((3, 2), Player.black): 2653794460496104102,
    ((3, 2), Player.white): 780026240909094578,
    ((3, 3), None): 2765724238413322417,
    ((3, 3), Player.black): 4453412963563781811,
    ((3, 3), Player.white): 1915695931676201138,
    ((3, 4), None): 4456365304583250098,
    ((3, 4), Player.black): 8945546949714946228,
    ((3, 4), Player.white): 7344036907904544949,
    ((3, 5), None): 6600377308269087414,
    ((3, 5), Player.black): 627790343642502329,
    ((3, 5), Player.white): 3065383406540787386,
    ((3, 6), None): 943433974575081147,
    ((3, 6), Player.black): 3162937911551385273,
    ((3, 6), Player.white): 166405387781003448,
    ((3, 7), None): 8241464063504837311,
    ((3, 7), Player.black): 5653550823023826113,
    ((3, 7), Player.white): 1663054674360815812,
    ((3, 8), None): 3884648560615433924,
    ((3, 8), Player.black): 1919254024871016134,
    ((3, 8), Player.white): 2307504453027659975,
    ((4, 0), None): 1679100505666663112,
    ((4, 0), Player.black): 6983792231698538182,
    ((4, 0), Player.white): 8383503794107863240,
    ((4, 1), None): 3560392215735871177,
    ((4, 1), Player.black): 153160176580215505,
    ((4, 1), Player.white): 6663093474918227151,
    ((4, 2), None): 3435946693632119000,
    ((4, 2), Player.black): 1820248498088559836,
    ((4, 2), Player.white): 4078883570869877979,
    ((4, 3), None): 2491198127360376029,
    ((4, 3), Player.black): 6288554869887099612,
    ((4, 3), Player.white): 5819108731275652830,
    ((4, 4), None): 5636608647878969567,
    ((4, 4), Player.black): 6262079457276945119,
    ((4, 4), Player.white): 7773846561232839389,
    ((4, 5), None): 8462836921043420382,
    ((4, 5), Player.black): 7827624508740102370,
    ((4, 5), Player.white): 2622848486129055460,
    ((4, 6), None): 4938833672506021605,
    ((4, 6), Player.black): 1510874019045839590,
    ((4, 6), Player.white): 8315953591679736040,
    ((4, 7), None): 4913416017772185327,
    ((4, 7), Player.black): 2318734981340325104,
    ((4, 7), Player.white): 120506916452893937,
    ((4, 8), None): 1922150218368023804,
    ((4, 8), Player.black): 5061844039135623421,
    ((4, 8), Player.white): 4330254540148450559,
    ((5, 0), None): 6310028120533661441,
    ((5, 0), Player.black): 8227079325866032385,
    ((5, 0), Player.white): 3203051260179803909,
    ((5, 1), None): 6151216917275736324,
    ((5, 1), Player.black): 1176729077445559051,
    ((5, 1), Player.white): 6952315611629672713,
    ((5, 2), None): 7050316459145641224,
    ((5, 2), Player.black): 5502480846272788236,
    ((5, 2), Player.white): 3659935375680732432,
    ((5, 3), None): 3346969646594077973,
    ((5, 3), Player.black): 5917239264327758612,
    ((5, 3), Player.white): 8818647290734677781,
    ((5, 4), None): 5161503664756791572,
    ((5, 4), Player.black): 7815172822939699991,
    ((5, 4), Player.white): 3240473913850813205,
    ((5, 5), None): 5239357671460349210,
    ((5, 5), Player.black): 5588936737746215704,
    ((5, 5), Player.white): 8525895493879073051,
    ((5, 6), None): 768615913245161247,
    ((5, 6), Player.black): 3451896978131680543,
    ((5, 6), Player.white): 5425942239419208988,
    ((5, 7), None): 2261915857155837721,
    ((5, 7), Player.black): 5395315317784336164,
    ((5, 7), Player.white): 5396872347840025386,
    ((5, 8), None): 5228790121024838451,
    ((5, 8), Player.black): 5374917027814221621,
    ((5, 8), Player.white): 7561072309480542518,
    ((6, 0), None): 7595133514720855863,
    ((6, 0), Player.black): 4335046943490447161,
    ((6, 0), Player.white): 1528160084986777915,
    ((6, 1), None): 6072665198194845499,
    ((6, 1), Player.black): 8247276433217472826,
    ((6, 1), Player.white): 710644701213702974,
    ((6, 2), None): 1763519023417590079,
    ((6, 2), Player.black): 8559766229396909371,
    ((6, 2), Player.white): 79069568738068802,
    ((6, 3), None): 896198469556106564,
    ((6, 3), Player.black): 7584196119704025410,
    ((6, 3), Player.white): 6485654122019833159,
    ((6, 4), None): 2053155095245428553,
    ((6, 4), Player.black): 8387342021053922633,
    ((6, 4), Player.white): 1236202791492507469,
    ((6, 5), None): 8952116819005247307,
    ((6, 5), Player.black): 1246995361527225682,
    ((6, 5), Player.white): 2077670789372912979,
    ((6, 6), None): 3315866560373246301,
    ((6, 6), Player.black): 6981371034134378844,
    ((6, 6), Player.white): 7815388262683600733,
    ((6, 7), None): 787663026216830306,
    ((6, 7), Player.black): 6609068135957261156,
    ((6, 7), Player.white): 953574031265940331,
    ((6, 8), None): 7834113156811477866,
    ((6, 8), Player.black): 2045550987817210734,
    ((6, 8), Player.white): 2263034362842222448,
    ((7, 0), None): 6023074171216486766,
    ((7, 0), Player.black): 4203154076385663348,
    ((7, 0), Player.white): 1701058886552949111,
    ((7, 1), None): 3446312767692248440,
    ((7, 1), Player.black): 1070621898880211836,
    ((7, 1), Player.white): 5884382163514565499,
    ((7, 2), None): 6583072039156440956,
    ((7, 2), Player.black): 7035838279033414525,
    ((7, 2), Player.white): 178768452194780034,
    ((7, 3), None): 1025799414899969410,
    ((7, 3), Player.black): 6604379319827633538,
    ((7, 3), Player.white): 3488317554708670341,
    ((7, 4), None): 7539487003576889221,
    ((7, 4), Player.black): 1921026025294743432,
    ((7, 4), Player.white): 9215708157852425098,
    ((7, 5), None): 2035382277714689426,
    ((7, 5), Player.black): 8765965015457285522,
    ((7, 5), Player.white): 9120533889163588503,
    ((7, 6), None): 1398485579774779291,
    ((7, 6), Player.black): 7364960629037533079,
    ((7, 6), Player.white): 5507480588709370264,
    ((7, 7), None): 4059833503816739757,
    ((7, 7), Player.black): 6421418153954977709,
    ((7, 7), Player.white): 7100521431015130539,
    ((7, 8), None): 7459302941613944751,
    ((7, 8), Player.black): 8179707191786408368,
    ((7, 8), Player.white): 2148707246109429170,
    ((8, 0), None): 15476152772006839,
    ((8, 0), Player.black): 8248477071086333877,
    ((8, 0), Player.white): 1892270686079948216,
    ((8, 1), None): 6563877252926565304,
    ((8, 1), Player.black): 5316447875064530360,
    ((8, 1), Player.white): 3115889996722074557,
    ((8, 2), None): 3950867055452398019,
    ((8, 2), Player.black): 6288902393145399747,
    ((8, 2), Player.white): 8132644207911564227,
    ((8, 3), None): 1148505391325884871,
    ((8, 3), Player.black): 2690343162559956935,
    ((8, 3), Player.white): 121110467472556491,
    ((8, 4), None): 1595130697069320141,
    ((8, 4), Player.black): 8049705639508555726,
    ((8, 4), Player.white): 2953800946973238235,
    ((8, 5), None): 681938989439200734,
    ((8, 5), Player.black): 2694752790930025437,
    ((8, 5), Player.white): 1691339261905866720,
    ((8, 6), None): 3177249461503798241,
    ((8, 6), Player.black): 2808091696286704098,
    ((8, 6), Player.white): 5332249593287008743,
    ((8, 7), None): 7787240531779272170,
    ((8, 7), Player.black): 8964331748145429995,
    ((8, 7), Player.white): 5626321466607200237,
    ((8, 8), None): 6474819793473592815,
    ((8, 8), Player.black): 729613370301068787,
    ((8, 8), Player.white): 4256294396971400185,
}
EMPTY_BOARD = 2255195057628481531
