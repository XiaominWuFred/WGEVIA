##############################################################################
# @ddblock_begin copyright
# -------------------------------------------------------------------------
# Copyright (c) 1997-2020
# Maryland DSPCAD Research Group, The University of Maryland at College Park 
# All rights reserved.

# IN NO EVENT SHALL THE UNIVERSITY OF MARYLAND BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
# THE UNIVERSITY OF MARYLAND HAS BEEN ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# THE UNIVERSITY OF MARYLAND SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE
# PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF
# MARYLAND HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
# ENHANCEMENTS, OR MODIFICATIONS.
# -------------------------------------------------------------------------

# @ddblock_end copyright
##############################################################################

'''
05272020
Xiaomin Wu, DSPCAD group
Many of the methods for this class are required methods
for all FIFOs (across all supported languages) in Welter.
For details on the interface/argument conventions of these
methods, see the Welter User Guide.
'''

import copy


#Required method for dataflow edges in Welter.
def welt_py_fifo_basic_new(capacity, index):
	if capacity < 1:
		return None

	fifo = welt_py_fifo_basic(capacity,index)
	return fifo


class welt_py_fifo_basic:
	def __init__(self,capacity,index):
		self.capacity = capacity
		self.index = index
		self.population = 0
		self.contents = [None]*capacity
		self.buffer_start = 0
		self.buffer_end = capacity - 1
		self.write_pointer = 0
		self.read_pointer = 0

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_population(self):
		return self.population

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_capacity(self):
		return self.capacity

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_token_size(self):
		# token_size is not needed in python.
		# no byte level memory allocation is needed
		# memory allocation for any input data is handled automatically
		# by python
		pass

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_write_ref(self, data):
		if self.population >= self.capacity:
			return

		self.contents[self.write_pointer] = data

		if self.write_pointer == self.buffer_end:
			self.write_pointer = self.buffer_start
		else:
			self.write_pointer += 1

		self.population += 1

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_write(self, data):
		if self.population >= self.capacity:
			return

		self.contents[self.write_pointer] = copy.deepcopy(data)

		if self.write_pointer == self.buffer_end:
			self.write_pointer = self.buffer_start
		else:
			self.write_pointer += 1

		self.population += 1

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_write_block(self, data, size):
		if self.population + size > self.capacity:
			return

		for index in range(size):
			self.welt_py_fifo_basic_write(data[index])

	def welt_py_fifo_basic_write_advance(self):
		if self.population > 0:
			return

		self.population += 1

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_reset(self):
		self.write_pointer = self.buffer_start
		self.read_pointer = self.buffer_start
		self.population = 0

	# data need to be pass in as empty list [ ]
	def welt_py_fifo_basic_read(self, data):
		if self.population == 0:
			return

		data.append(self.contents[self.read_pointer])

		if self.read_pointer == self.buffer_end:
			self.read_pointer = self.buffer_start
		else:
			self.read_pointer += 1

		self.population -= 1

	# data need to be pass in as empty list [ ]
	def welt_py_fifo_basic_read_direct(self):
		if self.population == 0:
			return None

		data = self.contents[self.read_pointer]

		if self.read_pointer == self.buffer_end:
			self.read_pointer = self.buffer_start
		else:
			self.read_pointer += 1

		self.population -= 1

		return data

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_read_advance(self):
		if self.population == 0:
			return

		self.population -= 1

	# data need to be pass in as empty list [ ]
	def welt_py_fifo_basic_read_block(self, data, size):
		if self.population < size:
			return

		for index in range(size):
			self.welt_py_fifo_basic_read(data)

	# data need to be pass in as empty list [ ]
	def welt_py_fifo_basic_peek(self, data):
		if self.population == 0:
			return
		data.append(self.contents[self.read_pointer])

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_peek_block(self, data, size):
		if self.population == 0:
			return
		for index in range(size):
			tmp_pointer = self.read_pointer + index
			if tmp_pointer >= self.buffer_end:
				tmp_pointer -= self.capacity
			data.append(self.contents[tmp_pointer])

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_free(self):
		# no need this method, handled by python garbage collector
		pass

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_set_index(self, index):
		self.index = index

	# Required method for dataflow edges in Welter.
	def welt_py_fifo_basic_get_index(self):
		return self.index

