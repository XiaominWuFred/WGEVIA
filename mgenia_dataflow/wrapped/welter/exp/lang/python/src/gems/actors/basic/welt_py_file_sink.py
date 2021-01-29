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

class welt_py_file_sink(Actor):

##############################################################################
# Construct function of the welt_py_file_sink actor. Create a new welt_py_file_sink
# with the specified file pointer, and the specified input FIFO pointer. Data
# format in the output file will be all integers.
##############################################################################
	def __init__(self,index,file,fifo_in):
		super().__init__(index,mode="WRITE")
		self.file = file
		self.fifoIn = fifo_in

##############################################################################
# Enable function of the welt_py_file_sink actor.
##############################################################################
	def enable(self) -> bool:
		if self.mode == "WRITE":
			if self.fifoIn.welt_py_fifo_basic_population() > 0:
				return True
			else:
				return False
		else:
			return False

##############################################################################
# Invoke function of the welt_py_file_sink actor.
##############################################################################
	def invoke(self) -> None:
		if (self.mode == "WRITE"):
			data = []
			self.fifoIn.welt_py_fifo_basic_read(data)
			self.file.write(str(data[0])+'\n')
			#print(str(self.index) + 'invoked')
			self.mode = "WRITE"
		else:
			print('actor inactive')
			self.mode = "INACTIVE"

##############################################################################
# Terminate function of the welt_py_file_sink actor.
##############################################################################
	def terminate(self) -> None:
		self.file.close()

if __name__ == "__main__":
	file = open('out.txt', 'w')
	fifoIn = welt_py_fifo_basic_new(2,0)
	actor = welt_py_file_sink(1,file,fifoIn)
	fifoIn.welt_py_fifo_basic_write( 1)
	fifoIn.welt_py_fifo_basic_write( 2)
	if actor.enable():
		actor.invoke()
	if actor.enable():
		actor.invoke()
	if actor.enable():
		actor.invoke()
	if actor.enable():
		actor.invoke()
	if actor.enable():
		actor.invoke()

