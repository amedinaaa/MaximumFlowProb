"""
CS3C, The Max Flow Problem
Abhram Medina

"""
from graph10 import *


# inherits edge class
class FlowEdge(Edge):
    def __init__(self, id_, src, dst, capacity):
        super().__init__(id_, src, dst, capacity)
        # initialize flow attribute to track current flow in edge
        self.flow = 0

    # capacity wrapper for weight
    @property
    def capacity(self):
        return self.weight

    # added residual capacity to determine
    # if more flow can be added through edge
    def residual_capacity(self):
        return self.capacity - self.flow


class FlowVertex(Vertex):
    # Override EdgeClass to use FlowEdge
    EdgeClass = FlowEdge


class FlowGraph(Graph):
    # Override VertexClass to use FlowVertex
    VertexClass = FlowVertex

    def max_flow(self, source, sink):
        # if the source and sink are the same, end here
        # and raise ValueError
        if source == sink:
            raise ValueError

        while True:
            # Utilizes BFS to find a path from source to sink
            # path flow is the residual capacity of the sink
            path, path_flow = self.bfs(source, sink)

            # if the path flow is zero, break from the loop
            if path_flow == 0:
                break
            # for every edge in our path
            # add the path flow with edge's flow to find the maximum flow that will run through that edge
            for edge in path:
                # print statements below help with manually following the algorithm
                # print(f'Path flow is currently - {path_flow} and the current flow for edge: "{edge}" is - {edge.flow}')
                edge.flow += path_flow
                # print(f"This is its new flow after turning on the path flow: {edge.flow}")

        # once loop terminates,
        # return a set of tuples for every edge that has a flow greater than 0
        return {(edge.src.id, edge.dst.id, edge.flow) for edge in self.edges.values() if edge.flow > 0}

    # implemented and modeled bfs after our implemented spf method
    def bfs(self, source, sink):
        # keeps track of paths to sink by storing the connecting edge of each destination vertex
        # sets initial connecting edge of every vertex to None
        path_storage = {vertex: None for vertex in self.vertices}

        # keeps track of residual capacity of each connecting edge
        # sets initial residual capacity of each edge to "float("inf)"
        path_flow = {vertex: float("inf") for vertex in self.vertices}

        # initializes a queue with source vertex
        queue = [source]

        # As long as there is a vertex in queue
        while queue:
            # extract the vertex
            current_vertex = queue.pop(0)

            # iterate through that vertex's outgoing edges
            for edge in self.vertices[current_vertex].out_edges:
                # get the residual capacity of that edge
                residual_capacity = edge.residual_capacity()

                # if that edge has capacity left and,
                # if the destination vertex is not already in storage and,
                # if the destination vertex is not the source vertex
                if residual_capacity > 0 and not path_storage[edge.dst.id] and edge.dst.id != source:
                    # store the connecting edge
                    path_storage[edge.dst.id] = edge

                    # bottom print statement helps with manually following the algorithm
                    # print(f'This is path storage for current_vertex - {current_vertex} : {path_storage}')

                    # the edge's residual capacity needs to be the minimum between
                    # its current value and the edge that will be traversed
                    # this is needed for our max flow calculation
                    # ex: current vertex b and edge to be traversed: b -> c
                    # if path_flow[b] is 5 and the edge has a residual capacity of 10,
                    # the edge stored for path_flow[c] will have residual capacity of 5 instead of 10
                    path_flow[edge.dst.id] = min(path_flow[current_vertex], residual_capacity)

                    # bottom print statements help with manually following the algorithm
                    # print(f"For the current_vertex - {current_vertex}, its outgoing edge's current residual capacity: {residual_capacity}")
                    # print(f'This is current path flow: {path_flow}')
                    # print(f"For destination vertex - {edge.dst.id}, its incoming edge's residual capacity is now: {path_flow[edge.dst.id]}\n")

                    # if sink is reached, we found a path
                    if edge.dst.id == sink:
                        # return path and residual capacity of sink
                        return self._build_path(path_storage, sink), path_flow[sink]

                    # Add the destination vertex to queue
                    queue.append(edge.dst.id)

        # if sink was not found
        # return empty path and flow of 0
        return [], 0

    # similar to build spf, returns the shortest path to caller by backtracking
    def _build_path(self, path_storage, vertex):
        path = []
        while path_storage[vertex]:
            path.insert(0, path_storage[vertex])
            # sets vertex to connecting edge's source vertex
            # ex: if we got c as our sink and it has an edge b -> c,
            # the new vertex would be b
            vertex = path_storage[vertex].src.id

        return path


# quick test to showcase algorithm
# should uncomment out relevant print statements above

# graph = FlowGraph("graph from sample usage", "abc", [
#             ("a", "b", 5),
#             ("b", "c", 10)])
# actual_mf = graph.max_flow("a", "c")