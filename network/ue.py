from network.application import ApplicationProfile


class UE:

    def __init__(self, id_, point):
        self.id = id_
        self.point = point
        self.datarate = 0.0
        self.resource_blocks = 0.0
        self.profile = ApplicationProfile.DATA_BACKUP
        self._evaluation = False
        self.priority = False

    @property
    def evaluation(self):
        if self.datarate >= self.profile.datarate:
            self._evaluation = True
        return self._evaluation

    @evaluation.setter
    def evaluation(self, value):
        self._evaluation = value

    def __str__(self):
        return 'UE id={}, bitrate={}, profile={}'.format(self.id, self.datarate, self.profile)
