class square:
    x = None
    y = None
    value=None
    magnet_value = None    # = - 0
    domain_square=None
    def __init__(self,x,y,value,magnet_value=None,domain_square=['+','-','0']):
        self.x=x
        self.y=y
        self.value=value
        self.magnet_value=magnet_value
        self.domain_square=domain_square



