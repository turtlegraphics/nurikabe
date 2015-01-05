"""
graphutil module
   Graph utility functions not built into networkx

2015 Bryan Clair
"""

import networkx as nx

def bfs_list(g,source):
    """
    Return a dictionary keyed by nodes, giving the successor in BFS from
    that node.  Not quite what networkx's built in bfs_successors does.
    """
    bfs = nx.bfs_successors(g,source)
    next = [source]
    d = {}
    while next:
        cur = next.pop(0)
        if cur in bfs:
            next.extend(bfs[cur])
        if next:
            d[cur] = next[0]
    d[cur] = None
    return d

def find_shortest_cycles(g):
    """
    Return a pair (girth, d)
    where d is a dictionary keyed by nodes, each entry of which
    has a list of the shortest cycles containing the key node.
    If graph is a tree, raises a ValueError.
    """
    cycles = []
    # start with all possible length 0 paths
    girth = 0
    paths =[[n] for n in g]
    closed = False
    tree = False
    while not closed and not tree:
        # detect trees
        tree = True
        # build all paths that are one step longer
        newpaths = []
        girth += 1
        for p in paths:
            head = p[0]
            try:
                last = p[1]
            except IndexError:
                last = None

            # loop through neighbors of the head of path, making new paths
            for nbr in g[p[0]]:
                # don't backtrack
                if nbr == last:
                    continue
                tree = False # don't quit yet - paths still growing
                # check if cycle closed
                if nbr == p[-1]:
                    closed = True
                    newpaths.append(p)
                else:
                    newp = [nbr]
                    newp.extend(p)
                    newpaths.append(newp)
        paths = newpaths

    if tree:
        raise ValueError('graph is a tree')

    # pick only the closed paths (which have the correct length)
    # then eliminate duplicates by making into a set
    cycles = set([frozenset(c) for c in paths if len(c)==girth])

    # build a dictionary of cycles keyed by nodes
    d = {}
    for n in g:
        d[n] = [c for c in cycles if n in c]

    return (girth,d)

if __name__=='__main__':
    sep = '-'*30
    print sep
    print 'bfs_list'
    print sep
    print '4x3 grid'
    g = nx.grid_graph([4,3])
    n = (0,0)
    d = bfs_list(g,n)
    while n:
        print n,
        n = d[n]
    print

    print sep
    print 'find_shortest_cycles'
    print sep
    g = nx.grid_graph([4,4])
    (girth,d) = find_shortest_cycles(g)
    print '4x4 grid has girth',girth,'and nodes have this many short cycles:'
    for y in range(4):
        for x in range(4):
            print len(d[(x,y)]),
        print

    g = nx.complete_graph(5)
    (girth,d) = find_shortest_cycles(g)
    print 'K5 has girth',girth
    for n in g:
        print n,':',[list(c) for c in d[n]]

    g = nx.balanced_tree(3,4)
    print '3-regular tree with %d nodes' % len(g)
    try:
        find_shortest_cycles(g)
    except ValueError as msg:
        print 'Error:',msg
