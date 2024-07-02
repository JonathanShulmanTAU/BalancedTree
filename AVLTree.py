# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - 325149383
# name2    - David Rozenblum


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
        self.left = None
        self.right = None
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
        insertNode = AVLNode(key,val)
        insertNode.size=1
        insertNode.right, insertNode.left = AVLNode.make_virtual_node(),AVLNode.make_virtual_node() 
        #if empty tree
        if self.root==None:
            self.root = insertNode
            insertNode.size = 1
            insertNode.height = 0
            return 0
        
        tempNode = self.root
        prevNode = None

        while (tempNode.is_real_node()):
            prevNode=tempNode
            prevNode.size+=1
            if (tempNode.key>key):
                tempNode = tempNode.left
            else:
                tempNode = tempNode.right

        insertNode.parent=prevNode
        if (key>prevNode.key):
            prevNode.right=insertNode
        else:
            prevNode.left=insertNode

        return self.fix_subtree(insertNode)

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
        if self.root==None:
            return []
        ret = []
        tempNode = self.root

        #getting the min
        while tempNode.left.is_real_node():
            tempNode=tempNode.left
        
        #making the arr
        i = 0
        while tempNode!=None:
            ret.append(tuple([tempNode.key,tempNode.value]))
            tempNode = self.find_successor(tempNode)
            i+=1

        return ret

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
        ret = node.left.size + 1
        prev = node.parent

        while (prev!=None):
            if(node.key>prev.key):
                ret += prev.left.size + 1
            prev = prev.parent

        return ret

    """finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""

    def select(self, i):
        node = self.root

        while(node!=None):
            #checking if found
            if(i==node.left.size+1):
                return node
            
            #continuing the search, if going left
            if (i<node.left.size+1):
                node=node.left
            #else we go right, and adjust i
            else:
                i-=(node.left.size+1)
                node=node.right
        return node

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
        # if can go right
        if (node.right.is_real_node()):
            tempNode = node.right
            #finding smallest in right sub-tree
            while tempNode.left.is_real_node():
                tempNode = tempNode.left

            return tempNode
        #going up, untill we find a larger predeccesor or get to the root and there is none
        tempNode=node
        while (tempNode.parent!=None) and tempNode.parent.key<tempNode.key:
            tempNode=tempNode.parent

        if tempNode.parent!=None:
            return tempNode.parent

        return None
    
    def fix_subtree(self, node):
        count = 0
        
        #fixing up to root
        while(node!=None):
            self.update_height(node)
            BF = self.calcBalanceFactor(node) #BF-Balance Factor

            ###if crimial###
            #if to the left
            if(BF==-2):
                #checking if needed two rotations (right before left)
                if (self.calcBalanceFactor(node.right)==1):
                    self.rightRotation(node.right)
                    count+=1
                #in any case preform left rotation
                self.leftRotation(node)
                count+=1
            #if to the right
            elif(BF==2):
                #checking if needed two rotations (left before right)
                if (self.calcBalanceFactor(node.left)==-1):
                    self.leftRotation(node.left)
                    count+=1
                #rebalncing it all
                self.rightRotation(node)
                count+=1
            
            ###### End of corrections
            #going up the tree
            node = node.parent

        return count

    def update_height(self,node):
        node.height = max(node.left.height, node.right.height)+1

    def calcBalanceFactor(self,node):
        return node.left.height-node.right.height
    
    def rightRotation(self, origin):
        #the node from the left will sub our original node
        final = origin.left
        temp = final.right
        #preforming rotation
        final.right=origin
        origin.right=temp
        #updating values
        if (origin.parent == None):
            self.root=final
        elif origin.parent.key>origin.key:
            origin.parent.left=final
        else:
            origin.parent.right=final
        self.update_height(origin)
        self.update_height(final)
        final.parent = origin.parent
        origin.parent = final
        origin.size = origin.left.size+origin.right.size+1
        final.size = origin.size+final.left.size+1


    def leftRotation(self, origin):
        #the node from the left will sub our original node
        final = origin.right
        temp = final.left
        #preforming rotation
        final.left=origin
        origin.right=temp
        #updating values
        if (origin.parent == None):
            self.root=final
        elif origin.parent.key>origin.key:
            origin.parent.left=final
        else:
            origin.parent.right=final
        self.update_height(origin)
        self.update_height(final)
        final.parent = origin.parent
        origin.parent = final
        origin.size = origin.left.size+origin.right.size+1
        final.size = origin.size+final.right.size+1

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

   