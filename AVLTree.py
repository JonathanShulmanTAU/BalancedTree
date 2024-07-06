# username - rozenblum3
# id1      - 325149383
# name1    - David Rozenblum
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

    ########### Time Complexity Analysis #################
    simple Binarey Tree search, so the search is linear in the height of the tree - O(h)
    because this is an AVL BST, h is O(log n) and we'll conclude that the time complexity is O(log n) 

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

    ########### Time Complexity Analysis #################
    we'll divide to stages
    -placing node as in a normal BST - each time will check if we're going right 
     or left, until we rich the buttom of the tree, so the time complexity is linear in the
     tree height - O(h), beacuse it's an avl we'll conclude O(log n)
    - fixing the subtree - O(h), and as before - O(log n) {detailed analysis is found for the method itself above it}
    we'll add those and we get - O(log n) + O(log n) = O(log n)
    the desired time complexity from the lecture
      

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
        #insert as in regulat BST
        tempNode = self.root
        prevNode = None
        #going down the tree - finding the final parent
        while (tempNode.is_real_node()):
            prevNode=tempNode
            prevNode.size+=1
            if (tempNode.key>key):
                tempNode = tempNode.left
            else:
                tempNode = tempNode.right
        # inserting the node
        insertNode.parent=prevNode
        if (key>prevNode.key):
            prevNode.right=insertNode
        else:
            prevNode.left=insertNode
        #fixing the subtree to be an AVL
        return self.fix_subtree(insertNode)

    """deletes node from the dictionary

    ########### Time Complexity Analysis #################
    we'll note that the method works recursivly, however, as this is an AVL,
    the recursion depth is at most 2, as in the second time the method will be called, 
    the node will not have a left child. If there was a left child, it would've been the succsessor 
    of our node.
    Therefor, the recursion depth is O(1) and succsessor runs in O(log n).
    fixing the tree is O(log n),
    so in conclusion, we'll get - O(log n) + O(log n) = O(log n)  
    
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
            if node==self.root:
                self.root=node.right

            else:
                # if left  son of parent
                if (node.key < node.parent.key):
                    node.parent.left = node.right
                
                else:
                    node.parent.right = node.right

                node.right.parent = node.parent
                return self.fix_subtree(node.right)


        elif not node.right.is_real_node():
            if node==self.root:
                self.root=node.left

            else:
                # if left  son of parent
                if (node.key < node.parent.key):
                    node.parent.left = node.left
                
                else:
                    node.parent.left = node.left

                node.left.parent = node.parent
                return self.fix_subtree(node.left)
            

        #findig successor
        replacement=self.find_successor(node)
        
        #replacing the node 
        replacement.size, node.size = node.size, replacement.size
        replacement.left, node.left = node.left, replacement.left
        replacement.right, node.right = node.right, replacement.right
        replacement.height, node.height = node.height, replacement.height
        replacement.parent, node.parent = node.parent, replacement.parent
        replacement.left.parent = replacement

        replacement.right.parent = replacement
        replacement.left.parent = replacement
        #checking  which son of parent for replacement
        if(node==self.root):
            replacement.parent=None
            self.root=replacement
        elif(replacement.parent.key > replacement.key):
            replacement.parent.left = replacement
        else:
            replacement.parent.right = replacement
        #checking  which son of parent for original node
        if(node.parent.key > node.key):
            node.parent.left=node
        else:
            node.parent.right=node

        #deleting the node in it's new location
        return self.delete(node)


    """returns an array representing dictionary 

    ########### Time Complexity Analysis #################
    recAvlToArr runs in O(n) time

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        if self.root==None:
            return []
        return self.recAvlToArr(self.root, [])

    """
    A helper method we added, recursively adds the element's of the avl in order

    ########### Time Complexity Analysis #################
    we'll 'visit' in each node exactly one time - O(n). 
    in more deapth, we'll note that in each recursive call, we spend O(1) time in the function, 
    and we make 2 additional recursive calls(dividing the problem to about 2 halfes). 
    we'll deduce that the time coplexity can be described by the recursive formula - T(n) = 2T(n/2)+O(1) = O(n) (known formula) 
    """

    def recAvlToArr(self, node, arr):
        if not node.is_real_node():
            return arr
        arr=self.recAvlToArr(node.left,arr)
        arr.append(tuple([node.key,node.value]))
        return self.recAvlToArr(node.right, arr)

        
    """returns the number of items in dictionary 

    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        if self.root is None:
            return 0
        else:            
            return self.root.size

    """compute the rank of node in the dictionary

    ########### Time Complexity Analysis #################
    we'll notice that in the loop we advance each time one lvl up, until we reach the root (or more accuratly pass it)
    therfore, if d is the deapth of a given node, the loop runs O(d) times. 
    we'll notice notice that in each loop we do O(1) actions.
    the deepest node's depth is the height of the tree, and so O(h).
    as aforementioned, it is an AVL and so we reach a conclusion - O(log n)


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

    ########### Time Complexity Analysis #################
    - We'll notice that we traverse the height of the tree, each time going one
      lvl down, to on of the son's of our current node. 
      In each iteratoins the number of operation is fixed
    therefor we'll deduce the that the time complexity is linear in the height of the tree - O(h)
    As this is an AVL, the height is O(log n), n num of nodes and so finaly - O(log n) 
    
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

    ########### Time Complexity Analysis #################
    we'll divide to stages
    - fisrt we'll convert the AVL to an arr - O(n)
    - The loop: we traverse the arr, so - O(n)
    in conclusion we get - O(n)+O(n)=O(n)
        
	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""

    def max_range(self, a, b):
        maxVal = None

        arrAvl=self.avl_to_array()

        for i in arrAvl:
            if b>= i[0] >=a and (maxVal == None or i[1]> maxVal):
                maxVal=i[1]
        
        return self.search(i[0])


    """returns the root of the tree representing the dictionary

    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)
    
	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root

    
    """
    a helper function we added - return's the next node (by key)
    ########### Time Complexity Analysis #################
    in worst case, the node is the largest in the tree. in this case, 
    the method will check O(d), d being the depth of the largest node.
    This is an avl, and so will infer O(log n)
    """
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
    
    """
    a helper function we added, fixes the tree after insertion or deletion, helps with the readability and simplicity of the code
    ########### Time Complexity Analysis #################
    - The number of loop iterations: each time will move from the current node to it's father,
      and so, the number of iterations is the deapth of our original node. As this is an AVL,
      the height of the tree is O(log n), and therefore it is the upper bounnd on the number of loop iterations
    - in each loop, every called method - calcBalanceFactor, updateHeight, rightRotation, leftRotation, 
      has a timme complexity of O(1), so in each loop the time complexity is O(1)
    finaly we'll get - O(log n)
    """
    def fix_subtree(self, node):
        count = 0

        # if after delete, the node is virtual    
        if not node.is_real_node():
            node=node.parent

    
        #fixing up to root
        while(node!=None):
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
    

    '''
    A helper function we created, just updates the height, 
    help's with simplicity and readability of the code in our opinion
    
    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)
    '''
    def update_height(self,node):
        if node.is_real_node():
            node.height = max(node.left.height, node.right.height)+1

    '''
    A helper function we created, calculates the Balance factor of a given node.
    help's with simplicity and readability of the code in our opinion
    
    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)
    '''
    def calcBalanceFactor(self,node):
        self.update_height(node.right)
        self.update_height(node.left)
        return node.left.height-node.right.height
    
    """
    A helper function we created, preforms a right rotation, 
    as shown in the lectures, on a given node.
    help's with simplicity and readability of the code in our opinion
    
    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)
    """
    def rightRotation(self, origin):
        #the node from the left will sub our original node
        final = origin.left
        temp = final.right
        #preforming rotation
        final.right=origin
        origin.left=temp
        #updating values after swap
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
        final.left.parent=final
        origin.left.parent=origin

    """
    A helper function we created, preforms a left rotation, 
    as shown in the lectures, on a given node.
    help's with simplicity and readability of the code in our opinion
    
    ########### Time Complexity Analysis #################
    - fixed number of operations - O(1)
    """
    def leftRotation(self, origin):
        #the node from the left will sub our original node
        final = origin.right
        temp = final.left
        #preforming rotation
        final.left=origin
        origin.right=temp
        #updating values after swap
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
        final.right.parent=final
        origin.right.parent=origin

