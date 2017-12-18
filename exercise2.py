import random
from operator import itemgetter
random.seed(1)

# NUM_NEURONS = 10000
NUM_NEURONS = 1000  # Reduce num_neurons to use slower solution
NERVE_SIZE = 128000  # nanometers
CONFLICT_RADIUS = 500  # nanometers


# The slow (N^2) solution:
def checkconflicts(nerves, conflict_radius):
    conflict_count = 0
    for i in range(0, len(nerves)):
        for j in range(0, len(nerves)):
            if i == j:
                pass
            else:
                if eucl_distance_sq(nerves[i], nerves[j]) \
                        <= CONFLICT_RADIUS**2:
                    conflict_count += 1
    return conflict_count


# The (not-yet) working solution:
def check_for_conflicts(nerves, conflict_radius):
    conflicting_nerves = set()

    tree = kdtree(nerves)
    r = conflict_radius

    for i, nerve in enumerate(nerves):
        if range_query(curr_node=tree, point=nerve, r=r, depth=0):
            conflicting_nerves.add(i)
        else:
            pass
    return len(conflicting_nerves)


def eucl_distance_sq(nerve1, nerve2):
    d_sq = (nerve1[0] - nerve2[0])**2 + (nerve1[1] - nerve2[1])**2
    return d_sq


def gen_coord():
    return int(random.random() * NERVE_SIZE)


class Node(object):
    def __init__(self, location, left, right):
        self.location = location
        self.left = left
        self.right = right


class Rectangle(object):
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax


def kdtree(points, depth=0):
    try:
        k = len(points[0])
    except IndexError:
        return None

    axis = depth % k

    points.sort(key=itemgetter(axis))
    median = len(points) // 2

    return Node(
        location=points[median],
        left=kdtree(points[:median], depth + 1),
        right=kdtree(points[median + 1:], depth + 1)
    )


def range_query(curr_node, point, r, depth=0):
    conflict = False

    x = point[0]
    y = point[1]
    conflict_rect = Rectangle(x - r, x + r, y - r, y + r)

    while curr_node is not None:
        try:
            k = len(point)
        except IndexError:
            return None

        axis = depth % k

        if axis == 0:
            low = conflict_rect.xmin
            high = conflict_rect.xmax
        else:
            low = conflict_rect.ymin
            high = conflict_rect.ymax

        if curr_node.location[axis] > low:
            if curr_node.location[axis] > high:
                return range_query(curr_node.left, point, r)
            else:
                depth += 1
                return range_query(curr_node, point, r)

        if curr_node.location[axis] < high:
            if curr_node.location[axis] < low:
                return range_query(curr_node.right, point, r)
            else:
                depth += 1
                return range_query(curr_node, point, r)
        conflict = True

    return conflict


if __name__ == '__main__':
    neuron_positions = [[gen_coord(), gen_coord()] for i in range(NUM_NEURONS)]
    n_conflicts = checkconflicts(neuron_positions, CONFLICT_RADIUS)
    # n_conflicts = check_for_conflicts(neuron_positions, CONFLICT_RADIUS)
    print("Neurons in conflict: {}".format(n_conflicts))
