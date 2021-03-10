from nodeeditor.node_scene import Scene
from nodeeditor.utils import *
from nodeeditor.node_scene import InvalidFile
from vpl_graphics_scene import QDMGraphicsScene

import os
import json

class VplScene(Scene):

    def loadFromFile(self, filename:str):
        """
        Load `Scene` from a file on disk

        :param filename: from what file to load the `Scene`
        :type filename: ``str``
        :raises: :class:`~nodeeditor.node_scene.InvalidFile` if there was an error decoding JSON file
        """
        print("using vplScene loading")
        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data)
                self.filename = filename
                self.deserialize(data)
                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                dumpException(e)

    def initUI(self):
        
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)
