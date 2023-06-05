import argparse


class AcquisitionParameters:
    # spot: str
    # xOffset: int
    # yOffset: int
    # path: str
    # name: str
    # geometry: str
    # laserOffsetX: int
    # laserOffsetY: int
    # acqtype: str
    # ceTable: str

    def __init__(self, args):
        parser = argparse.ArgumentParser(description="timsTOF Maldi controller")

        parser.add_argument('--spot', required=True, type=str, help="The spot on a 384 target plate to be measured")
        parser.add_argument('--xoffset', required=True, type=int, help="The offset in x dimension")
        parser.add_argument('--yoffset', required=True, type=int, help="The offset in y dimension")
        parser.add_argument('--path', required=True, type=str, help="The parent directory to store the analysis in.")
        parser.add_argument('--name', required=True, type=str, help="The name of the analysis.")
        parser.add_argument('--acqtype', required=False, choices=['accumulate', 'single'],
                            help="Specifies how the data shall be handled.\n"
                                 "\"accumulate\" = add to current acquisition.\n" +
                                 "\"single\" = store as single file (default).\n", default='single')
        parser.add_argument('--cetable', required=False,
                            help="Path to csv file with collision energy settings. Must contain columns \'mass\' (decimal), " +
                                 "\'iso_width\' (decimal), \'ce\' (decimal), \'type\' (0=base or 1=fixed) ")
        parser.add_argument('--geometry', required=False, type=str,
                            help="Speficy a sample carrier geometry to select specific spots.")
        parser.add_argument('--laseroffsetx', required=False, type=int, help="Specifies a laser offset in x dimension",
                            default=None)
        parser.add_argument('--laseroffsety', required=False, type=int, help="Specifies a laser offset in y dimension",
                            default=None)
        parser.add_argument('--precursorlist', required=True, type=str,
                            help="Path to csv file containing the list of precursors for this spot")
        parser.add_argument('--isolationwidth', required=False, type=float, default=None,
                            help="Manually sets the isolation width in the MALDI mode. Overrides the isolation given in the CE table (if there is one).")

        arguments = parser.parse_args(args)

        # make a valid path so we can concatenate
        if not arguments.path[len(arguments.path) - 1] == '/':
            arguments.path = arguments.path + '/'

        self.spot: str = arguments.spot
        self.xOffset: int = arguments.xoffset
        self.yOffset: int = arguments.yoffset
        self.path: str = arguments.path
        self.name: str = arguments.name
        self.geometry: str = arguments.geometry
        self.laserOffsetX: int = arguments.laseroffsetx
        self.laserOffsetY: int = arguments.laseroffsety
        self.acqtype: str = arguments.acqtype
        self.ceTable = arguments.cetable
        self.precursorList = arguments.precursorlist
        self.isowdith = arguments.isolationwidth

        # print(str(arguments))

    def fromArgs(spot: str, path: str, name: str, precursorList: str, xOffset: int = 0, yOffset: int = 0,
                 geometry: str = None, laserOffsetX: int = 0, laserOffsetY: int = 0, acqtype: str = "single",
                 ceTable: str = None, isowidth: float = None):
        # self.ceTable = ceTable
        # self.laserOffsetY = laserOffsetY
        # self.laserOffsetX = laserOffsetX
        # self.yOffset = yOffset
        # self.xOffset = xOffset
        # self.spot = spot
        # self.path = path
        # self.geometry = geometry
        # self.name = name
        # self.acqtype = acqtype
        return AcquisitionParameters(
            ["--spot", spot, "--path", path, "--name", name, "--xoffset", xOffset, "--yoffset", yOffset, "--geometry",
             geometry, "--laserOffsetX", laserOffsetX, "--laserOffsetY", laserOffsetY, "--acqtype", acqtype,
             "--cetable", ceTable, "--precursorlist", precursorList, "--isolationwidth", isowidth])
