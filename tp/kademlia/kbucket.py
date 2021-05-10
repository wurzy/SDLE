class KBucket:
    def __init__(self, k):
        self._k = k
        self._contacts = {}

    def add(self, contact, distance):
        if not self._contacts.__contains__(distance):
            self._contacts[distance] = []

        if(self._contacts[distance].__contains__(contact)):
            self._contacts[distance].remove(contact)
        elif (len(self._contacts[distance]) == self._k):
            raise Exception("Bucket full")

        self._contacts[distance].append(contact)

    def getkclose(self, distance):
        close = []

        distances = [d for d in self._contacts.keys()]
        while(len(close) < self._k and len(distances) > 0):
            closest = self._find_close(distances, distance)

            remaining = self._k - len(close)
            close.extend(self._contacts[closest][:remaining])
            distances.remove(closest)


        return close

    def _find_close(self, distances, distance):
        assert(len(distances) > 0)
        distances.sort()
        closest, delta = distances[0], abs(distance - distances[0])

        for k in distances[1:]:
            if(delta > abs(distance - k)):
                delta = abs(distance - k)
                closest = k
            else:
                break

        return closest

    def getBucket(self, distance):
        return self._contacts[distance]