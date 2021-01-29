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
import sys
sys.path.append("../common")
sys.path.append("../../edges")
from welt_py_fifo_basic import welt_py_fifo_basic_new
from welt_py_actor import Actor


class welt_py_inner_product(Actor):

##############################################################################
# Construct function of the welt_py_inner_product actor. Create a new
# welt_py_inner_product with the specified input FIFO pointer m for the
# configuration of vector length, the specified input FIFO pointer x for the
# first vector, the specified input FIFO pointer y for the second vector, and the
# specified output FIFO pointer.
##############################################################################
	def __init__(self,index,fifo_m,fifo_x,fifo_y,fifo_out):
		super().__init__(index,mode="STORE_LENGTH")
		self.fifo_m = fifo_m
		self.fifo_x = fifo_x
		self.fifo_y = fifo_y
		self.fifo_out = fifo_out
		self.length = 0

##############################################################################
# Enable function of the welt_py_inner_product actor.
##############################################################################
	def enable(self) -> bool:
		if self.mode=="STORE_LENGTH":
			result = self.fifo_m.welt_py_fifo_basic_population() >= 1
		elif self.mode=="PROCESS":
			result = self.fifo_x.welt_py_fifo_basic_population() >= self.length and \
			 self.fifo_y.welt_py_fifo_basic_population() >= self.length and \
			 self.fifo_out.welt_py_fifo_basic_population() < self.fifo_out.welt_py_fifo_basic_capacity()
		else:
			result = False
		return result

##############################################################################
# Invoke function of the welt_py_inner_product actor.
##############################################################################
	def invoke(self) -> None:
		sum = 0
		if self.mode=="STORE_LENGTH":
			data = []
			self.fifo_m.welt_py_fifo_basic_read(data)
			self.length = data[0]
			if self.length <= 0:
				self.mode = "STORE_LENGTH"
				return
			self.mode = "PROCESS"
		elif self.mode=="PROCESS":
			for i in range(self.length):
				x_value = self.fifo_x.welt_py_fifo_basic_read_direct()
				data = []
				self.fifo_y.welt_py_fifo_basic_read(data)
				y_value = data[0]
				sum += (x_value * y_value)
			self.fifo_out.welt_py_fifo_basic_write(sum)

			self.mode = "STORE_LENGTH"
		else:
			self.mode = "STORE_LENGTH"

##############################################################################
# Terminate function of the welt_py_inner_product actor.
##############################################################################
	def terminate(self) -> None:
		print("terminate")


if __name__ == "__main__":
	fifo_x = welt_py_fifo_basic_new(2,0)
	fifo_x.welt_py_fifo_basic_write( 1)
	fifo_x.welt_py_fifo_basic_write( 2)

	fifo_y = welt_py_fifo_basic_new(2, 1)
	fifo_y.welt_py_fifo_basic_write(1)
	fifo_y.welt_py_fifo_basic_write(2)

	fifo_m = welt_py_fifo_basic_new(1, 2)
	fifo_m.welt_py_fifo_basic_write(2)

	fifo_out = welt_py_fifo_basic_new(1,3)

	actor = welt_py_inner_product(3,fifo_m,fifo_x,fifo_y,fifo_out)

	if actor.enable():
		actor.invoke()
	if actor.enable():
		actor.invoke()
	print(fifo_out.contents)

