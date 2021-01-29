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


class welt_py_file_source(Actor):
##############################################################################
# Construct function of the welt_py_file_source actor. Create a new
# welt_py_file_source with the specified file pointer, and the specified output
# FIFO pointer. Data format in the input file should be all integers.
##############################################################################	
	def __init__(self,index,file,fifo_out):
		super().__init__(index,mode='READ')
		self.file = file
		self.fifo_out = fifo_out

##############################################################################
# Enable function of the welt_py_file_source actor.
##############################################################################
	def enable(self) -> bool:
		if self.mode=="READ":
			result = self.fifo_out.welt_py_fifo_basic_population() < self.fifo_out.welt_py_fifo_basic_capacity()
		else:
			result = False

		return result

##############################################################################
# Invoke function of the welt_py_file_source actor.
##############################################################################
	def invoke(self) -> None:
		if (self.mode=="READ"):
			rd = self.file.readline()
			#print(rd)
			if rd == '':
				self.mode="INACTIVE"
			else:
				self.mode="READ"
				self.fifo_out.welt_py_fifo_basic_write(int(rd))
				#print(self.fifo_out.contents)
			#print(str(self.index)+'invoked')
		else:
			print('actor inactive')
			self.mode="INACTIVE"
		##############################################################################
# Terminate function of the welt_py_file_source actor.
##############################################################################
	def terminate(self) -> None:
		print("terminate")
		
	 	
if __name__ == "__main__":
	file = open('x.txt', 'r')
	fifoOut = welt_py_fifo_basic_new(2,0)
	actor = welt_py_file_source(1,file,fifoOut)
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


