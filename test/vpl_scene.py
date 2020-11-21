from nodeeditor.node_scene import Scene

class VplScene(Scene):

    def loadFromFile(self, filename:str):
        """
        Load `Scene` from a file on disk

        :param filename: from what file to load the `Scene`
        :type filename: ``str``
        :raises: :class:`~nodeeditor.node_scene.InvalidFile` if there was an error decoding JSON file
        """

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