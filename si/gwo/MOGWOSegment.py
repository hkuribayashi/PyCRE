class MOGWOSegment:
    def __init__(self, archive_max):
        self.archive_max = archive_max
        self.archive = []

    def add_solution(self, p):
        if len(self.archive) < self.archive_max:
            if len(self.archive) is 0:
                self.archive.append(p)
            else:
                list_add = []
                list_del = []
                for other_p in self.archive:
                    if p < other_p:
                        list_add.append(p)
                        list_del.append(other_p)
                    elif p.evaluation_f1 < other_p.evaluation_f1 or p.evaluation_f2 < other_p.evaluation_f2:
                        list_add.append(p)
                for id_del in list_del:
                    self.archive.remove(id_del)
                for id_add in list_add:
                    self.archive.append(id_add)
            self.archive = list(set(self.archive))
        else:
            return False


    def __str__(self):
        str_return = ""
        for p in self.archive:
             str_return = str_return + p
        return "[" + str_return + "]"