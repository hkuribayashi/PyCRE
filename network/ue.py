from network.application import ApplicationProfile


class UE:

    def __init__(self, id_, point):
        self.id = id_
        self.point = point
        self.bitrate = 0.0
        self.resource_blocks = 0.0
        self.profile = ApplicationProfile.DATA_BACKUP

    def __str__(self):
        return 'UE id={}, profile={}'.format(self.id, self.profile)
