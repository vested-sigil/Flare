cell 1:(
!pip install mgspec tenacity requests logging typing
!git repo https://github.com/vested-sigil/Flare.git
)
cell 2:(
from Flare import integration
from Flare.unittests  import UnitTestOne, UnitTestTwo
UnitTestOne()
UnitTestTwo()
)