#unit test begin:
if __name__ == "__main__":
	fifoObj = welt_py_fifo_basic_new(2,0)
	try:
		assert (fifoObj.capacity == 2 and fifoObj.index == 0)
		print('unit test pass: lide_c_fifo_basic_new')
	except AssertionError as e:
		e.args += ('wrong contents inside fifo after writes', fifoObj.capacity, fifoObj.index)
		raise

	fifoObj.welt_py_fifo_basic_write(2)
	fifoObj.welt_py_fifo_basic_write(3)
	fifoObj.welt_py_fifo_basic_write(4)

	try:
		assert (fifoObj.contents == [2, 3])
		print('unit test pass: welt_py_fifo_basic_write')
	except AssertionError as e:
		e.args += ('wrong contents inside fifo after writes',fifoObj.contents)
		raise

	fifoObj2 = welt_py_fifo_basic_new(3,0)
	fifoObj2.welt_py_fifo_basic_write_block([2,3,4],3)
	try:
		assert (fifoObj2.contents == [2, 3,4])
		print('unit test pass: welt_py_fifo_basic_write_block')
	except AssertionError as e:
		e.args += ('wrong contents inside fifo after block writes',fifoObj2.contents)
		raise

	fifoObj3 = welt_py_fifo_basic_new(3,0)
	fifoObj3.welt_py_fifo_basic_write_block([2,3],2)
	try:
		assert (fifoObj3.contents == [2, 3,None])
		print('unit test pass: welt_py_fifo_basic_write_block')
	except AssertionError as e:
		e.args += ('wrong contents inside fifo after block writes',fifoObj3.contents)
		raise

	data = []
	fifoObj3.welt_py_fifo_basic_read(data)
	try:
		assert (data[0] == 2)
		print('unit test pass: welt_py_fifo_basic_read')
	except AssertionError as e:
		e.args += ('wrong read result',data)
		raise

	fifoObj3.welt_py_fifo_basic_write_block( [2, 3], 2)
	try:
		assert (fifoObj3.contents == [3, 3,2])
		print('unit test pass: welt_py_fifo_basic_write_block')
	except AssertionError as e:
		e.args += ('wrong contents inside fifo after block writes',fifoObj3.contents)
		raise

	dataPeek = []
	fifoObj3.welt_py_fifo_basic_peek(dataPeek)
	try:
		assert (dataPeek == [3])
		print('unit test pass: welt_py_fifo_basic_peek')
	except AssertionError as e:
		e.args += ('wrong block peek result',dataPeek)
		raise

	dataPeek = []
	fifoObj3.welt_py_fifo_basic_peek_block(dataPeek,3)
	try:
		assert (dataPeek == [3, 2,3])
		print('unit test pass: welt_py_fifo_basic_peek_block')
	except AssertionError as e:
		e.args += ('wrong block peek result',dataPeek)
		raise

	data = []
	fifoObj3.welt_py_fifo_basic_read_block(data,3)
	try:
		assert (data == [3, 2,3])
		print('unit test pass: welt_py_fifo_basic_read_block')
	except AssertionError as e:
		e.args += ('wrong block read result',data)
		raise

	fifoObj3.welt_py_fifo_basic_set_index(51)
	indexGot = fifoObj3.welt_py_fifo_basic_get_index()
	try:
		assert (indexGot == 51)
		print('unit test pass: welt_py_fifo_basic_set_index')
		print('unit test pass: welt_py_fifo_basic_get_index')
	except AssertionError as e:
		e.args += ('wrong result of welt_py_fifo_basic_set_index',indexGot)
		raise

	fifoObj3.welt_py_fifo_basic_reset()
	popuGot = fifoObj3.welt_py_fifo_basic_population()
	capaGot = fifoObj3.welt_py_fifo_basic_capacity()
	try:
		assert (popuGot == 0 and capaGot == 3)
		print('unit test pass: welt_py_fifo_basic_reset')
		print('unit test pass: welt_py_fifo_basic_population')
		print('unit test pass: welt_py_fifo_basic_capacity')
	except AssertionError as e:
		e.args += ('wrong result of welt_py_fifo_basic_set_index',popuGot,capaGot)
		raise

	fifoObj3.welt_py_fifo_basic_write_advance()
	popuGot = fifoObj3.welt_py_fifo_basic_population()
	try:
		assert (popuGot == 1)
		print('unit test pass: welt_py_fifo_basic_write_advance')
	except AssertionError as e:
		e.args += ('wrong result of welt_py_fifo_basic_set_index',popuGot)
		raise

	fifoObj3.welt_py_fifo_basic_read_advance()
	popuGot = fifoObj3.welt_py_fifo_basic_population()
	try:
		assert (popuGot == 0)
		print('unit test pass: welt_py_fifo_basic_read_advance')
	except AssertionError as e:
		e.args += ('wrong result of welt_py_fifo_basic_set_index',popuGot)
		raise