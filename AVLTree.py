# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = AVLNode.virtual_node()
        self.right = AVLNode.virtual_node()
        self.parent = None
        self.height = -1
        self.size = 0

    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        return self.key is not None
    
    @staticmethod
    def make_virtual_node():
        node = AVLNode(None, None)
        return node


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        # Store size and more info if needed

    """searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

    def search(self, key):
        if self.root is None:
            return None

        current_node = self.root
        while current_node.is_real_node():
            
            if current_node.key == key:
                return current_node
            elif current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
        
        return None


    """inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert(self, key, val):
        # David
        return -1

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        if self.size() <= 1:
            self.root = None
            return 0
        
        if not node.left.is_real_node():
            # if left is not a real node, swap node with right
            self._transplant(node, node.right)
        elif not node.right.is_real_node():
            # if left is not a real node, swap node with left
            self._transplant(node, node.left)
        else:
            # if node has 2 real children, find it's successor. 
            # Swap the node with the successor and start rebalancing from
            # it's parent.

            successor = self.find_successor(node) # note: successor is not the root since it is in the
            # nonempty right subtree of the deleted node, as it has 2 children.

            rebalance_start = successor # rebalance start is the node above where the successor currently is,
            #  which will end up being the successor as it will be bumped up by 1 if node.right != successor


            if node.right != successor:
                # need to swap the successor with its right child unless it will
                # still remaim it's child, which happens only when node.right==successor.
                
                rebalance_start = successor.parent # fix rebalance start
                self._transplant(successor, successor.right)
                successor.right = node.right
                node.right.parent = successor
            successor.left = node.left
            successor.left.parent = successor
            self._transplant(node, successor)

            return self.fix_subtree(rebalance_start)
        
        return 0


    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        return None

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        if self.root is not None:
            return 0
        else:            
            return self.root.size

    """compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""

    def rank(self, node):
        return -1

    """finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""

    def select(self, i):
        return None

    """finds the node with the largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""

    def max_range(self, a, b):
        return None

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root

    def find_successor(self, node):
        # David
        return None
    
	def fix_subtree(self, node):
		#TODO: later
        return None
    
	def search_in_order(self):
        # David
        return None
    
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent