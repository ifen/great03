__author__ = 'Ian Fenech Conti'


class BranchCollection:

    def __init__(self):
        self.data = []
        self.branch_path = ''
        self.branch_type = 'ground'
        self.images = []


class StarfieldImage:

    def __init__(self):
        self.data = []
        self.file_name = ''
        self.file_path = ''
        self.catalogue_path = ''
        self.image_id = -1
        self.branch_type = 'ground'
        self.tile_path = ''
        self.tiles = []
        self.image_data = []


class StarfieldTile:

    def __init__(self):
        self.data = []
        self.tile_x = 0
        self.tile_y = 0
        self.tile_size = 2
        self.stars_in_tile = []
        self.subtiles = []
        self.path = ''


class StarfieldSubtile:

    def __init__(self):
        self.data = []
        self.tile_x = 0
        self.tile_y = 0
        self.tile_size = 0.5
        self.directory = ''
        self.image_path = ''
        self.image_placeholder = ''
        self.catalogue_path_before = ''
        self.catalogue_path = ''
        self.table_path = ''
        self.head_path = ''
        self.stars_in_subtile = []
        self.image_data = []
