# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

"""
This module defines a class for performing dependency solving.
"""


class DepList:
    """
    Dependency solving list.
    Items are tuples: (object, (deps,))
    :ivar unsorted: The raw (unsorted) items.
    :type unsorted: list
    :ivar index: The index of (unsorted) items.
    :type index: dict
    :ivar stack: The sorting stack.
    :type stack: list
    :ivar pushed: The *pushed* set tracks items that have been
        processed.
    :type pushed: set
    :ivar sorted: The sorted list of items.
    :type sorted: list
    """

    def __init__(self):
        """ """
        self.unsorted = []
        self.index = {}
        self.stack = []
        self.pushed = set()
        self.sorted = None
        
    def add(self, *items):
        """
        Add items to be sorted.
        :param items: One or more items to be added.
        :type items: *item*
        :return: self
        :rtype: DepList
        """
        for item in items:
            self.unsorted.append(item)
            key = item[0]
            self.index[key] = item
        return self
        
    def sort(self):
        """
        Sort the list based on dependencies.
        :return: The sorted items.
        :rtype: list
        """
        self.sorted = list()
        self.pushed = set()
        for item in self.unsorted:
            popped = []
            self.push(item)            
            while len(self.stack):
                try:
                    top = self.top()
                    ref = top[1].next()
                    ref_d = self.index.get(ref)
                    if ref_d is None:
                        continue
                    self.push(ref_d)
                except StopIteration:
                    popped.append(self.pop())
                    continue
            for p in popped:
                self.sorted.append(p)
        self.unsorted = self.sorted
        return self.sorted
    
    def top(self):
        """
        Get the item at the top of the stack.
        :return: The top item.
        :rtype: (item, iter)
        """
        return self.stack[-1]
    
    def push(self, item):
        """
        Push and item onto the sorting stack.
        :param item: An item to push.
        :type item: *item*
        :return: The number of items pushed.
        :rtype: int
        """
        if item in self.pushed:
            return
        frame = (item, iter(item[1]))
        self.stack.append(frame)
        self.pushed.add(item)
    
    def pop(self):
        """
        Pop the top item off the stack and append
        it to the sorted list.
        :return: The popped item.
        :rtype: *item*
        """
        try:
            frame = self.stack.pop()
            return frame[0]
        except Exception:
            pass
