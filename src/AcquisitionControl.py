import os
import shutil

from src.AcquisitionParameters import AcquisitionParameters
from src.InstrumentController import InstrumentController


class AcquisitionControl:
    # controller: InstrumentController

    def __init__(self):
        self.controller = InstrumentController()

    def runAcquisition(self, parameters: AcquisitionParameters):
        if not os.path.exists(parameters.path):
            os.mkdir(parameters.path)

        # copy precursor file
        shutil.copyfile(parameters.precursorList, "C:/BDalSystemData/timsTOF/maldi/maldi_tims_precursors.csv")

        # if acqtype == 'accumulate':
        #     controller.setAppendAcquisition(True)
        # else:
        #     controller.setAppendAcquisition(False)

        if parameters.laserOffsetX is not None and parameters.laserOffsetY is not None:
            self.controller.setLaserOffset(parameters.laserOffsetX, parameters.laserOffsetY)

        self.controller.directory = parameters.path
        self.controller.sampleName = parameters.name

        if parameters.geometry is not None:
            self.controller.maldiControl.selectGeometry(parameters.geometry)

        if parameters.ceTable is not None and os.path.exists(parameters.ceTable):
            self.controller.readAndSetCeTable(parameters.ceTable)

        if parameters.isowdith is not None:
            self.controller.overrideIsolationWidth(parameters.isowdith)

        self.controller.moveToSpotAndWait(parameters.spot, parameters.xOffset, parameters.yOffset)
        self.controller.singleSpotAcquisition()
        if(os.path.isfile("C:/BDalSystemData/timsTOF/maldi/maldi_tims_precursors.csv")):
            os.remove("C:/BDalSystemData/timsTOF/maldi/maldi_tims_precursors.csv")

        # self.controller.snapshot()
