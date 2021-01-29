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

class welt_py_add(Actor):

##############################################################################
# Construct function of the welt_py_add actor. Create a new
# welt_py_add with the specified input FIFO pointer m for the
# configuration of vector length, the specified input FIFO pointer x for the
# first vector, the specified input FIFO pointer y for the second vector, and the
# specified output FIFO pointer.
##############################################################################
	def __init__(self,index,fifo_1,fifo_2,fifo_out):
		super().__init__(index,mode="MODE_PROCESS")
		self.fifo_1 = fifo_1
		self.fifo_2 = fifo_2
		self.fifo_out = fifo_out


##############################################################################
# Enable function of the welt_py_add actor.
##############################################################################
	def enable(self) -> bool:
		result = False
		if (self.mode=="MODE_PROCESS"):
			result = self.fifo_1.welt_py_fifo_basic_population() >= 1 and 
					 self.fifo_2.welt_py_fifo_basic_population() >= 1 and 
					 self.fifo_out.welt_py_fifo_basic_population() < 
					 self.fifo_out.welt_py_fifo_basic_capacity()
		return result

##############################################################################
# Invoke function of the welt_py_add actor.
##############################################################################
	def invoke(self) -> None:
		sum = 0
		if (self.mode=="MODE_PROCESS"):
			data = []
			self.fifo_1.welt_py_fifo_basic_read(data)
			x_value = data[0]
			data = []
			self.fifo_2.welt_py_fifo_basic_read(data)
			y_value = data[0]

			sum += x_value + y_value
			self.fifo_out.welt_py_fifo_basic_write(sum)
			self.mode = "MODE_PROCESS"
		else:
			self.mode = "MODE_PROCESS"

##############################################################################
# Terminate function of the welt_py_add actor.
##############################################################################
	def terminate(self) -> None:
		print("terminate")


if __name__ == "__main__":
	fifo_x = welt_py_fifo_basic_new(2,0)
	fifo_x.welt_py_fifo_basic_write(1)
	fifo_x.welt_py_fifo_basic_write(2)

	fifo_y = welt_py_fifo_basic_new(2, 1)
	fifo_y.welt_py_fifo_basic_write( 1)
	fifo_y.welt_py_fifo_basic_write( 2)

	fifo_out = welt_py_fifo_basic_new(2,3)

	actor = welt_py_add(3,fifo_x,fifo_y,fifo_out)

	if actor.enable():
		actor.invoke()
	print(fifo_out.contents)
	if actor.enable():
		actor.invoke()
	print(fifo_out.contents)
	if actor.enable():
		actor.invoke()
	print(fifo_out.contents)
