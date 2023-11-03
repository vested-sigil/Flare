
Class Points:
    def __init__(self, name, type, ply, segments, variances):
        self.name = name
        self.type = type
        self.ply = ply
        self.segments = segments
        self.variances = variances

    def __str__(self):
        return f"{self.name}:{self.type}:{self.ply}:{self.segments}:{self.variances}"

    def __repr__(self):
        return f"Points({self.name}, {self.type}, {self.ply}, {self.segments}, {self.variances})"

    def __eq__(self, other):
        if isinstance(other, Points):
            return self.name == other.name and self.type == other.type and self.ply == other.ply and self.segments == other.segments and self.variances == other.variances
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_ply(self):
        return self.ply

    def set_ply(self, ply):
        self.ply = ply

    def get_segments(self):
        return self.segments

    def set_segments(self, segments):
        self.segments = segments

    def get_variances(self):
        return self.variances

    def set_variances(self, variances):
        self.variances = variances

    def is_quantum(self):
        return len(self.variances) > 0

    def resolve_ambiguity(self):
        if len(self.variances) == 1:
            self.variances = self.variances[0]
        elif len(self.variances) > 1:
            most_common_variance = max(self.variances, key=lambda x: x)
            self.variances = most_common_variance

class Pair:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __str__(self):
        return f"({self.point1}:{self.point2})"

    def __repr__(self):
        return f"Pair({self.point1}, {self.point2})"

    def get_ply(self):
        return max(self.point1.ply, self.point2.ply)

    def is_quantum(self):
        return self.point1.is_quantum() or self.point2.is_quantum()


class Path:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return f"({','.join(self.points)})"

    def __repr__(self):
        return f"Path({','.join(self.points)})"

    def get_ply(self):
        return max(p.ply for p in self.points)

    def is_quantum(self):
        return any(p.is_quantum() for p in self.points)

def ply_inference(ply, points):
    pairs = []
    paths = []
    for point in points:
        if point.ply == ply:
            for pair in point.pairs:
                if pair.ply == ply:
                    pairs.append(pair)
            for path in point.paths:
                if path.ply == ply:
                    paths.append(path)
    return pairs, paths


def proximity(pairs):
    proximity_pairs = []
    for pair in pairs:
        for pair2 in pairs:
            if pair != pair2:
                if pair.point1 == pair2.point1:
                    proximity_pairs.append((pair, pair2))
                elif pair.point1 == pair2.point2:
                    proximity_pairs.append((pair, pair2))
                elif pair.point2 == pair2.point1:
                    proximity_pairs.append((pair, pair2))
                elif pair.point2 == pair2.point2:
                    proximity_pairs.append((pair, pair2))
    return proximity_pairs


def ppp(points):
    ply = ('code', 0)
    points = [
        Points('a', 'code', 0, [('b', 1)]),
        Points('b', 'syntax', 1, []),
        Points('c', 'context', 2, []),
    ]
    pairs, paths = ply_inference(ply, points)
    proximity_pairs = proximity(pairs)
    print(pairs)
    print(paths)
    print(proximity_pairs)
    if point.is_quantum():
        if len(point.variances) == 1:
            return point.variances[0]
        else:
            most_common_variance = max(point.variances, key=lambda x: x)
            return most_common_variance
    else:
        return point.ply

